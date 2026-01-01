import json
import os
from pathlib import Path
import pandas as pd


RAW_PATH = Path("src/data/raw")
PROCESSED_PATH = Path("src/data/processed")
PROCESSED_PATH.mkdir(parents=True, exist_ok=True)


def load_json(filename):
    path = RAW_PATH / filename

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if path.stat().st_size == 0:
        raise ValueError(f"Empty file: {path}")

    with open(path, "r", encoding="utf-8") as f:
        first_char = f.read(1)
        f.seek(0)

        # NDJSON
        if first_char == "{":
            return pd.read_json(f, lines=True)

        # Standard JSON (list or object)
        return pd.read_json(f)


def train(df):
    """
    Returns ALL taxes by customer + product
    """

    required = [
        "customerId",
        "productId",
        "taxCode",
        "descriptionTax",
        "taxAliquot",
    ]

    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Missing columns: {missing}")

    result = (
        df
        .dropna(subset=["taxCode", "descriptionTax"])
        .groupby(
            ["customerId", "productId", "taxCode", "descriptionTax"]
        )
        .agg(
            occurrences=("taxCode", "count"),
            aliquote_tax=("taxAliquot", "mean"),
        )
        .reset_index()
    )

    result["aliquote_tax"] = result["aliquote_tax"].round(4)

    return result


def main():
   # 🔹 Load ETL data (raw)
    customers = load_json("customers.json")
    products = load_json("products.json")
    sales = load_json("sales_movements.json")
    fiscal = load_json("fiscal_movements.json")
    integrated = load_json("integrated_movements.json")


    df = (
        sales

        # sales → customers
        .merge(
            customers,
            left_on="customerCode",
            right_on="customerId",
            how="left",
            suffixes=("", "_customer"),
            validate="m:1"
        )

        # sales → products
        .merge(
            products,
            left_on=["companyCode", "productCode"],
            right_on=["companyCode", "productId"],
            how="left",
            suffixes=("", "_product"),
            validate="m:m"
        )        

        # sales → fiscal
        .merge(
            fiscal,
            left_on="taxId",
            right_on="relationshipId",
            how="left",
            suffixes=("", "_fiscal"),
            validate="m:m"
        )        
        
        # fiscal → integrated
        .merge(
            integrated,
            left_on=["companyCode", "taxCode"],
            right_on=["companyCode", "taxId"],
            how="left",
            suffixes=("", "_integrated"),
            validate="m:m"
        )        
    )    
    
    
    # 🔹 Train
    result = train(df)

    # 🔹 Save training
    result.to_csv(
        PROCESSED_PATH / "tax_profiles.csv",
        index=False,
        encoding="utf-8"
    )

    print("✔ ML trained successfully!")
    print(result.head())


if __name__ == "__main__":
    main()
