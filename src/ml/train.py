import json
from pathlib import Path
import pandas as pd


RAW_PATH = Path("src/data/raw")
PROCESSED_PATH = Path("src/data/processed")
PROCESSED_PATH.mkdir(parents=True, exist_ok=True)


def load_json(file_name):
    with open(RAW_PATH / file_name, encoding="utf-8") as f:
        return pd.DataFrame(json.load(f))


def train(df):
    results = []

    grouped = df.groupby(
        ["customerId", "productId", "taxId_y", "taxId", "descriptionTax"]
    )

    for (customer_id, product_id, tax_id_y, tax_id, description_tax), group in grouped:
        avg_aliquot = group["taxAliquot"].mean()

        results.append({
            "customerId": customer_id,
            "productId": product_id,
            "most_likely_tax": tax_id.strip(),
            "name_tax": description_tax.strip() if isinstance(description_tax, str) else None,
            "aliquote_tax": round(avg_aliquot, 4)
        })

    return pd.DataFrame(results)


def main():
    # 🔹 Carrega dados do ETL (raw)
    customers = load_json("customers.json")
    products = load_json("products.json")
    sales = load_json("sales_movements.json")
    fiscal = load_json("fiscal_movements.json")
    integrated = load_json("integrated_movements.json")

    # 🔹 Joins (igual você já fez antes)
    df = (
        sales
        .merge(customers, left_on="customerCode", right_on="customerId", how="left")
        .merge(products, left_on="productCode", right_on="productId", how="left")
        .merge(fiscal, on="companyCode", how="left")
        .merge(integrated, on="companyCode", how="left")
    )

    # 🔹 Treina
    result = train(df)

    # 🔹 Salva aprendizado
    result.to_csv(
        PROCESSED_PATH / "tax_profiles.csv",
        index=False,
        encoding="utf-8"
    )

    print("✔ ML treinado com sucesso!")
    print(result.head())


if __name__ == "__main__":
    main()
