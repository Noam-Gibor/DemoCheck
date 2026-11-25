"""Download one file of the public Unitree G1 dataset and save a small sample to data/.

Outputs:
  data/episodes_summary.csv  one row per episode (frames, duration)
  data/sample_episode.csv    one episode: time + arm joints + finger states
"""
from pathlib import Path
import urllib.request

import numpy as np
import pandas as pd

URL = ("https://huggingface.co/datasets/unitreerobotics/G1_WBT_Inspire_Plastic_Box_Parts"
       "/resolve/main/data/chunk-000/file-000.parquet")
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "file-000.parquet"  # ~90MB, ignored by git

# Array columns from meta/info.json and the names of their elements
ARRAYS = {
    "observation.state.left_arm": ["shoulder_pitch", "shoulder_roll", "shoulder_yaw", "elbow",
                                   "wrist_yaw", "wrist_roll", "wrist_pitch"],
    "observation.state.right_arm": ["shoulder_pitch", "shoulder_roll", "shoulder_yaw", "elbow",
                                    "wrist_yaw", "wrist_roll", "wrist_pitch"],
    "observation.state.left_fig6d": ["thumb_oc", "thumb_lat", "index", "middle", "ring", "little"],
    "observation.state.right_fig6d": ["thumb_oc", "thumb_lat", "index", "middle", "ring", "little"],
}


def main():
    if not RAW.exists():
        RAW.parent.mkdir(parents=True, exist_ok=True)
        print("Downloading", URL)
        urllib.request.urlretrieve(URL, RAW)

    df = pd.read_parquet(RAW, columns=["episode_index", "frame_index", "timestamp", *ARRAYS])

    summary = (df.groupby("episode_index")
                 .agg(n_frames=("frame_index", "size"), duration_s=("timestamp", "max"))
                 .reset_index())
    summary.to_csv(ROOT / "data" / "episodes_summary.csv", index=False)

    ep = df[df["episode_index"] == summary["episode_index"].iloc[0]]
    out = ep[["episode_index", "frame_index", "timestamp"]].reset_index(drop=True)
    for col, names in ARRAYS.items():
        side = col.split(".")[-1]  # e.g. right_arm
        values = np.stack(ep[col].to_numpy())
        assert values.shape[1] == len(names), f"{col}: expected {len(names)} values"
        out[[f"{side}_{n}" for n in names]] = values
    out.to_csv(ROOT / "data" / "sample_episode.csv", index=False)

    print(f"{len(summary)} episodes in this file, sample episode has {len(out)} frames")


if __name__ == "__main__":
    main()
