# Tax Assistant Python

Project **tax-assistant-python** — a data pipeline and machine learning module that complements the **Tax Assistant Spring** APIs.
This module aims to perform **ETL (Extract, Transform, Load)** tasks and **train ML models** to suggest tax mappings based on historical data.

---

## Project Structure

```

tax-assistant-python
├── src
│   ├── etl
│   │   ├── __init__.py
│   │   ├── extract.py
│   │   └── auth.py
│   ├── ml
│   │   ├── __init__.py
│   │   ├── simple_tax_predictor.py
│   │   ├── train_prediction.py
│   │   └── train_taxes.py
│   ├── __init__.py
│   └── main.py
├── tests
│   ├── etl
│   │   ├── test_extract.py
│   │   └── test_auth.py
│   ├── ml
│   │   ├── test_simple_tax_predictor.py
│   │   └── test_train_taxes.py
│   └── test_main.py
├── .env
├── .gitignore
├── pytest.ini
└── README.md

---

## Goal

The purpose of this module is to:

* Extract data from **Spring Boot** APIs
* Transform and consolidate fiscal and tax-related information
* Train **Machine Learning (Scikit-Learn)** models to suggest tax mappings based on historical cases
* Serve as a base for analysis and future intelligent automations

---

## Development Environment

**Prerequisites:**

* Python 3.7+
* Virtualenv configured

**Create virtual environment (Windows - PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## Technologies Used

**Python**
**Pandas** — data manipulation
**Requests** — consuming Spring APIs
**Scikit-Learn** — machine learning
**Pytest** — automated testing
**Jupyter Notebook** — interactive exploration

---

## Notes

The ML models are trained using real historical tax data
Outputs are probabilistic, not absolute
The quality of predictions depends directly on data volume and consistency
The module is designed to evolve incrementally alongside the Spring APIs

---

## Return Example

The `predict_taxes` function returns a **list of tax suggestions**, each one representing
a possible tax mapping with an associated probability and confidence level.

```json
[
  {
    "taxCode": "IBSMUN",
    "descriptionTax": "IBS MUNICIPAL - Imposto sobre Bens e Serviços Municipal.",
    "taxAliquot": 0.0,
    "probability": 0.2,
    "level": "FULL_PROFILE"
  },
  {
    "taxCode": "IBSMUN",
    "descriptionTax": "IBS MUNICIPAL - Imposto sobre Bens e Serviços Municipal.",
    "taxAliquot": 0.0,
    "probability": 0.2,
    "level": "PRODUCT_UF"
  },
  {
    "taxCode": "IBSMUN",
    "descriptionTax": "IBS MUNICIPAL - Imposto sobre Bens e Serviços Municipal.",
    "taxAliquot": 0.0,
    "probability": 0.2,
    "level": "PRODUCT_ONLY"
  },
  {
    "taxCode": "IBSMUN",
    "descriptionTax": "IBS MUNICIPAL - Imposto sobre Bens e Serviços Municipal.",
    "taxAliquot": 0.0,
    "probability": 0.2,
    "level": "CUSTOMER_UF"
  },
  {
    "taxCode": "IBSMUN",
    "descriptionTax": "IBS MUNICIPAL - Imposto sobre Bens e Serviços Municipal.",
    "taxAliquot": 0.0,
    "probability": 0.2,
    "level": "GLOBAL"
  }
]

### Confidence Levels

- `FULL_PROFILE` – Customer, product, and UF matched
- `PRODUCT_UF` – Product and UF matched
- `PRODUCT_ONLY` – Only product matched
- `CUSTOMER_UF` – Customer and UF matched
- `GLOBAL` – No specific match, historical global data

