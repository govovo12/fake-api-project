import pytest
import json
from pathlib import Path
from workspace.controller.data_generation_controller import generate_and_save_testdata
from workspace.utils.asserts.assert_helper import assert_in_keys
pytestmark = [pytest.mark.integration, pytest.mark.controller, pytest.mark.testdatacontroller]

def test_generate_and_save_testdata_integration(tmp_path, monkeypatch):
    # 1. 建立 sandbox 路徑
    user_dir = tmp_path / "user"
    product_dir = tmp_path / "product"
    user_dir.mkdir()
    product_dir.mkdir()

    # 2. patch 路徑變數和 function
    monkeypatch.setattr("workspace.config.paths.USER_TESTDATA_ROOT", user_dir)
    monkeypatch.setattr("workspace.config.paths.PRODUCT_TESTDATA_ROOT", product_dir)
    monkeypatch.setattr("workspace.config.paths.get_user_testdata_path", lambda fname: user_dir / fname)
    monkeypatch.setattr("workspace.config.paths.get_product_testdata_path", lambda fname: product_dir / fname)

    # 3. 執行主流程
    code, info = generate_and_save_testdata()
    assert code == 0
    assert "uuid" in info

    # 4. 驗證檔案產生且命名正確
    user_files = list(user_dir.glob("*.json"))
    product_files = list(product_dir.glob("*.json"))
    assert len(user_files) == 1
    assert len(product_files) == 1

    user_file = user_files[0]
    product_file = product_files[0]
    assert user_file.name.endswith("_user.json")
    assert product_file.name.endswith("_product.json")

    # 5. 讀取檔案內容，檢查 uuid、必要欄位
    with user_file.open(encoding="utf-8") as f:
        user_data = json.load(f)
    with product_file.open(encoding="utf-8") as f:
        product_data = json.load(f)

    # 檢查 uuid 一致
    uuid = info["uuid"]
    assert user_data.get("uuid") == uuid
    assert product_data.get("uuid") == uuid

    # 檢查必要欄位
    for field in ["uuid", "email", "password"]:
        assert field in user_data
    for field in ["uuid", "title", "category"]:
        assert field in product_data

    # 6. 檢查回傳資訊檔案路徑與實際一致
    assert str(user_file) == str(info["user_file"])
    assert str(product_file) == str(info["product_file"])

    # 7. 檢查產生內容格式正確（使用 assert_in_keys）
    user_required_keys = ["uuid", "email", "password", "passwordConfirm"]
    product_required_keys = ["uuid", "title", "category", "description", "image", "price"]

    assert_in_keys(user_data, user_required_keys)
    assert_in_keys(product_data, product_required_keys)



    


    