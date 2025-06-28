import streamlit as st
import pandas as pd


# Load the prioritized feature data
df = pd.read_csv("clustered_prioritization.csv")


st.set_page_config(page_title="Feature Prioritization", layout="wide")
st.title("📊 AI-Powered Feature Prioritization")

st.markdown("""
### 🤖 What This App Does
This app uses AI to analyze raw customer feedback and automatically **prioritize product features**.

It does this by:
- 🧠 Clustering similar requests using NLP
- 📝 Summarizing feature themes
- 📊 Scoring each group based on **frequency**, **NPS**, and **customer tier**
- 🎯 Helping Product Managers focus on what matters most

Use the filters in the sidebar to explore high-impact features!

---
""")

# Sidebar filters
st.sidebar.header("🔍 Filter Features")
min_score = st.sidebar.slider("Minimum Score", 0.0, float(df["score"].max()), 0.0)
min_nps = st.sidebar.slider("Minimum Avg NPS", 0.0, 10.0, 0.0)
min_freq = st.sidebar.slider("Minimum Frequency", 1, int(df["frequency"].max()), 1)


filtered = df[
    (df["score"] >= min_score) &
    (df["avg_nps"] >= min_nps) &
    (df["frequency"] >= min_freq)
].sort_values("score", ascending=False)


st.write(f"📌 Showing {len(filtered)} features")
for _, row in filtered.iterrows():
    st.markdown(f"""
    ---
    ### 🧠 Feature Cluster {int(row['topic_cluster'])}
    **Summary:** {row['summary']}  
    **Score:** `{row['score']:.2f}`  
    - Avg NPS: `{row['avg_nps']:.2f}`  
    - Frequency: `{row['frequency']}`  
    - Avg Tier Weight: `{row['avg_tier_weight']:.2f}`
    """)


# Download CSV button
st.download_button(
    label="📥 Download CSV",
    data=filtered.to_csv(index=False),
    file_name="prioritized_features.csv",
    mime="text/csv"
)
