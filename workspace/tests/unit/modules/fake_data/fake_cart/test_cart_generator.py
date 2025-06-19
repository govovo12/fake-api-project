import pytest
import re
from workspace.modules.fake_data.fake_cart.cart_generator import generate_cart_data

pytestmark = [pytest.mark.unit, pytest.mark.fake_cart]

def test_generate_cart_data_structure():
    """
    測試 generate_cart_data() 回傳資料結構正確
    """
    data = generate_cart_data()

    assert isinstance(data, dict)
    assert "userId" in data
    assert isinstance(data["userId"], int)
    assert 1 <= data["userId"] <= 10

    assert "date" in data
    assert isinstance(data["date"], str)

    assert "products" in data
    assert isinstance(data["products"], list)
    assert 1 <= len(data["products"]) <= 5

    for product in data["products"]:
        assert isinstance(product, dict)
        assert "productId" in product
        assert isinstance(product["productId"], int)
        assert 1 <= product["productId"] <= 20

        assert "quantity" in product
        assert isinstance(product["quantity"], int)
        assert 1 <= product["quantity"] <= 5


def test_generate_cart_product_ids_unique():
    """
    測試每次產生的購物車中 productId 不重複
    """
    data = generate_cart_data()
    product_ids = [item["productId"] for item in data["products"]]
    assert len(product_ids) == len(set(product_ids))


def test_cart_date_format_is_valid():
    """
    測試產生的購物車日期格式為 YYYY-MM-DD
    """
    data = generate_cart_data()
    date = data["date"]
    assert isinstance(date, str)
    assert re.match(r"^\d{4}-\d{2}-\d{2}$", date)


def test_generate_cart_multiple_runs_validity():
    """
    測試連續多次執行 generate_cart_data() 都產出合法資料（強化信心）
    """
    for _ in range(100):
        data = generate_cart_data()
        assert isinstance(data["userId"], int)
        assert 1 <= data["userId"] <= 10
        assert isinstance(data["products"], list)
        for item in data["products"]:
            assert 1 <= item["productId"] <= 20
            assert 1 <= item["quantity"] <= 5
