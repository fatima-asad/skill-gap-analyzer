from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()

vec = joblib.load("models/TFIDF_vectorizer.pkl")
model = joblib.load("models/TFIDF_LogReg.pkl")

class InputText(BaseModel):
    text: str
@app.get("/")
def home():
    return {"message": "Skill Gap API is running"}

@app.post("/predict")
def predict(data: InputText):
    X = vec.transform([data.text])
    pred = model.predict(X)[0]
    return {"prediction": pred}