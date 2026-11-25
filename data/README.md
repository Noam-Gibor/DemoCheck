<div dir="rtl">

# 📂 נתונים

## M2: robomimic Lift MH
| קובץ | מה יש בו | בריפו? |
|---|---|---|
| `demos_features.csv` | שורה לכל הקלטה (300): מפעיל, קבוצה, 10 מאפיינים, y | כן |
| `demos_clean.csv` | אותה טבלה אחרי ניקוי (בלי `n_steps`), נוצרת במחברת M2 | כן |
| `raw/lift_mh_low_dim_v15.hdf5` | הקובץ המקורי (כ-51MB) | לא |

**המקור:** https://huggingface.co/datasets/amandlek/robomimic/resolve/main/v1.5/lift/mh/low_dim_v15.hdf5 (רישיון MIT)
**איך יוצרים מחדש:** `python scripts/make_features.py`

## M1: Unitree G1 (מבט ראשון על הפורמט)
| קובץ | מה יש בו | בריפו? |
|---|---|---|
| `episodes_summary.csv` | שורה לכל הקלטה: מספר פריימים ומשך בשניות | כן |
| `sample_episode.csv` | הקלטה אחת: זמן, 7 מפרקים בכל זרוע, 6 ערכי אצבעות בכל יד | כן |
| `raw/file-000.parquet` | הקובץ המקורי (כ-90MB) | לא |

**המקור:** [unitreerobotics/G1_WBT_Inspire_Plastic_Box_Parts](https://huggingface.co/datasets/unitreerobotics/G1_WBT_Inspire_Plastic_Box_Parts), הקובץ `data/chunk-000/file-000.parquet` (19 הקלטות מתוך 200).
**איך יוצרים מחדש:** `python scripts/make_sample.py`

**נתוני המעבדה:** עוד לא כאן. יתווספו אחרי אישור של ראש המעבדה.

</div>
