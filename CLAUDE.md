# CLAUDE.md

## Goal
DemoCheck: flag low-quality robot teleoperation recordings from the robot's own motion.
Course project, "Vibe coding with Claude", Ariel University. Solo (Noam).
Course-sized scope: Jupyter notebooks + sklearn. No Streamlit for now (lecturer asked for notebooks).

## Data (M2 onward)
- robomimic Lift MH (`data/raw/lift_mh_low_dim_v15.hdf5`, git-ignored, MIT license):
  300 human teleop demos, 6 operators x 50, Panda arm in robosuite sim, 20 Hz. All demos succeed.
- Operator groups come from the file's `mask/<group>_operator_<i>` lists.
- `scripts/make_features.py` -> `data/demos_features.csv` (one row per demo).
- Notebook M2 drops `n_steps` -> `data/demos_clean.csv` (300 rows, 13 columns).
- M1 used Unitree G1 public data (`scripts/make_sample.py`), no labels. Lab G1 data: later, needs approval.

## ML
- y = `is_worse` (1 = worse operator). 100 yes / 200 no. Label is per OPERATOR, not per demo.
- X: duration_s, path_length_m, straightness, mean_speed, max_speed, mean_joint_speed,
  action_jerk, gripper_switches, idle_fraction.
- NEVER use `operator` or `quality` as features (they define y).
- Baseline: majority class, accuracy 66.7%, recall 0.
- M3: split train/test BY OPERATOR (each operator has a style; random split leaks it).

## What EDA found (details in INSIGHTS.md)
- duration_s strongest (r=0.66). Worse operators ~2x slower, path only ~25% longer.
- mean_speed ~ mean_joint_speed (r=0.94): keep one. max_speed, action_jerk ~ no signal.

## Files
- `README.md`: project definition in Hebrew (for humans). `INSIGHTS.md`: EDA conclusions.
- `notebooks/`: one notebook per milestone, must pass Restart and Run All.

## Rules
- Hebrew, RTL for course docs and notebook conclusions. Code and file names in English.
- Never use em dashes or similar long dashes. Use "-" or rephrase.
- Every plot gets a conclusion under it, with numbers that match the output.
- Do not invent data fields or numbers. Check the real files.
- Noam is not an experienced Python programmer: explain what the code does.
