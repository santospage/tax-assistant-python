import os
import pandas as pd
from pathlib import Path


RAW_PATH = Path("src/data/raw")
PROCESSED_PATH = Path("src/data/processed")
PROCESSED_PATH.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------
# UTIL
# -------------------------------------------------
def load_json(filename: str) -> pd.DataFrame:
    path = RAW_PATH / filename

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if path.stat().st_size == 0:
        raise ValueError(f"Empty file: {path}")

    with open(path, "r", encoding="utf-8") as f:
        first = f.read(1)
        f.seek(0)

        if first == "{":
            return pd.read_json(f, lines=True)

        return pd.read_json(f)


def normalize_strings(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()
    return df


# -------------------------------------------------
# TRAIN
# -------------------------------------------------
def train(df: pd.DataFrame) -> pd.DataFrame:
    """
    Train fiscal probabilities at multiple levels (robust)
    """

    df = df.dropna(subset=["taxCode", "descriptionTax", "taxAliquot"])

    profile_sets = {
        "FULL_PROFILE": [
            "typeCustomer",
            "ufCustomer",
            "cityCustomer",
            "countryCustomer",
            "nationalRegistryCustomer",
            "typeProduct",
            "specifingCodeST",
            "mercosulExtNomenclature",
        ],
        "PRODUCT_UF": [
            "typeProduct",
            "specifingCodeST",
            "mercosulExtNomenclature",
            "ufCustomer",
        ],
        "PRODUCT_ONLY": [
            "typeProduct",
            "specifingCodeST",
            "mercosulExtNomenclature",
        ],
        "CUSTOMER_UF": [
            "typeCustomer",
            "ufCustomer",
        ],
        "GLOBAL": []  # handled separately
    }

    results = []

    for level, cols in profile_sets.items():

        temp = df.copy()

        # -------------------------
        # CASE GLOBAL (NO PROFILE)
        # -------------------------
        if not cols:
            grouped = (
                temp
                .groupby(
                    ["taxCode", "taxId", "descriptionTax", "taxAliquot"]
                )
                .size()
                .reset_index(name="occurrences")
            )

            total = grouped["occurrences"].sum()
            grouped["total"] = total
            grouped["probability"] = (
                grouped["occurrences"] / total
            ).round(4)

            grouped["level"] = level

            # Fill profile columns with ANY
            for col in profile_sets["FULL_PROFILE"]:
                grouped[col] = "__ANY__"

            results.append(grouped)
            continue

        # -------------------------
        # OTHER LEVELS
        # -------------------------
        for c in cols:
            temp[c] = temp[c].fillna("__ANY__")

        group_cols = cols + [
            "taxCode",
            "taxId",
            "descriptionTax",
            "taxAliquot",
        ]

        grouped = (
            temp
            .groupby(group_cols)
            .size()
            .reset_index(name="occurrences")
        )

        totals = (
            grouped
            .groupby(cols)["occurrences"]
            .sum()
            .reset_index(name="total")
        )

        result = grouped.merge(totals, on=cols, how="left")

        result["probability"] = (
            result["occurrences"] / result["total"]
        ).round(4)

        result["level"] = level

        for col in profile_sets["FULL_PROFILE"]:
            if col not in result.columns:
                result[col] = "__ANY__"

        results.append(result)

    final = pd.concat(results, ignore_index=True)

    return final.sort_values(
        ["level", "probability", "occurrences"],
        ascending=[True, False, False]
    )


# -------------------------------------------------
# MAIN
# -------------------------------------------------
def main():
    customers = load_json("customers.json")
    products = load_json("products.json")
    sales = load_json("sales_movements.json")
    fiscal = load_json("fiscal_movements.json")
    integrated = load_json("integrated_movements.json")

    customers = normalize_strings(customers)
    products = normalize_strings(products)
    sales = normalize_strings(sales)
    fiscal = normalize_strings(fiscal)
    integrated = normalize_strings(integrated)

    df = (
        sales
        .merge(
            customers,
            left_on=["companyCode", "customerCode"],
            right_on=["companyCode", "customerId"],
            how="left"
        )
        .merge(
            products,
            left_on=["companyCode", "productCode"],
            right_on=["companyCode", "productId"],
            how="left"
        )
        .merge(
            fiscal,
            left_on=["companyCode", "taxId"],
            right_on=["companyCode", "relationshipId"],
            how="left",
            suffixes=("", "_fiscal")
        )
        .merge(
            integrated,
            left_on=["companyCode", "taxCode"],
            right_on=["companyCode", "taxId"],
            how="left",
            suffixes=("", "_integrated")
        )
    )

    print(f"Total number of rows after joins: {len(df)}")

    result = train(df)

    output = PROCESSED_PATH / "tax_prediction.csv"
    result.to_csv(output, index=False, encoding="utf-8")
    
    print(result.head(10))


if __name__ == "__main__":
    main()
