import pytest
from utils.response.response_helper import (
    is_success,
    extract_token,
    get_error_message,
    get_data_field,
)

pytestmark = [pytest.mark.unit, pytest.mark.response]


class TestResponseHelper:

    def test_is_success_true(self):
        assert is_success({"code": 200, "data": {"key": "value"}})
        # ✅ 測試正常成功回應（code=200 且有 data）

    def test_is_success_false_missing_data(self):
        assert not is_success({"code": 200})
        # ❌ code=200 但沒有 data，不應視為成功

    def test_is_success_false_wrong_code(self):
        assert not is_success({"code": 400, "data": {}})
        # ❌ code 錯誤（非 200），不應視為成功

    def test_is_success_empty_response(self):
        assert not is_success({})
        # ❌ 完全空的回應，必為失敗

    def test_extract_token_exists(self):
        assert extract_token({"data": {"token": "abc123"}}) == "abc123"
        # ✅ 正常從 data 中取出 token

    def test_extract_token_missing_token(self):
        assert extract_token({"data": {}}) == ""
        # ❌ data 有但沒有 token，應回傳空字串

    def test_extract_token_missing_data(self):
        assert extract_token({}) == ""
        # ❌ 沒有 data 欄位，應回傳空字串

    def test_get_error_message_msg(self):
        assert get_error_message({"msg": "發生錯誤"}) == "發生錯誤"
        # ✅ 有 msg 欄位，應正確回傳 msg

    def test_get_error_message_error(self):
        assert get_error_message({"error": "錯誤發生"}) == "錯誤發生"
        # ✅ 沒有 msg 但有 error，也應正確回傳 error

    def test_get_error_message_fallback(self):
        assert get_error_message({}) == "未知錯誤"
        # ❌ 兩個欄位都沒有，應回傳預設錯誤訊息

    def test_get_data_field_exists(self):
        assert get_data_field({"data": {"user": "tony"}}, "user") == "tony"
        # ✅ data 中有指定欄位，應正確取得值

    def test_get_data_field_missing_key(self):
        assert get_data_field({"data": {"user": "tony"}}, "age") is None
        # ❌ 查詢欄位不存在，應回傳 None

    def test_get_data_field_missing_data(self):
        assert get_data_field({}, "user") is None
        # ❌ 沒有 data 欄位，應回傳 None
