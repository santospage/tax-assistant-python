import pandas as pd

MODEL_FILE = "src/data/processed/tax_profiles.csv"

def predict_fiscal_profile(customer_id, product_id):
    df = pd.read_csv(MODEL_FILE)

    # 🔧 NORMALIZAÇÃO
    df["customerId"] = df["customerId"].astype(str).str.lstrip("0")
    customer_id = customer_id.lstrip("0")

    df["productId"] = df["productId"].astype(str).str.lstrip("0")
    product_id = product_id.lstrip("0")       

    customer_id = customer_id.strip()
    product_id = product_id.strip()

    filtered = df[
        (df["customerId"] == customer_id) &
        (df["productId"] == product_id)
    ]

    results = []
    for _, row in filtered.iterrows():
        results.append({
            "most_likely_tax": row["most_likely_tax"],
            "name_tax": row["name_tax"],
            "aliquote_tax": row["aliquote_tax"]
        })
        

    return results
