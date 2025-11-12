import pickle
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "expense_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")

def train_model():
    data_path = os.path.join(BASE_DIR, "..", "training_data.csv")
    df = pd.read_csv(data_path)

    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(df["note"])
    y = df["category"]

    model = MultinomialNB()
    model.fit(X, y)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)
    print("✅ Model trained and saved successfully.")

def predict_category(note):
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        train_model()

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)

    X = vectorizer.transform([note])
    prediction = model.predict(X)[0]
    return prediction
if __name__ == "__main__":
    train_model()
