# workspace/tests/unit/fake/test_fake_data_controller_unit.py

import re
import pytest
from controller.fake_data_controller import FakeDataController

# 新增 fake 標記
pytestmark = pytest.mark.fake

def test_generate_user_payload_contains_expected_keys():
    payload = FakeDataController.get_fake_user_payload()
    assert set(payload.keys()) == {"username", "password", "email"}
    assert isinstance(payload["email"], str) and "@" in payload["email"]

def test_generate_product_payload_contains_expected_keys():
    payload = FakeDataController.get_fake_product_payload()
    assert set(payload.keys()) == {"title", "description", "price"}
    price = payload["price"]
    assert isinstance(price, float) and price >= 0 and round(price, 2) == price

def test_generate_cart_payload_contains_user_and_products():
    user_id, product_id = 42, 99
    payload = FakeDataController.get_fake_cart_payload(user_id=user_id, product_id=product_id)
    assert payload["userId"] == user_id
    assert re.match(r"^\d{4}-\d{2}-\d{2}$", payload["date"])
    products = payload["products"]
    assert isinstance(products, list) and len(products) == 1
    item = products[0]
    assert item["productId"] == product_id
    assert isinstance(item["quantity"], int) and 1 <= item["quantity"] <= 10
