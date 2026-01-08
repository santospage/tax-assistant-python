import pandas as pd
from pathlib import Path


DATA_PATH = Path("src/data/processed/tax_prediction.csv")
ANY = "__ANY__"


def load_data():
    if not DATA_PATH.exists():
        print("⚠︝ tax_prediction.csv not found.")
        return pd.DataFrame()

    return pd.read_csv(DATA_PATH)


def _match(col, value):
    """
    Statistical rule:
    value matches if it is equal OR __ANY__
    """
    return (col == value) | (col == ANY)


def predict_taxes_old(
    type_customer: str,
    type_product: str,
    min_probability: float = 0.0
):
    df = load_data()

    if df.empty:
        return []

    # Normalization
    type_customer = type_customer.strip().upper()
    type_product = type_product.strip().upper()

    # 🔥 CORRECT FILTER WITH __ANY__
    filtered = df[
        _match(df["typeCustomer"], type_customer) &
        _match(df["typeProduct"], type_product)
    ]

    if filtered.empty:
        return []

    # Remove statistical noise if desired
    filtered = filtered[filtered["probability"] >= min_probability]

    if filtered.empty:
        return []

    # 🔹 Priority by level (the more specific, the better)
    level_priority = {
        "FULL_PROFILE": 1,
        "PRODUCT_UF": 2,
        "PRODUCT_ONLY": 3,
        "CUSTOMER_UF": 4,
        "GLOBAL": 5,
    }

    filtered = filtered.copy()
    filtered["level_rank"] = filtered["level"].map(level_priority).fillna(99)

    filtered = filtered.sort_values(
        by=["level_rank", "probability"],
        ascending=[True, False]
    )

    return filtered[
        [
            "taxCode",
            "descriptionTax",
            "taxAliquot",
            "probability",
            "level"
        ]
    ].to_dict(orient="records")

def predict_taxes(type_customer: str, type_product: str):
    df = pd.read_csv(DATA_PATH)

    # filtro simples (primeira vers�o)
    filtered = df[
        (df["typeCustomer"].isin([type_customer, "__ANY__"])) &
        (df["typeProduct"].isin([type_product, "__ANY__"]))
    ]

    if filtered.empty:
        return []

    # transforma em dict j� no formato do contrato
    result = []
    for _, row in filtered.iterrows():
        result.append({
            "taxCode": row["taxCode"],
            "descriptionTax": row["descriptionTax"],
            "taxAliquot": float(row["taxAliquot"]),
            "probability": float(row["probability"]),
            "level": row["level"]
        })

    return result
