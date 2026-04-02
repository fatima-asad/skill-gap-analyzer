import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

df = pd.read_csv("data/labeled_jobs.csv")

X = df["clean_text"].fillna("")
y = df["final_label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

tfidf = TfidfVectorizer(max_features=5000)
X_train_vec = tfidf.fit_transform(X_train)
X_test_vec = tfidf.transform(X_test)

model = LogisticRegression(max_iter=2000)
model.fit(X_train_vec, y_train)

preds = model.predict(X_test_vec)
print(classification_report(y_test, preds))

# save both
joblib.dump(tfidf, "models/TFIDF_vectorizer.pkl")
joblib.dump(model, "models/TFIDF_LogReg.pkl")

print("Saved models in /models")