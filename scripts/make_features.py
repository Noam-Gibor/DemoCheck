"""Turn robomimic Lift MH recordings into a table: one row per recording (demo).

Input : data/raw/lift_mh_low_dim_v15.hdf5  (download link in data/README.md)
Output: data/demos_features.csv

Each recording is a sequence of robot states at 20 Hz. For each one we compute
a few numbers that describe HOW the operator moved (speed, smoothness, pauses...).
The label (y) comes from the dataset: which operator group recorded it.
"""
from pathlib import Path
import urllib.request

import h5py
import numpy as np
import pandas as pd

URL = ("https://huggingface.co/datasets/amandlek/robomimic/resolve/main"
       "/v1.5/lift/mh/low_dim_v15.hdf5")
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "lift_mh_low_dim_v15.hdf5"  # ~51MB, ignored by git
HZ = 20  # control frequency, from env_args in the file
IDLE_SPEED = 0.02  # m/s: below this the hand counts as "not moving"


def operator_of_each_demo(f):
    """The file has lists (masks) like 'worse_operator_1' -> demo names."""
    owner = {}
    for group in ["worse", "okay", "better"]:
        for i in [1, 2]:
            for d in f["mask"][f"{group}_operator_{i}"][:]:
                owner[d.decode()] = (f"{group}_{i}", group)
    return owner


def features(demo):
    obs = demo["obs"]
    pos = obs["robot0_eef_pos"][:]           # hand position x,y,z (meters)
    joint_vel = obs["robot0_joint_vel"][:]   # 7 joint speeds (rad/s)
    actions = demo["actions"][:]             # operator commands, last column = gripper
    n = len(pos)

    step = np.linalg.norm(np.diff(pos, axis=0), axis=1)  # distance moved each step
    speed = step * HZ
    path = step.sum()
    straight = np.linalg.norm(pos[-1] - pos[0])
    grip = np.sign(actions[:, -1])

    return {
        "n_steps": n,
        "duration_s": n / HZ,
        "path_length_m": path,
        "straightness": straight / path if path > 0 else np.nan,
        "mean_speed": speed.mean(),
        "max_speed": speed.max(),
        "mean_joint_speed": np.linalg.norm(joint_vel, axis=1).mean(),
        "action_jerk": np.linalg.norm(np.diff(actions[:, :-1], axis=0), axis=1).mean(),
        "gripper_switches": int((np.diff(grip) != 0).sum()),
        "idle_fraction": (speed < IDLE_SPEED).mean(),
    }


def main():
    if not RAW.exists():
        RAW.parent.mkdir(parents=True, exist_ok=True)
        print("Downloading", URL)
        urllib.request.urlretrieve(URL, RAW)

    rows = []
    with h5py.File(RAW, "r") as f:
        owner = operator_of_each_demo(f)
        for name, demo in f["data"].items():
            operator, quality = owner.get(name, (None, None))
            rows.append({"demo": name, "operator": operator, "quality": quality,
                         **features(demo)})

    df = pd.DataFrame(rows)
    df["is_worse"] = (df["quality"] == "worse").astype(int)  # y: 1 = low-quality operator
    df = df.sort_values("demo", key=lambda s: s.str[5:].astype(int)).reset_index(drop=True)
    assert len(df) == 300 and df["operator"].notna().all(), "every demo should have an operator"
    df.to_csv(ROOT / "data" / "demos_features.csv", index=False)
    print(df.shape)
    print(df.groupby("quality").size())


if __name__ == "__main__":
    main()
