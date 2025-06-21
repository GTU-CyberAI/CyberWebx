import pandas as pd
import numpy as np
import random
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# === Custom tokenizer ===
def sanitization(web):
    web = web.lower()
    token = []
    dot_token_slash = []
    raw_slash = str(web).split('/')
    for i in raw_slash:
        raw1 = str(i).split('-')
        slash_token = []
        for j in range(len(raw1)):
            raw2 = str(raw1[j]).split('.')
            slash_token += raw2
        dot_token_slash += raw1 + slash_token
    token = list(set(dot_token_slash))
    if 'com' in token:
        token.remove('com')
    return token

# === Load dataset ===
df = pd.read_csv(
    'Dataset/data_url.csv',
    delimiter=',',
    on_bad_lines=lambda x: print("Bad line skipped:", x),
    engine='python'
)
data = df.to_numpy()
random.shuffle(data)

# Separate features and labels
urls = [d[0] for d in data]
labels = [d[1] for d in data]

# === Build pipeline ===
pipeline = Pipeline([
    ('vectorizer', TfidfVectorizer(tokenizer=sanitization)),
    ('classifier', LogisticRegression(solver='lbfgs', max_iter=1000))
])

# === Train & Evaluate ===
x_train, x_test, y_train, y_test = train_test_split(urls, labels, test_size=0.2, random_state=42)
pipeline.fit(x_train, y_train)

score = pipeline.score(x_test, y_test)
print("Model accuracy: {:.2f}%".format(score * 100))

# === Save model ===
joblib.dump(pipeline, 'Classifier/url_model.pkl')
print("Model saved to Classifier/url_model.pkl ✅")
