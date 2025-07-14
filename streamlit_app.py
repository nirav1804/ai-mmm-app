import streamlit as st
import pandas as pd
from meridian_model_template import run_meridian_model

st.title("📊 AI MMM Tool (Beta)")

uploaded_file = st.file_uploader("Upload Your Campaign Data (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df.head())
    
    media_cols = [col for col in df.columns if "spend" in col]
    target = "revenue"
    
    results = run_meridian_model(df, media_cols, target)
    st.subheader("📈 MMM Results")
    st.dataframe(results)
else:
    st.warning("Please upload a CSV file.")
