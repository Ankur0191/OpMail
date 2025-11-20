# classifier/train_model.py
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from joblib import dump, load
import sys

DATA_PATH = "classifier/training_data.json"
MODEL_PATH = "classifier/model.joblib"
VECT_PATH = "classifier/vectorizer.joblib"

def load_data(path=DATA_PATH):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    texts = []
    labels = []
    for item in data:
        texts.append(item["text"])
        labels.append(item["label"])
    return texts, labels

def train():
    texts, labels = load_data()
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)
    pipeline = make_pipeline(TfidfVectorizer(max_df=0.9, min_df=1, ngram_range=(1,2)), MultinomialNB())
    pipeline.fit(X_train, y_train)
    score = pipeline.score(X_test, y_test)
    dump(pipeline, MODEL_PATH)
    print("Saved model to", MODEL_PATH)
    print("Test accuracy:", score)

if __name__ == "__main__":
    train()
