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

    # Show actual columns
    st.write("📂 Columns in uploaded file:")
    st.write(df.columns.tolist())

    # Expected media spend columns from your file
    expected_media_cols = [
        "TV Spend",
        "Print Spend",
        "Outdoor Spend",
        "Cinema Spend",
        "YouTube Spend",
        "FacebookAds Spend",
        "GoogleAds Spend",
        "Programmatic Spend",
        "RegionalPrint Spend",
        "RegionalOutdoor Spend",
        "RegionalDigital Spend",
        "RegionalRadio Spend",
        "GroundActivation Spend"
    ]

    media_cols = [col for col in expected_media_cols if col in df.columns]
    target = "revenue"

    if not media_cols:
        st.error("❌ No media spend columns found. Please check your column names.")
    elif target not in df.columns:
        st.error("❌ 'revenue' column is missing. Please add a column named exactly 'revenue'.")
    else:
        try:
            # Debugging display
            st.write("✅ Media columns being used:", media_cols)
            st.write("✅ Target column:", target)

            X = df[media_cols]
            y = df[target]
            st.write("✅ Shape of X (media input):", X.shape)
            st.write("✅ Shape of y (target):", y.shape)

            if X.empty or y.empty:
                st.error("❌ Input data is empty. Check your CSV values.")
            else:
                results = run_meridian_model(df, media_cols, target)
                st.subheader("📈 MMM Results Table")
                st.dataframe(results)

                # 🧠 Automated Analysis & Recommendation
                st.subheader("🧠 Insights & Recommendations")

                # Sort by ROI and Contribution
                top_roi = results.sort_values(by="estimated_roi", ascending=False)
                top_contribution = results.sort_values(by="normalized_contribution", ascending=False)

                # Get best and worst
                best_channel = top_roi.iloc[0]['media_channel']
                best_roi = top_roi.iloc[0]['estimated_roi']
                worst_channel = top_roi.iloc[-1]['media_channel']
                worst_roi = top_roi.iloc[-1]['estimated_roi']

                # Low ROI channels (arbitrary threshold: <1.0)
                low_roi_channels = results[results["estimated_roi"] < 1.0]["media_channel"].tolist()
                high_contrib_channels = results[results["normalized_contribution"] > 0.15]["media_channel"].tolist()

                # ✅ Always show best/worst
                st.markdown(f"""
                - ✅ **Most efficient channel:** `{best_channel}` with an estimated ROI of **{best_roi:.2f}**
                - 🚫 **Least efficient channel:** `{worst_channel}` with an ROI of **{worst_roi:.2f}**
                """)

                # 🔍 Show low ROI if any
                if low_roi_channels:
                    st.markdown(f"- ⚠️ **Channels with ROI < 1.0:** {', '.join(low_roi_channels)}")
                else:
                    st.markdown("- ✅ No channels have ROI below 1.0 — good efficiency overall.")

                # 🔝 Show high contributors
                if high_contrib_channels:
                    st.markdown(f"- 🔝 **Top contributors (>15%)**: {', '.join(high_contrib_channels)}")
                else:
                    st.markdown("- ℹ️ No channel has a contribution >15%")

                # 📌 Recommendation summary
                st.info(f"""
                📌 **Recommendation:**

                Focus more on `{best_channel}` due to its high ROI (**{best_roi:.2f}**).
                Consider reallocating part of the budget from `{worst_channel}` (ROI: **{worst_roi:.2f}**) if needed.

                {"Monitor " + ", ".join(low_roi_channels) + " closely as they are below break-even ROI." if low_roi_channels else "Continue to monitor all channels to sustain high ROI."}
                """)

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
