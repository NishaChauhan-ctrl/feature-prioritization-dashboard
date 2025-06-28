import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("clustered_prioritization.csv")

st.set_page_config(page_title="AI Feature Prioritization", layout="wide")
st.title("📊 AI-Powered Feature Prioritization")

# 🧠 Intro
st.markdown("""
### 🤖 What This App Does
This dashboard clusters customer feedback into feature themes using AI, and helps Product Managers prioritize what to build next.

Each feature theme is:
- 🧠 Grouped from similar user comments
- 📈 Scored by **frequency × NPS × tier weight**
- 📋 Summarized and shown with top example comments

Use the filters to explore high-impact requests.
---
""")

# 🎛️ Sidebar filters with explained labels
st.sidebar.header("🎛️ Filter Feature Clusters")
min_score = st.sidebar.slider("Minimum Score (impact priority)", 0.0, float(df["score"].max()), 0.0, step=1.0)
min_nps = st.sidebar.slider("Minimum Avg NPS (user sentiment)", 0.0, 10.0, 0.0, step=0.5)
min_freq = st.sidebar.slider("Minimum Frequency (how many users said this)", 1, int(df["frequency"].max()), 1)

# Filter
filtered = df[
    (df["score"] >= min_score) &
    (df["avg_nps"] >= min_nps) &
    (df["frequency"] >= min_freq)
].sort_values("score", ascending=False)

if filtered.empty:
    st.warning("No clusters match your filters. Try adjusting the sliders.")

# Display clusters
st.subheader(f"📌 Showing {len(filtered)} Prioritized Feature Cluster(s)")

# Load original feedback for context
full_feedback = pd.read_csv("expanded_customer_feedback.csv")
tier_label = {1: "Free", 2: "SMB", 3: "Enterprise"}

for _, row in filtered.iterrows():
    cluster_label = row["topic_cluster"]
    summary = row["summary"]
    score = row["score"]
    freq = int(row["frequency"])
    nps = round(row["avg_nps"], 2)
    tier = round(row["avg_tier_weight"], 2)
    
    # Get matching examples
    cluster_num = -1 if "Miscellaneous" in cluster_label else int(cluster_label.split()[-1])
    examples = full_feedback[full_feedback["embedding"].notnull()]  # ensure loaded via Colab
    try:
        examples = full_feedback[full_feedback["cluster"] == cluster_num]["text"].tolist()
    except:
        examples = []

    st.markdown(f"""
    ---
    ### 🧠 **{summary}**
    **Cluster**: `{cluster_label}`  
    **Why it matters:**  
    - 🗣️ Mentioned by `{freq}` users
    - 🧲 Avg Tier: `{tier}` ({tier_label.get(round(tier), 'Mixed')})
    - 📈 Avg NPS: `{nps}`
    - 🔢 Score = `{freq}` × (1 + {tier}) × {nps} / 10 = **`{score:.2f}`**

    **Example Feedback:**
    """)

    if examples:
        for ex in examples[:3]:
            st.markdown(f"- “{ex}”")
    else:
        st.markdown("_No sample feedback available for this cluster._")

# 📥 Download
st.download_button(
    label="📥 Download Filtered Priorities as CSV",
    data=filtered.to_csv(index=False),
    file_name="prioritized_features_filtered.csv",
    mime="text/csv"
)
