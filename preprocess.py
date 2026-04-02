import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download("stopwords")
nltk.download("wordnet")

df = pd.read_csv("data/raw_jobs.csv")

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = text.lower()
    text = re.sub(r"<[^>]+>", " ", text)      # remove HTML
    text = re.sub(r"[^a-z\s]", " ", text)     # remove punctuation/numbers
    text = re.sub(r"\s+", " ", text).strip()
    words = [lemmatizer.lemmatize(w) for w in text.split() if w not in stop_words]
    return " ".join(words)

# before/after sample
print("BEFORE:\n", df["description"].iloc[0][:300])
df["clean_text"] = df["description"].astype(str).apply(clean_text)
print("\nAFTER:\n", df["clean_text"].iloc[0][:300])

df.to_csv("data/clean_jobs.csv", index=False)
print("Saved cleaned data to data/clean_jobs.csv")