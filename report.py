import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, classification_report
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/labeled_jobs.csv")
X = df["clean_text"].fillna("")
y = df["final_label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

vec = joblib.load("models/TFIDF_vectorizer.pkl")
model = joblib.load("models/TFIDF_LogReg.pkl")

X_test_vec = vec.transform(X_test)
preds = model.predict(X_test_vec)

print(classification_report(y_test, preds))

disp = ConfusionMatrixDisplay.from_predictions(y_test, preds, xticks_rotation=45)
plt.tight_layout()
plt.savefig("confusion_matrix.png")
print("Saved confusion_matrix.png")