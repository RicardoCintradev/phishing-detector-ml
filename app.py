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
# FUNÇÕES DE EXPLICAÇÃO
# =========================

def detectar_alfabetos(texto):
    alfabetos = set()

    for char in texto:
        nome = unicodedata.name(char, "")
        
        if "CYRILLIC" in nome:
            alfabetos.add("cirilico")
        elif "GREEK" in nome:
            alfabetos.add("grego")
        elif "LATIN" in nome:
            alfabetos.add("latino")

    return alfabetos


def gerar_explicacao(url):
    explicacoes = []
    
    alfabetos = detectar_alfabetos(url)

    if len(alfabetos) > 1:
        explicacoes.append(f"Mistura de alfabetos: {', '.join(alfabetos)}")

    if "xn--" in url:
        explicacoes.append("Uso de Punycode (possível spoofing)")

    if any(ord(c) > 127 for c in url):
        explicacoes.append("Presença de caracteres Unicode incomuns")

    return explicacoes

# =========================
# ENDPOINT PRINCIPAL
# =========================

@app.post("/predict")
def predict(data: URLRequest):
    url = data.url
    
    pred = model.predict([url])[0]
    prob = model.predict_proba([url])[0].max()

    explicacoes = gerar_explicacao(url)

    return {
        "url": url,
        "resultado": "phishing" if pred == 1 else "legitimo",
        "probabilidade": float(prob),
        "explicacao": explicacoes
    }

# =========================
# ROTA TESTE
# =========================

@app.get("/")
def home():
    return {"mensagem": "API de detecção de phishing ativa "}