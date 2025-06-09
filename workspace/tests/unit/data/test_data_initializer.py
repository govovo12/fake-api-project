import pytest
import json
from pathlib import Path

from workspace.utils.data.data_initializer import (
    generate_empty_data,
    write_empty_data_file
)

# ✅ 單元測試標記：屬於 unit 測試 + 資料模組 data 類別
pytestmark = [pytest.mark.unit, pytest.mark.data]


# 測試：產生空使用者資料
def test_generate_empty_data_user():
    data = generate_empty_data("user")
    assert isinstance(data, dict)
    assert set(data.keys()) == {"uuid", "name", "email"}
    assert data["uuid"] == ""


# 測試：產生空商品資料
def test_generate_empty_data_product():
    data = generate_empty_data("product")
    assert isinstance(data, dict)
    assert set(data.keys()) == {"uuid", "name", "price"}
    assert data["price"] == 0


# 測試：不支援的 kind 應傳回空 dict
def test_generate_empty_data_unknown():
    data = generate_empty_data("unknown")
    assert data == {}  # ✅ 不支援的 kind 傳空 dict


# 測試：正常寫入空資料檔案
def test_write_empty_data_file_success(tmp_path):
    path = tmp_path / "product.json"
    success, meta = write_empty_data_file(path, "product")

    # ✅ 成功應回傳 True, 且 meta 為空 dict
    assert success is True
    assert meta == {}

    # ✅ 檔案內容應為空 JSON（符合目前工具模組預設）
    content = json.loads(path.read_text(encoding="utf-8"))
    assert content == {}  # ✅ 這是目前工具模組寫入的內容


# 測試：模擬 save_json 寫檔失敗，應回傳錯誤 meta
def test_write_empty_data_file_fail(monkeypatch, tmp_path):
    path = tmp_path / "fail.json"

    # ✅ patch save_json 讓它模擬失敗
    monkeypatch.setattr(
        "workspace.utils.data.data_initializer.save_json",
        lambda path, data: False
    )

    success, meta = write_empty_data_file(path, "user")

    # ✅ 預期應回傳 False，且 reason 為 save_failed_user
    assert success is False
    assert meta["reason"] == "save_failed_user"
    assert "fail.json" in meta["path"]
