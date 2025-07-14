import streamlit as st
import pandas as pd
import plotly.express as px
from meridian_model_template import run_meridian_model

st.set_page_config(page_title="AI MMM Tool", layout="centered")
st.title("📊 AI MMM Tool (Beta)")

uploaded_file = st.file_uploader("Upload Your Campaign Data (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File Uploaded Successfully")
    st.dataframe(df.head())

    # Define expected media columns
    expected_media_cols = [
        "TV Spend (INR)",
        "Print Spend (INR)",
        "Outdoor Spend (INR)",
        "Cinema Spend (INR)",
        "YouTube Spend (INR)",
        "Facebook Ads Spend (INR)",
        "Google Ads Spend (INR)"
    ]

    media_cols = [col for col in expected_media_cols if col in df.columns]
    target = "revenue"

    # Check for necessary columns
    if not media_cols:
        st.error("❌ No media spend columns found. Please check column names in your file.")
    elif target not in df.columns:
        st.error("❌ 'revenue' column is missing. Please add a column named exactly 'revenue'.")
    else:
        try:
            # Run the model
            results = run_meridian_model(df, media_cols, target)
            st.subheader("📈 MMM Results Table")
            st.dataframe(results)

            # 📊 Chart 1: Normalized Contribution
            st.subheader("📊 Normalized Contribution by Media Channel")
            fig1 = px.bar(
                results,
                x='media_channel',
                y='normalized_contribution',
                title="Media Contribution to Revenue",
                labels={'normalized_contribution': 'Normalized Contribution'},
                color='media_channel'
            )
            st.plotly_chart(fig1)

            # 📉 Chart 2: Estimated ROI
            st.subheader("📉 Estimated ROI by Media Channel")
            fig2 = px.bar(
                results,
                x='media_channel',
                y='estimated_roi',
                title="ROI per Media Channel",
                labels={'estimated_roi': 'Estimated ROI'},
                color='media_channel'
            )
            st.plotly_chart(fig2)

            # 📥 Export Button
            st.subheader("📥 Export Results")
            csv = results.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name='mmm_results.csv',
                mime='text/csv',
            )

        except Exception as e:
            st.error(f"❌ Model failed to run: {e}")
else:
    st.info("⬆️ Please upload a CSV file to get started.")

  
