"""
Phishing Detection API with Homoglyph Analysis
Author: Ricardo França Cintra 
Description: Machine Learning system to detect phishing domains using Unicode and structural analysis.
"""


from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os
import unicodedata
import numpy as np

# =========================
# INICIALIZAÇÃO
# =========================

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model_phishing.pkl")

model = joblib.load(model_path)

# =========================
# MODELO DE ENTRADA
# =========================

class URLRequest(BaseModel):
    url: str

# =========================
# FEATURES (KAGGLE)
# =========================

def is_non_ascii(domain):
    return sum(ord(c) > 127 for c in domain)

def detect_scripts(domain):
    scripts = set()
    
    for char in domain:
        try:
            name = unicodedata.name(char)
            if "LATIN" in name:
                scripts.add("latin")
            elif "CYRILLIC" in name:
                scripts.add("cyrillic")
            elif "GREEK" in name:
                scripts.add("greek")
        except:
            pass
    
    return len(scripts)

def has_mixed_scripts(domain):
    return 1 if detect_scripts(domain) > 1 else 0

def extract_features(domain):
    return [
        len(domain),
        sum(c.isdigit() for c in domain),
        is_non_ascii(domain),
        domain.count('-'),
        has_mixed_scripts(domain)
    ]

# =========================
# EXPLICAÇÃO
# =========================

def gerar_explicacao(url):
    explicacoes = []
    
    if has_mixed_scripts(url):
        explicacoes.append("Mistura de alfabetos detectada")

    if is_non_ascii(url):
        explicacoes.append("Caracteres Unicode incomuns")

    if "xn--" in url:
        explicacoes.append("Uso de Punycode (possível spoofing)")

    return explicacoes

# =========================
# ENDPOINT
# =========================

@app.post("/predict")
def predict(data: URLRequest):
    url = data.url
    
    features = np.array(extract_features(url)).reshape(1, -1)

    pred = model.predict(features)[0]
    prob = model.predict_proba(features)[0].max()

    explicacoes = gerar_explicacao(url)

    return {
        "url": url,
        "resultado": "phishing" if pred == 1 else "legitimo",
        "probabilidade": float(prob),
        "explicacao": explicacoes
    }

# =========================
# TESTE
# =========================

@app.get("/")
def home():
    return {"mensagem": "API FINAL "}