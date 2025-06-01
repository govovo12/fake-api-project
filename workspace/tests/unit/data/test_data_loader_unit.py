import pytest
import json
from pathlib import Path
from utils.data.data_loader import load_json, save_json, load_jsons

pytestmark = [pytest.mark.unit, pytest.mark.data]

def test_load_json_success(tmp_path):
    """[LOAD] 正常載入 JSON 檔案（should load valid file）"""
    test_data = {"key": "value"}
    file_path = tmp_path / "test.json"
    file_path.write_text(json.dumps(test_data), encoding="utf-8")
    result = load_json(file_path)
    assert result == test_data

def test_load_json_file_not_found(tmp_path):
    """[LOAD] 檔案不存在時回傳空 dict 並觸發 on_error（should handle file not found）"""
    file_path = tmp_path / "notfound.json"
    flag = {"called": False}
    def on_error(e, p):
        flag["called"] = True
        assert isinstance(e, Exception)
        assert p == file_path
    result = load_json(file_path, on_error=on_error)
    assert result == {}
    assert flag["called"] is True

def test_load_json_invalid_format(tmp_path):
    """[LOAD] JSON 格式錯誤時回傳空 dict 並觸發 on_error（should handle invalid format）"""
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{invalid json}", encoding="utf-8")
    flag = {"called": False}
    def on_error(e, p):
        flag["called"] = True
        assert isinstance(e, Exception)
        assert p == bad_file
    result = load_json(bad_file, on_error=on_error)
    assert result == {}
    assert flag["called"] is True

def test_load_json_no_on_error(tmp_path):
    """[LOAD] 出錯但沒傳 on_error，應不會報錯，單純回傳 {}"""
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{invalid json}", encoding="utf-8")
    result = load_json(bad_file)
    assert result == {}

def test_save_json_success_and_load(tmp_path):
    """[SAVE] 正常寫入 json 並可被 load_json 讀取"""
    test_data = {"abc": 123, "中文": "內容"}
    file_path = tmp_path / "saved.json"
    ok = save_json(test_data, file_path)
    assert ok is True
    assert file_path.exists()
    # 內容正確
    loaded = load_json(file_path)
    assert loaded == test_data

def test_save_json_invalid_path(tmp_path):
    """[SAVE] 寫入不存在資料夾應回傳 False 並觸發 on_error"""
    test_data = {"abc": 1}
    invalid_dir = tmp_path / "no_such_dir"
    invalid_path = invalid_dir / "file.json"
    flag = {"called": False}
    def on_error(e, p):
        flag["called"] = True
        assert isinstance(e, Exception)
        assert p == invalid_path
    ok = save_json(test_data, invalid_path, on_error=on_error)
    assert ok is False
    assert flag["called"] is True

def test_load_jsons_batch(tmp_path):
    """[BATCH LOAD] 資料夾內多個 json 應正確批次載入"""
    data1 = {"a": 1}
    data2 = {"b": 2}
    f1 = tmp_path / "1.json"
    f2 = tmp_path / "2.json"
    f1.write_text(json.dumps(data1), encoding="utf-8")
    f2.write_text(json.dumps(data2), encoding="utf-8")
    result = load_jsons(tmp_path)
    assert isinstance(result, dict)
    assert "1.json" in result and result["1.json"] == data1
    assert "2.json" in result and result["2.json"] == data2

def test_load_jsons_with_invalid_file(tmp_path):
    """[BATCH LOAD] 有一檔損壞時，應回傳空 dict 且不影響其他檔案"""
    good = {"x": 9}
    f1 = tmp_path / "ok.json"
    f2 = tmp_path / "bad.json"
    f1.write_text(json.dumps(good), encoding="utf-8")
    f2.write_text("{bad json}", encoding="utf-8")
    flags = []
    def on_error(e, p):
        flags.append(str(p))
        assert isinstance(e, Exception)
    result = load_jsons(tmp_path, on_error=on_error)
    assert "ok.json" in result and result["ok.json"] == good
    assert "bad.json" in result and result["bad.json"] == {}
    assert str(f2.name) in ''.join(flags)
