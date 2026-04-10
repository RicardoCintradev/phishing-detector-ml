"""
Phishing Detection API with Homoglyph Analysis
Author: Ricardo França Cintra 
Description: Machine Learning system to detect phishing domains using Unicode and structural analysis.
"""

from fastapi import FastAPI
import joblib
import unicodedata
app = FastAPI()

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model_phishing.pkl")

model = joblib.load(model_path)

def detect_scripts(domain):
    scripts = set()
    for char in domain:
        try:
            name = unicodedata.name(char)
            if 'CYRILLIC' in name: scripts.add('Cyrillic')
            elif 'GREEK' in name: scripts.add('Greek')
            elif 'LATIN' in name: scripts.add('Latin')
        except:
            pass
    return len(scripts)

def check_keywords(domain):
    keywords = ['login', 'verify', 'secure', 'bank', 'update', 'support', 'account']
    return sum(1 for k in keywords if k in domain.lower())

def extract_features(domain):
    return [[
        len(domain),
        sum(c.isdigit() for c in domain),
        domain.count('-'),
        sum(ord(c) >= 128 for c in domain),
        detect_scripts(domain),
        check_keywords(domain)
    ]]

@app.get("/")
def home():
    return {"message": "API rodando "}

@app.get("/predict")
def predict(domain: str):
    features = extract_features(domain)
    prediction = model.predict(features)[0]

    return {
        "domain": domain,
        "resultado": "MALICIOSO" if prediction == 1 else "LEGÍTIMO"
    }