import pytest

pytestmark = [pytest.mark.unit, pytest.mark.fixture]

def tool(func):
    func.is_tool = True
    return func

@pytest.fixture
@tool
def stub_cart_payload():
    """產生購物車 payload dict（for stub/mock）[TOOL]"""
    return {
        "userId": 5,
        "date": "2022-05-05",
        "products": [
            {"productId": 1, "quantity": 2},
            {"productId": 2, "quantity": 1}
        ]
    }
