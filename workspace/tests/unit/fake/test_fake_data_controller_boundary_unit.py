# workspace/tests/unit/fake/test_fake_data_controller_boundary_unit.py

import re
import pytest
from controller.fake_data_controller import FakeDataController

# 新增 fake 標記
pytestmark = pytest.mark.fake

class TestFakeDataControllerBoundary:

    def test_cart_quantity_min_max(self, monkeypatch):
        # quantity = 1
        monkeypatch.setattr(
            "workspace.utils.fake.fake_helper.faker.random_int",
            lambda *_args, **_kwargs: 1
        )
        cart = FakeDataController.get_fake_cart_payload(user_id=1, product_id=1)
        assert cart["products"][0]["quantity"] == 1

        # quantity = 10
        monkeypatch.setattr(
            "workspace.utils.fake.fake_helper.faker.random_int",
            lambda *_args, **_kwargs: 10
        )
        cart = FakeDataController.get_fake_cart_payload(user_id=1, product_id=1)
        assert cart["products"][0]["quantity"] == 10

    @pytest.mark.parametrize("value", [0.00, 9999.99])
    def test_product_price_min_max(self, monkeypatch, value):
        monkeypatch.setattr(
            "workspace.utils.fake.fake_helper.faker.pyfloat",
            lambda *_args, **_kwargs: value
        )
        product = FakeDataController.get_fake_product_payload()
        price = product["price"]
        assert isinstance(price, float)
        assert price == pytest.approx(value, rel=1e-6)
        assert round(price, 2) == price

    def test_email_strict_format(self):
        payload = FakeDataController.get_fake_user_payload()
        email = payload["email"]
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        assert re.match(pattern, email), f"Email 格式不合法: {email}"
