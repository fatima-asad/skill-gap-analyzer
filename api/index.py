import os
import requests
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

class InputText(BaseModel):
    text: str

@app.get("/api")
def home():
    return {"message": "Skill Gap API is running"}

@app.post("/api/predict")
def predict(data: InputText):
    skill = data.text.strip().lower()
    if not skill:
        return {"prediction": "Skill cannot be empty"}
        
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        res = requests.get(f"https://remoteok.com/api?tags={skill}", headers=headers, timeout=5)
        
        if res.status_code == 200:
            jobs = res.json()
            if len(jobs) > 0 and 'legal' in jobs[0]:
                jobs = jobs[1:]
        else:
            jobs = []
            
    except Exception as e:
        print("API Error:", e)
        return {"prediction": "Scraping failed: API unreachable"}

    if not jobs:
        return {"prediction": "Low Demand, Low Pay (0 live jobs found)"}

    job_count = len(jobs)
    salaries = [j.get('salary_max', 0) for j in jobs if j.get('salary_max', 0) > 0]
    avg_salary = np.mean(salaries) if salaries else 0

    demand = "High Demand" if job_count >= 3 else "Low Demand"
    pay = "High Pay" if avg_salary >= 70000 else "Low Pay"

    return {"prediction": f"{demand}, {pay} ({job_count} jobs scraped)"}
