import pytest
from workspace.utils.stub import data_stub
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.stub]


def test_stub_valid_json_file():
    """
    測試 stub_valid_json_file 回傳的路徑字串格式是否合理。
    """
    result = data_stub.stub_valid_json_file()
    assert isinstance(result, str)
    assert "test_valid.json" in result


def test_stub_invalid_json_file_success(monkeypatch):
    """
    測試 stub_invalid_json_file 正常情況下回傳成功碼。
    模擬 Path.write_text 成功。
    """
    class DummyPath:
        def write_text(self, content, encoding):
            return None

    monkeypatch.setattr("workspace.utils.stub.data_stub.Path", lambda p: DummyPath())
    result = data_stub.stub_invalid_json_file()
    assert result == ResultCode.SUCCESS


def test_stub_invalid_json_file_write_fail(monkeypatch):
    """
    模擬 stub_invalid_json_file 寫檔失敗，檢查錯誤碼回傳。
    """
    class DummyPath:
        def write_text(self, content, encoding):
            raise Exception("write fail")

    monkeypatch.setattr("workspace.utils.stub.data_stub.Path", lambda p: DummyPath())
    result = data_stub.stub_invalid_json_file()
    assert result == ResultCode.TOOL_STUB_FILE_WRITE_FAILED


def test_stub_valid_json_dict():
    """
    測試 stub_valid_json_dict 回傳的 dict 結構與內容。
    """
    result = data_stub.stub_valid_json_dict()
    assert isinstance(result, dict)
    assert result.get("name") == "R88"
    assert result.get("enabled") is True


def test_stub_invalid_json_dict():
    """
    測試 stub_invalid_json_dict 回傳的 dict 結構與內容。
    """
    result = data_stub.stub_invalid_json_dict()
    assert isinstance(result, dict)
    assert result.get("version") is None
    assert isinstance(result.get("enabled"), str)


def test_stub_invalid_input_invalid_type():
    """
    測試 stub_invalid_input 傳入非法參數時，會回傳錯誤碼。
    """
    result = data_stub.stub_invalid_input("not a dict")
    assert result == ResultCode.TOOL_STUB_INVALID_DATA


def test_stub_invalid_input_valid_type():
    """
    測試 stub_invalid_input 傳入合法 dict 時，會回傳成功碼。
    """
    result = data_stub.stub_invalid_input({"key": "value"})
    assert result == ResultCode.SUCCESS
