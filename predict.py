import joblib
import pandas as pd

# choose TFIDF or BOW
VEC_PATH = "models/TFIDF_vectorizer.pkl"
MODEL_PATH = "models/TFIDF_LogReg.pkl"  # we’ll save this next

def predict_label(text):
    vec = joblib.load(VEC_PATH)
    model = joblib.load(MODEL_PATH)
    X = vec.transform([text])
    return model.predict(X)[0]

if __name__ == "__main__":
    skills = input("Enter your skills: ")
    label = predict_label(skills)
    print("Predicted class:", label)