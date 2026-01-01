import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../src")
    )
)

from ml.simple_tax_predictor import predict_taxes


def test_predict_taxes():
    result = predict_taxes(
        type_customer="F",
        type_product="PA"
    )

    print("\nResult:")
    for r in result:
        print(r)

    assert len(result) > 0


if __name__ == "__main__":
    test_predict_taxes()
