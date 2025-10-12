# Tax Assistant Python

Project **tax-assistant-python** — a data pipeline and machine learning module that complements the **Tax Assistant Spring** APIs.
This module aims to perform **ETL (Extract, Transform, Load)** tasks and **train ML models** to suggest tax mappings based on historical data.

---

## Project Structure

```

tax-assistant-python/
??? etl/
?   ??? extract.py
?   ??? transform.py
?   ??? load.py
?   ??? __init__.py
??? ml/
?   ??? train_model.py
?   ??? evaluate_model.py
?   ??? __init__.py
??? main.py
??? .gitignore
??? README.md

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

## Planned Technologies

* **Python**
* **Pandas** — data manipulation
* **Requests** — consuming Spring APIs
* **Scikit-Learn** — machine learning
* **Jupyter Notebook** — interactive exploration

---

## RoadMap

* Implement initial ETL flow (API extraction)
* Create data transformation pipeline
* Integrate ML models and training scripts
* Evaluate performance and metrics