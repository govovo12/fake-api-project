import pytest
from workspace.controller.stub_controller import (
    get_valid_user_cart_payload,
    get_valid_user_only,
    get_cart_only
)

pytestmark = [pytest.mark.unit, pytest.mark.stub]

def test_get_valid_user_cart_payload_contains_user_and_cart():
    """回傳 dict 應含 user 與 cart 欄位"""
    result = get_valid_user_cart_payload()
    assert "user" in result
    assert "cart" in result
    assert isinstance(result["user"], dict)
    assert isinstance(result["cart"], dict)
    assert "username" in result["user"]
    assert "products" in result["cart"]

def test_get_valid_user_only_returns_user_dict():
    """get_valid_user_only 應回傳正確 user dict"""
    user = get_valid_user_only()
    assert isinstance(user, dict)
    assert user["username"] == "johnd"
    assert user["password"] == "m38rmF$"

def test_get_cart_only_returns_cart_dict():
    """get_cart_only 可傳入 user_id 並正確產生 cart dict"""
    cart = get_cart_only(user_id=99)
    assert isinstance(cart, dict)
    assert cart["userId"] == 99
    assert "products" in cart
