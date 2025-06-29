import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("clustered_prioritization.csv")
full_feedback = pd.read_csv("expanded_customer_feedback.csv")

tier_label = {1: "Free", 2: "SMB", 3: "Enterprise"}

# Page setup
st.set_page_config(page_title="AI Feature Prioritization", layout="wide")
st.title("📊 AI-Powered Feature Prioritization Dashboard")

# 🧠 App Overview
st.markdown("""
### 🤖 What This App Does

This dashboard uses AI to turn messy customer feedback into clear feature priorities.

Here's how it works:
- Groups similar user comments into **feature themes**
- Scores each theme based on **who said it, how often, and how happy they were**
- Lets you **filter** to explore what matters most

#### 🔍 Metric Cheat Sheet:
- **NPS**: How happy users are (1–10 scale)
- **Frequency**: How many users mentioned it
- **Tier Weight**: Free = 1, SMB = 2, Enterprise = 3
- **Score** = Frequency × (1 + Tier Weight) × NPS ÷ 10
---
""")

# 🎛️ Filters
st.sidebar.header("🎛️ Filter Feature Clusters")

min_score = st.sidebar.slider("Minimum Priority Score", 
                              min_value=float(df["score"].min()), 
                              max_value=float(df["score"].max()), 
                              value=float(df["score"].min()), step=1.0)

min_nps = st.sidebar.slider("Minimum Avg NPS (User Happiness)", 
                            min_value=0.0, max_value=10.0, value=0.0, step=0.5)

min_freq = st.sidebar.slider("Minimum Mentions (How Many Users)", 
                             min_value=1, max_value=int(df["frequency"].max()), 
                             value=1)

# Apply filters
filtered = df[
    (df["score"] >= min_score) &
    (df["avg_nps"] >= min_nps) &
    (df["frequency"] >= min_freq)
].sort_values("score", ascending=False)

st.subheader(f"📌 Showing {len(filtered)} Prioritized Feature Cluster(s)")

if filtered.empty:
    st.warning("No results match your filters. Try adjusting them.")
else:
    for _, row in filtered.iterrows():
        cluster_id = row["cluster_id"]
        freq = int(row["frequency"])
        nps = round(row["avg_nps"], 2)
        tier = round(row["avg_tier_weight"], 2)
        score = round(row["score"], 2)

        examples = full_feedback[full_feedback["cluster"] == cluster_id]["text"].tolist()

        # --- Display Cluster ---
        st.markdown(f"""
        ---
        ### 🧠 Feature Cluster {cluster_id}
        **Why this matters:**  
        - 🗣️ Mentioned by **{freq}** users  
        - 🧲 Avg Tier: **{tier}** ({tier_label.get(round(tier), "Mixed")})  
        - 😊 Avg NPS: **{nps}**  
        - 📈 Score = {freq} × (1 + {tier}) × {nps} ÷ 10 = **{score}**
        """)

        # Show example feedback as bullet points
        if examples:
            st.markdown("**Top User Comments in This Cluster:**")
            for ex in examples[:5]:
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
