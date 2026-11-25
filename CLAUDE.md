# CLAUDE.md

## Goal
DemoCheck: classify a robot teleoperation recording (episode) as success or fail
from the robot's own signals. Course project, "Vibe coding with Claude", Ariel University.
Course-sized scope: Jupyter notebooks + sklearn. No Streamlit (lecturer asked for a notebook).

## Data
- Public: Hugging Face `unitreerobotics/G1_WBT_Inspire_Plastic_Box_Parts` (LeRobot v3.0,
  G1 + Inspire hands, 200 episodes, 30 fps). No success labels.
- Lab: ARCA lab G1 recordings, labeled success/fail by the operator. Not in repo yet
  (needs approval from the lab head).
- `scripts/make_sample.py` downloads one parquet file to `data/raw/` (git-ignored)
  and writes small CSVs to `data/`.

## ML
- y: operator label, success yes/no (binary classification).
- X: per-episode features (duration, max speed, grip time, finger open/close count, stops).
- One row = one episode. If rows are time windows, split train/test BY EPISODE (leakage).

## Files
- `README.md`: project definition in Hebrew (for humans)
- `notebooks/`: one notebook per milestone, must pass Restart and Run All
- `IDEA.md`: idea, form answers, open questions

## Rules
- Hebrew, RTL for course docs and notebook conclusions. Code and file names in English.
- Never use em dashes or similar long dashes. Use "-" or rephrase.
- Every plot gets a one-line conclusion under it.
- Do not invent data fields or numbers. Check the real files.
- Noam is not an experienced Python programmer: explain what the code does.
