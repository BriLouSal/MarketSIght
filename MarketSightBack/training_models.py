
from sklearn.feature_extraction.text  import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.calibration import CalibratedClassifierCV



from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json



from anthropic import AnthropicVertex
from anthropic import Anthropic

import os
import torch
from dotenv import load_dotenv

from inscriptis import get_text


from yahooquery import Ticker
import pandas as pd
from MSOAI import (
    NewsSummary,
    info_to_positivty_rating_positivety,
    info_to_positivty_rating_negative,
    info_to_positivty_rating_netural,
    news,
    gen_ai_parser,
)

load_dotenv()

DATASET_PATH = os.path.join(os.path.dirname(__file__), "sentiment_dataset_of_stocks.json")




MODEL_PATH = "sentiment_model.pkl"
VECTORIZER_PATH = "sentiment_vectorizer.pkl"
# API KEYS:

CLAUDE_API = os.getenv('CLAUDE')

client = Anthropic(api_key=CLAUDE_API)








def check_language(news: str):
    pass

# Check positivety for news, train the data
def positivity_rating_training():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)
    positive_data = dataset['Positive']
    negative_data = dataset['Negative']
    neutral_data  = dataset['Neutral']


    model_df = pd.DataFrame({
        'text': positive_data + negative_data + neutral_data,
        'label': [2]*len(positive_data) + [0]*len(negative_data) + [1]*len(neutral_data),

    })

    vectorizer = TfidfVectorizer(max_features=20000,
        ngram_range=(1,2),
        lowercase=True,
        stop_words="english",
        sublinear_tf=True,
        max_df=0.95,
        min_df=2,)
    X = vectorizer.fit_transform(model_df['text'])
    y = model_df['label']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    # Use Logistic Regression to predict the positivity rating,
    # This will be our training dataset, and we're using Claude API to get those positive
    # words for stocks, and then we'll compare it after

    # Update; Use Linear SVC, as it's apparently much less volatile and offers consistent results

    base = LinearSVC()
    model = CalibratedClassifierCV(estimator=LinearSVC(), method="sigmoid", cv=5)


    model.fit(X_train, y_train)

    accuracy = round((model.score(X_test, y_test) * 100), 2)
    print(accuracy)
    
    joblib.dump(model, MODEL_PATH)
    
    joblib.dump(vectorizer, VECTORIZER_PATH)

    return model, vectorizer


def load_dataset():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Dataset not found — run generate_universal_dataset() first.")
    
    if not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError("Vectorizer not found. Train model first.")
    
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer


# Must Finish

# Obtain positivity news form the data
def obtain_positivity(stock: str) -> dict:

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)
    positive_data = dataset.get("Positive", [])
    neutral_data = dataset.get("Neutral", []) or dataset.get("Netural", [])

    negative_data = dataset.get("Negative", [])
    

    if (neutral_data or positive_data or negative_data) is None:
        return ("Dataset incomplete: missing neutral/positive/negative samples")


    stock = stock.upper()
    news_of_stock = news(stock=stock)
    


    if not news_of_stock:
        return None, "No News is available"
    


    headline = (news_of_stock.get("Headline") or "").strip()
    html_file = (news_of_stock.get("Content") or "").strip()
    body_text = get_text(html_file) if html_file else ""
    

    model, vectorizer = load_dataset()

    docs = []

    if headline:
        docs.append(headline)

    if body_text:
        for line in gen_ai_parser(body_text): 
            if len(line) >= 25:                
                docs.append(line)
            if len(docs) >= 4:               
                break

    if not docs:
        return None, "Insufficient news content"

    # load model/vectorizer and score
    model, vectorizer = load_dataset()
    X = vectorizer.transform(docs)
    probs = model.predict_proba(X)

    classes = list(model.classes_)
    pos_i = classes.index(2) if 2 in classes else None
    neu_i = classes.index(1) if 1 in classes else None
    p_pos = probs[:, pos_i] if pos_i is not None else 0.0
    p_neu = probs[:, neu_i] if neu_i is not None else 0.0

    score = ((p_pos + 0.5 * p_neu).mean()) * 100.0
    return round(float(score), 0)   # 0–100
 

def ensure_trained():
    if not (os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH)):
        positivity_rating_training(None)

if __name__ == "__main__":
    ensure_trained()
    positivity_rating_training()


    
