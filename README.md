#  Phishing Detection API with Machine Learning

##  Author
Ricardo França

##  Description
This project implements a Machine Learning-based API to detect phishing domains, including advanced homoglyph (Unicode) attacks used by cybercriminals.

## Features
- Detection of phishing domains
- Homoglyph (Unicode) attack detection
- Keyword-based threat scoring
- Machine Learning classification (Random Forest)
- REST API built with FastAPI

##  Technologies
- Python
- FastAPI
- Scikit-learn
- Pandas

##  How to Run

1. Install dependencies:
2. Run the API:
3. Access:
http://127.0.0.1:8000/docs


##  Example Test

/predict?domain=gооgle.com


 This domain uses a homoglyph attack (fake Unicode characters) and should be detected as malicious.

 Este domínio utiliza um ataque de homoglifos (caracteres Unicode falsos) e deve ser identificado como malicioso.
