import requests
import pandas as pd

API_URL = "https://remoteok.com/api"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_remoteok_api():
    res = requests.get(API_URL, headers=headers)
    res.raise_for_status()
    data = res.json()

    # first item is metadata, skip it
    jobs = data[1:]

    rows = []
    for job in jobs:
        rows.append({
            "id": job.get("id"),
            "date": job.get("date"),
            "company": job.get("company", ""),
            "position": job.get("position", ""),
            "tags": ", ".join(job.get("tags", [])),
            "location": job.get("location", ""),
            "salary_min": job.get("salary_min", 0),
            "salary_max": job.get("salary_max", 0),
            "description": job.get("description", ""),
            "url": job.get("url", "")
        })

    df = pd.DataFrame(rows)

    # clean empty descriptions
    df = df[df["description"].str.len() > 50]

    df.to_csv("data/raw_jobs.csv", index=False)
    print("Saved", len(df), "jobs to data/raw_jobs.csv")

if __name__ == "__main__":
    scrape_remoteok_api()