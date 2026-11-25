"""DemoCheck - first app (M1): project name, project sentence, and a first look at the data."""
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="DemoCheck", page_icon="🤖")


def rtl(text):
    # blank lines let markdown (### headers) render inside the RTL div
    st.markdown(f'<div dir="rtl">\n\n{text}\n\n</div>', unsafe_allow_html=True)


st.title("🤖 DemoCheck")
rtl("### בודק איכות להקלטות טלאופרציה")
rtl("חוקרים שאוספים הקלטות טלאופרציה לאימון רובוטים סובלים מהקלטות גרועות שנכנסות לאימון "
    "בלי שאף אחד שם לב, ואנחנו נבנה מחברת שמזהה הקלטות באיכות נמוכה מתוך תנועת הרובוט, בעזרת ML.")

data = Path(__file__).parent / "data" / "demos_clean.csv"
if data.exists():
    df = pd.read_csv(data)
    rtl(f"#### 📊 הנתונים: {len(df)} הקלטות, {df['operator'].nunique()} מפעילים")
    st.dataframe(df.head())
else:
    st.warning("data/demos_clean.csv not found. Run scripts/make_features.py and notebooks/m2_eda.ipynb")

st.info("🚧 בקרוב: מודל שמסמן הקלטות חשודות 🟢🔴")
