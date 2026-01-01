import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from ml.predict import predict_fiscal_profile

def test_predict_fiscal_profile():        
    
    result = predict_fiscal_profile(
        customer_id='000001', 
        product_id='ESTSE0000000000000000000001303'
    )
    
    print("Result:", result)
    assert result is not None    

if __name__ == "__main__":
    test_predict_fiscal_profile()
