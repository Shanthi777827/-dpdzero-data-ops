import pandas as pd
import numpy as np

# Step 1: Load Data
call_logs = pd.read_csv(r"C:\Users\steph\OneDrive\Documents\Desktop\DPDzero Data Ops Assignment\call_logs.csv", parse_dates=["call_date"])
agent_roster = pd.read_csv(r"C:\Users\steph\OneDrive\Documents\Desktop\DPDzero Data Ops Assignment\agent_roster.csv")
disposition_summary = pd.read_csv(r"C:\Users\steph\OneDrive\Documents\Desktop\DPDzero Data Ops Assignment\disposition_summary.csv", parse_dates=["call_date"])

# Step 2: Validation
def validate(df, cols):
    missing = df[df[cols].isnull().any(axis=1)]
    duplicates = df[df.duplicated()]
    return missing, duplicates

missing_calls, dup_calls = validate(call_logs, ["call_date", "agent_id", "org_id"])
missing_disp, dup_disp = validate(disposition_summary, ["call_date", "agent_id", "org_id"])
missing_agent, dup_agent = validate(agent_roster, ["agent_id", "org_id"])

# Drop invalids
call_logs.drop(missing_calls.index.union(dup_calls.index), inplace=True)
disposition_summary.drop(missing_disp.index.union(dup_disp.index), inplace=True)
agent_roster.drop(missing_agent.index.union(dup_agent.index), inplace=True)

# Step 3: Merge Data

# Handling mismatches:
# - Used LEFT JOIN to retain all call records even if no matching disposition or roster entry is found.
# - Missing values in disposition/login_time indicate mismatches; handled them using fillna or conditional logic.
# - This ensures no data loss from the call_logs base.

merged = call_logs.merge(agent_roster, on=["agent_id", "org_id"], how="left")
merged = merged.merge(disposition_summary, on=["agent_id", "org_id", "call_date"], how="left")

# Step 4: Feature Engineering
summary = merged.groupby(["agent_id", "call_date"]).agg(
    total_calls=("call_id", "count"),
    unique_loans=("installment_id", pd.Series.nunique),
    completed_calls=("status", lambda x: (x == "completed").sum()),
    avg_duration=("duration", "mean"),
    presence=("login_time", lambda x: 1 if x.notnull().any() else 0)
                  ).reset_index()

summary["connect_rate"] = (summary["completed_calls"] / summary["total_calls"]).round(2)
summary["avg_duration"] = summary["avg_duration"].round(2)

# Step 5: Merge Agent Name
summary = summary.merge(agent_roster, on="agent_id", how="left")
summary["agent_name"] = summary["users_first_name"] + " " + summary["users_last_name"]

# Step 6: Save CSV
summary.to_csv("agent_performance_summary.csv", index=False)

# Step 7: Slack-Style Summary
report_date = summary["call_date"].max().strftime("%Y-%m-%d")
top_agent = summary.loc[summary["connect_rate"].idxmax()]
active_agents = summary["presence"].sum()
avg_dur = summary["avg_duration"].mean().round(2)

print(f"""Agent Summary for {report_date}
Top Performer   : {top_agent['agent_name']} ({int(top_agent['connect_rate'] * 100)}% connect rate)
Active Agents   : {int(active_agents)}
Avg Call Duration: {avg_dur} min""")

