import pytest
import tempfile
import os
import json
from pathlib import Path

from workspace.utils.data.data_loader import load_json, save_json

# ✅ 全檔標記：unit + data 類別
pytestmark = [pytest.mark.unit, pytest.mark.data]


def test_load_json_success():
    """
    ✅ 測試成功載入 JSON 檔案
    """
    with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as f:
        json.dump({"name": "test"}, f)
        temp_path = f.name

    data, meta = load_json(temp_path)
    assert data == {"name": "test"}
    assert meta is None

    os.remove(temp_path)


def test_load_json_file_not_found():
    """
    ✅ 測試檔案不存在時回傳正確 reason
    """
    data, meta = load_json("nonexistent_file.json")
    assert data is None
    assert meta["reason"] == "file_not_found"


def test_load_json_empty_file():
    """
    ✅ 測試檔案為空時回傳錯誤
    """
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        temp_path = f.name

    data, meta = load_json(temp_path)
    assert data is None
    assert meta["reason"] == "file_empty_or_invalid"
    os.remove(temp_path)


def test_load_json_invalid_json():
    """
    ✅ 測試非 JSON 格式檔案
    """
    with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as f:
        f.write("not a json")
        temp_path = f.name

    data, meta = load_json(temp_path)
    assert data is None
    assert meta["reason"] == "load_json_failed"
    os.remove(temp_path)


def test_save_json_success():
    """
    ✅ 測試正常儲存 JSON
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "data.json"
        success, meta = save_json(file_path, {"key": "value"})
        assert success is True
        assert meta is None

        with open(file_path, encoding="utf-8") as f:
            assert json.load(f) == {"key": "value"}


def test_save_json_type_error():
    """
    ✅ 測試儲存時發生 JSON 轉換錯誤（TypeError）
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "bad.json"
        success, meta = save_json(file_path, {"x": set()})  # set 不能轉成 JSON
        assert success is False
        assert meta["reason"] == "json_serialization_failed"
