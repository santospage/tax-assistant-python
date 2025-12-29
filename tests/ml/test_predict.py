import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from ml.predict import predict_fiscal_profile

def test_predict_fiscal_profile():        
    
    result = predict_fiscal_profile(
        customer_id='000094', 
        product_id='000000000000000000000000004LOC'
    )
    
    print("Resultado:", result)
    assert result is not None    

if __name__ == "__main__":
    test_predict_fiscal_profile()
