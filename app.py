import streamlit as st
import pandas as pd

# Load the finalized feature clusters
df = pd.read_csv("clustered_prioritization.csv")

st.set_page_config(page_title="AI Feature Prioritization", layout="wide")
st.title("📊 AI-Powered Feature Prioritization")

# Intro block to onboard users
st.markdown("""
### 🤖 What This App Does
This tool analyzes customer feedback and **automatically clusters, scores, and ranks feature requests** using AI.

It helps Product Managers identify high-impact features by:
- 🧠 Grouping similar feedback themes using NLP
- 📊 Scoring them by frequency, customer tier, and NPS
- 🎯 Visualizing which features deserve attention now

Use the filters to explore and prioritize features!
---
""")

# Sidebar filter with EXPLAINED labels
st.sidebar.header("🎛️ Filter Feature Clusters")
min_score = st.sidebar.slider(
    label="Minimum Importance Score (combines impact, NPS, and tier weight)",
    min_value=0.0, max_value=float(df["score"].max()), value=0.0, step=1.0
)
min_nps = st.sidebar.slider(
    label="Minimum Average NPS (user satisfaction level)",
    min_value=0.0, max_value=10.0, value=0.0, step=0.5
)
min_freq = st.sidebar.slider(
    label="Minimum Frequency (number of users requesting this)",
    min_value=1, max_value=int(df["frequency"].max()), value=1, step=1
)

# Filter and sort
filtered = df[
    (df["score"] >= min_score) &
    (df["avg_nps"] >= min_nps) &
    (df["frequency"] >= min_freq)
].sort_values("score", ascending=False)

# Note for filtering edge cases
if filtered.empty:
    st.warning("No feature clusters match the selected filters. Try lowering your thresholds.")

# Show clusters
st.subheader(f"📌 Showing {len(filtered)} Prioritized Feature Cluster(s)")

for _, row in filtered.iterrows():
    st.markdown(f"""
    ---
    ### 🧠 {row['topic_cluster']}
    **Summary**: {row['summary']}  
    **Score**: `{row['score']:.2f}`  
    - 🗣️ Frequency: `{row['frequency']}` users mentioned this
    - 📈 Avg NPS: `{row['avg_nps']:.2f}`
    - 🧲 Avg Tier Weight: `{row['avg_tier_weight']:.2f}`
    """)

# Download button
st.download_button(
    label="📥 Download CSV of Filtered Priorities",
    data=filtered.to_csv(index=False),
    file_name="prioritized_features_filtered.csv",
    mime="text/csv"
)
