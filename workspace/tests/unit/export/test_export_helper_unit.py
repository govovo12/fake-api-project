import pytest
import json
from pathlib import Path
from workspace.utils.export import export_helper

pytestmark = [pytest.mark.unit, pytest.mark.export]

def test_export_json_success(tmp_path):
    """export_json: 輸出 JSON 檔案，並驗證結構與內容"""
    data = {"x": 1, "y": [2, 3]}
    out_path = tmp_path / "report" / "data.json"
    export_helper.export_json(data, out_path)
    assert out_path.exists(), "JSON 檔案未正確建立"
    loaded = json.loads(out_path.read_text(encoding="utf-8"))
    assert loaded == data, "JSON 內容不符"

def test_export_json_invalid_data(tmp_path):
    """export_json: 非法資料型態（不可序列化）應拋 TypeError"""
    class Unserializable:
        pass
    data = {"bad": Unserializable()}
    out_path = tmp_path / "invalid.json"
    with pytest.raises(TypeError) as exc:
        export_helper.export_json(data, out_path)
    assert "is not JSON serializable" in str(exc.value) or "Object of type" in str(exc.value)

def test_export_text_success(tmp_path):
    """export_text: 正常寫入純文字檔案"""
    msg = "測試輸出內容"
    out_path = tmp_path / "log" / "output.log"
    export_helper.export_text(msg, out_path)
    assert out_path.exists(), "文字檔未正確建立"
    content = out_path.read_text(encoding="utf-8")
    assert content == msg, "寫入文字內容不正確"

def test_export_text_creates_directory(tmp_path):
    """export_text: 資料夾不存在時自動建立"""
    out_path = tmp_path / "nested" / "log" / "out.txt"
    export_helper.export_text("ok", out_path)
    assert out_path.exists(), "文字檔未建立"

def test_export_text_non_string_input(tmp_path):
    """export_text: 非字串輸入應拋 TypeError"""
    with pytest.raises(TypeError):
        export_helper.export_text(123, tmp_path / "bad.txt")
