# 🔍 AI-Powered Feature Prioritization Dashboard

This Streamlit app helps Product Managers turn messy qualitative feedback into **data-driven feature priorities** — using clustering, scoring, and summarization powered by AI.

📍 Live demo
👉 [Launch the app](https://feature-prioritization-dashboard-hppx2bnntk4eezccu9c2qz.streamlit.app/)

---

## 🧠 What It Does

Product teams get flooded with user feedback — but how do you **decide what to build next**?

This app:
- ✅ Groups similar user feedback into **feature clusters** using embeddings + HDBSCAN
- 📊 Scores each cluster based on:
  - How many users mentioned it
  - How happy they were (NPS)
  - Which tier they belong to (Free, SMB, Enterprise)
- 🧠 Shows example feedback for each cluster so you can understand the **why** behind the numbers
- 🎛️ Lets you filter results interactively to explore high-priority themes

---

## 📈 Scoring Formula
Score = Frequency × (1 + Tier Weight) × Avg NPS ÷ 10

| Metric        | Meaning                                       |
|---------------|-----------------------------------------------|
| NPS           | Net Promoter Score (user sentiment 0–10)      |
| Frequency     | How many users mentioned this                 |
| Tier Weight   | Free = 1, SMB = 2, Enterprise = 3             |

---

## 📊 Example Output

> 🧠 **Feature Cluster 3**  
> - “Mobile app crashes often”  
> - “Navigation broken on mobile”  
> - “Can't scroll properly on small screens”  
>
> Mentioned by 6 users | Avg Tier: SMB | Avg NPS: 5.3 | Score: 63.6

---

## 🚀 Try It Out

🟢 [Click here to open the app](https://feature-prioritization-dashboard-hppx2bnntk4eezccu9c2qz.streamlit.app/)

You can:
- Use the sliders on the left to change filters
- View how priorities change based on NPS, frequency, or user tier
- Download the filtered results as CSV

---

## 🧱 Tech Stack

- Frontend: Streamlit
- Clustering: Sentence-BERT + HDBSCAN
- Scoring: Custom scoring based on feedback frequency, NPS, and tier
- Summarization: TF-IDF extractive top-line summary (or example bullets)

---

## 🗂️ Files

| File                         | Purpose                                      |
|------------------------------|----------------------------------------------|
| `app.py`                     | Streamlit app source                         |
| `clustered_prioritization.csv` | Scored + summarized clusters                 |
| `expanded_customer_feedback.csv` | Full 100-entry dataset with clusters assigned |
| `README.md`                  | This file 🙂                                 |

---

## 🧪 How To Run Locally

1. Clone the repo  
2. Install dependencies:

```bash
pip install streamlit pandas
-----------------
Run the app:
streamlit run app.py
Make sure the two CSV files (clustered_prioritization.csv, expanded_customer_feedback.csv) are in the same folder.
