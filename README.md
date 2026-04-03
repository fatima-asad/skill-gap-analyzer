# 🦆 Skill-Gap Analyzer AI

A modern, serverless web application that analyzes user-inputted skills to predict their current market demand and compensation level in real-time. Built specifically to be hosted on Vercel.

## 🌟 How It Works

The application operates fundamentally on a **Live Web Scraping / API Architecture**, abandoning static, biased Machine Learning models in favor of real-time market data.

Here is the exact step-by-step workflow:

### 1. The Frontend (User Interface)
- **Location:** `index.html` (served at the root `/`).
- **Functionality:** Users land on a beautiful, glassmorphic UI featuring a pink color palette and an AI Donald Duck assistant.
- **Action:** When a user types a skill (e.g., "Python Developer") and clicks "Analyze Now", the frontend runs JavaScript to seamlessly make an asynchronous `POST` request to the backend with the payload: `{"text": "Python Developer"}`.

### 2. The Backend (Real-Time Scraping)
- **Location:** `api/index.py` (FastAPI Serverless Function).
- **Execution:** Vercel routes the `/api/predict` fetch request to this Python script.
- **Live Data Fetch:** The backend immediately strips and formats the requested skill, then sends an HTTP request to `https://remoteok.com/api?tags=skill` pretending to be a real browser (`User-Agent` configured).
- **Processing:** 
  - **Demand Check:** The AI counts the total number of live, active jobs returned for that specific skill. If there are 3 or more jobs currently hiring for it, it classifies it as **"High Demand"**.
  - **Pay Check:** The AI scrapes the `salary_max` field of every fetched job and calculates the average. If the average salary is above $70,000/yr, it classifies it as **"High Pay"**.
- **Response:** The backend formats the prediction (e.g. `High Demand, Low Pay (12 jobs scraped)`) and returns it securely to the frontend.

### 3. Result Display
- The frontend receives the JSON response from the server, hides the loading spinner, and gracefully animatingly displays the accurate prediction back to the user!

---

## 🚀 Deployment (Vercel)
The project runs strictly through zero-configuration on **Vercel** with the explicit rules defined in `vercel.json`:
- All requests targeting `/` trigger `@vercel/static` to serve `index.html`.
- All requests targeting `/api/*` trigger `@vercel/python` to execute the FastAPI backend, utilizing dependencies cached from `requirements.txt`.

## 🛠️ Local Development
To run this application locally and test both the UI and the Backend, execute:
```bash
python local_server.py
```
And navigate your browser to `http://127.0.0.1:8000`.
