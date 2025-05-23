# DPDzero Data Ops Assignment

This repository contains datasets and analysis scripts for the Data Operations Assignment submitted to **DPDzero**.

## Files Included

- `call_logs.csv` — Call records with agent and call-related info.
- `agent_roster.csv` — Agent details including names and login info.
- `disposition_summary.csv` — Disposition outcomes of calls made.
- `data_ops_analysis.py` — Python script used for data validation, merging, feature engineering, and final reporting.
- `agent_performance_summary.csv` — Final output file with daily performance metrics for each agent.

##  Summary of Work

- ✅ **Data Validation:** Checked and removed missing and duplicate records.
- ✅ **Data Merging:** Combined all datasets using `LEFT JOIN` to retain important call data.
- ✅ **Feature Engineering:** Calculated total calls, completed calls, connect rate, presence flag, etc.
- ✅ **Reporting:** Created a performance summary CSV and generated a report message.

##  Key Metrics

- **Connect Rate** = Completed Calls / Total Calls  
- **Presence Flag** = 1 if agent logged in, else 0  
- **Average Duration** = Mean call duration

## 🛠️ Tools Used

- Python (Pandas, NumPy)
- Jupyter Notebook / VS Code
  

##  About Me

I'm  graduate with a passion for data and analytics, actively applying for data-related roles. This project reflects my ability to clean, transform, and report real-world data in a structured and professional way.

---


