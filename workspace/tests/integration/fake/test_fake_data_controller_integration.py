# workspace/tests/integration/fake/test_fake_data_controller_integration.py

import re
import pytest
from controller.fake_data_controller import FakeDataController

# 同時標記 integration + fake
pytestmark = [pytest.mark.integration, pytest.mark.fake]

def test_get_fake_user_payload_structure():
    payload = FakeDataController.get_fake_user_payload()
    assert isinstance(payload, dict)
    assert set(payload.keys()) == {"username", "password", "email"}
    assert isinstance(payload["username"], str) and payload["username"]
    assert isinstance(payload["password"], str) and payload["password"]
    assert isinstance(payload["email"], str) and "@" in payload["email"]

def test_get_fake_product_payload_structure():
    payload = FakeDataController.get_fake_product_payload()
    assert isinstance(payload, dict)
    assert set(payload.keys()) == {"title", "description", "price"}
    assert isinstance(payload["title"], str) and payload["title"]
    assert isinstance(payload["description"], str) and payload["description"]
    price = payload["price"]
    assert isinstance(price, float)
    assert price >= 0
    assert round(price, 2) == price

def test_get_fake_cart_payload_structure():
    user_id = 123
    product_id = 456
    payload = FakeDataController.get_fake_cart_payload(user_id=user_id, product_id=product_id)
    assert isinstance(payload, dict)
    assert payload["userId"] == user_id
    assert isinstance(payload["date"], str)
    assert re.match(r"^\d{4}-\d{2}-\d{2}$", payload["date"])
    assert isinstance(payload["products"], list) and len(payload["products"]) == 1
    item = payload["products"][0]
    assert item["productId"] == product_id
    quantity = item["quantity"]
    assert isinstance(quantity, int)
    assert 1 <= quantity <= 10

def test_get_fake_user_cart_bundle_structure():
    bundle = FakeDataController.get_fake_user_cart_bundle()
    assert isinstance(bundle, dict)
    assert set(bundle.keys()) == {"user", "product", "cart"}

    user = bundle["user"]
    assert set(user.keys()) == {"username", "password", "email"}
    assert "@" in user["email"]

    product = bundle["product"]
    assert set(product.keys()) == {"title", "description", "price"}

    cart = bundle["cart"]
    assert cart["userId"] == 1
    assert re.match(r"^\d{4}-\d{2}-\d{2}$", cart["date"])
    assert isinstance(cart["products"], list) and len(cart["products"]) == 1
