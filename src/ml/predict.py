import pandas as pd

MODEL_FILE = "src/data/processed/tax_profiles.csv"

def predict_fiscal_profile(customer_id, product_id):
    df = pd.read_csv(MODEL_FILE)    
    
    # 🔧 Normalization        
    customer_id = customer_id.strip()
    product_id = product_id.strip()
    
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    df['customerId'] = df['customerId'].astype(str).str.zfill(6)
    df['productId'] = df['productId'].astype(str)
       
    results = df[
        (df['customerId'] == customer_id) &
        (df['productId'] == product_id)
    ]
        
    return results
