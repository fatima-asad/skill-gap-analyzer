import pandas as pd
import numpy as np

df = pd.read_csv("data/clean_jobs.csv")

# ---- Demand score ----
all_tags = df["tags"].fillna("").str.lower().str.split(", ")
tags_flat = [t for tags in all_tags for t in tags if t]
tag_freq = pd.Series(tags_flat).value_counts()

def demand_label(tags):
    tags = [t for t in str(tags).lower().split(", ") if t]
    if not tags:
        return "low"
    avg = np.mean([tag_freq.get(t, 0) for t in tags])
    return "high" if avg >= tag_freq.quantile(0.60) else "low"

# ---- Pay score ----
salary = df["salary_max"].fillna(0)

# if salary is missing (0), use description length as proxy
salary_proxy = salary.copy()
salary_proxy[salary_proxy == 0] = df["description"].str.len()

salary_threshold = salary_proxy.quantile(0.60)

def pay_label(s, desc_len):
    value = s if s > 0 else desc_len
    return "high" if value >= salary_threshold else "low"

df["demand"] = df["tags"].apply(demand_label)
df["pay"] = df.apply(lambda r: pay_label(r["salary_max"], len(str(r["description"]))), axis=1)

def combine(d, p):
    if d=="high" and p=="high": return "HighDemand_HighPay"
    if d=="high" and p=="low": return "HighDemand_LowPay"
    if d=="low" and p=="high": return "LowDemand_HighPay"
    return "LowDemand_LowPay"

df["final_label"] = df.apply(lambda r: combine(r["demand"], r["pay"]), axis=1)

# ---- Fix rare classes (merge if <2 samples) ----
counts = df["final_label"].value_counts()
rare = counts[counts < 2].index.tolist()
if rare:
    print("Merging rare classes:", rare)
    df.loc[df["final_label"].isin(rare), "final_label"] = "HighDemand_LowPay"

print(df["final_label"].value_counts())
df.to_csv("data/labeled_jobs.csv", index=False)
print("Saved: data/labeled_jobs.csv")