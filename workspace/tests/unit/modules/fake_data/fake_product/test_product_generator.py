import pytest
import random
from workspace.modules.fake_data.fake_product.product_generator import generate_product_data
from workspace.config.envs.fake_product_config import CATEGORIES

pytestmark = [pytest.mark.unit, pytest.mark.fake_product]


def test_generate_product_data_success(monkeypatch):
    """
    測試 generate_product_data 成功回傳資料格式與內容
    """
    success, data, meta = generate_product_data()
    assert success is True
    assert meta is None
    assert isinstance(data, dict)
    assert "title" in data and isinstance(data["title"], str)
    assert "price" in data and (isinstance(data["price"], float) or isinstance(data["price"], int))
    assert "description" in data and isinstance(data["description"], str)
    assert "category" in data and isinstance(data["category"], str)
    assert "image" in data and isinstance(data["image"], str)


def test_generate_product_data_empty_categories(monkeypatch):
    """
    模擬 CATEGORIES 為空，測試錯誤回傳
    """
    monkeypatch.setattr("workspace.modules.fake_data.fake_product.product_generator.CATEGORIES", [])

    success, data, meta = generate_product_data()
    assert success is False
    assert data is None
    assert meta is not None
    assert meta.get("reason") == "product_generator_no_category" or meta.get("reason") == "empty_categories"
    assert "CATEGORIES 配置為空" in meta.get("message", "")



def test_generate_product_data_unexpected_exception(monkeypatch):
    """
    模擬內部例外，測試錯誤回傳
    """
    def fake_choice(_):
        raise Exception("unexpected error")

    monkeypatch.setattr("random.choice", fake_choice)

    success, data, meta = generate_product_data()
    assert success is False
    assert data is None
    assert meta is not None
    assert meta.get("reason") == "product_generator_unknown_error" or meta.get("reason") == "unexpected_exception"
    assert "unexpected error" in meta.get("message", "")
