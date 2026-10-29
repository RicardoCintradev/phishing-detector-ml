# Phishing Detection API

API em Python e FastAPI para identificar domínios suspeitos usando Machine Learning e análise de caracteres Unicode.

## Tecnologias

- Python
- FastAPI
- Scikit-learn
- Pandas

## Instalação e execução

```bash
git clone https://github.com/RicardoCintradev/phishing-detector-ml.git
cd phishing-detector-ml
pip install -r requirements.txt
uvicorn app:app --reload
```

A documentação interativa fica disponível em:

```text
http://127.0.0.1:8000/docs
```

## Endpoint

### `POST /predict`

Recebe uma URL em formato JSON e informa se ela parece legítima ou maliciosa.

**Requisição:**

```json
{
  "url": "https://gооgle.com"
}
```

**Exemplo com cURL:**

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"url":"https://gооgle.com"}'
```

**Resposta:**

```json
{
  "url": "https://gооgle.com",
  "resultado": "phishing",
  "probabilidade": 1.0,
  "explicacao": "Mistura de alfabetos detectada, Caracteres Unicode incomuns"
}
```

O domínio do exemplo usa caracteres Unicode semelhantes aos de `google.com`, caracterizando um possível ataque de homoglifos.

