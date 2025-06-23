"""
單元測試：create_cart 任務模組
測試目標：
- 成功建立購物車
- 處理異常情況（檔案格式錯誤、讀檔失敗、API 錯誤）
- Bearer token 與 headers 設定正確性
"""

# ------------------------
# 📦 測試框架與工具
# ------------------------
import pytest
from unittest.mock import patch, MagicMock

# ------------------------
# 🧪 被測模組與錯誤碼
# ------------------------
from workspace.modules.cart.create_cart import create_cart
from workspace.config.rules.error_codes import ResultCode

# ------------------------
# 🏷️ 測試標記
# ------------------------
pytestmark = [pytest.mark.unit, pytest.mark.cart]


class TestCreateCart:
    """單元測試：create_cart 任務模組"""

    @patch("workspace.modules.cart.create_cart.load_json", return_value={"userId": 1})
    @patch("workspace.modules.cart.create_cart.post_and_parse_json", return_value=(200, {"id": 10}))
    def test_create_cart_success(self, mock_post, mock_load):
        """✅ 測試成功建立購物車"""
        code, resp = create_cart("uuid-123", token="fake-token")
        assert code == ResultCode.SUCCESS
        assert resp == {"id": 10}

    @patch("workspace.modules.cart.create_cart.load_json", return_value=None)
    def test_create_cart_invalid_format(self, mock_load):
        """❌ 測試載入 JSON 格式錯誤"""
        code, resp = create_cart("uuid-123", token="fake-token")
        assert code == ResultCode.TOOL_FILE_LOAD_FAILED
        assert resp == {}

    @patch("workspace.modules.cart.create_cart.load_json", return_value={"userId": 1})
    @patch("workspace.modules.cart.create_cart.post_and_parse_json", return_value=(503, {}))
    def test_create_cart_server_error(self, mock_post, mock_load):
        """❌ 測試伺服器錯誤（5xx）"""
        code, resp = create_cart("uuid-123", token="fake-token")
        assert code == ResultCode.SERVER_ERROR
        assert resp == {}

    @patch("workspace.modules.cart.create_cart.load_json", return_value={"userId": 1})
    @patch("workspace.modules.cart.create_cart.post_and_parse_json", return_value=(408, {}))
    def test_create_cart_requests_exception(self, mock_post, mock_load):
        """❌ 測試請求錯誤（非 200 且非 5xx）"""
        code, resp = create_cart("uuid-123", token="fake-token")
        assert code == ResultCode.REQUESTS_EXCEPTION
        assert resp == {}

    @patch("workspace.modules.cart.create_cart.post_and_parse_json")
    @patch("workspace.modules.cart.create_cart.get_cart_path", return_value="fake/path/cart.json")
    @patch("workspace.modules.cart.create_cart.load_json", side_effect=Exception("file error"))
    def test_create_cart_exception(self, mock_load, mock_path, mock_post):
        """💥 測試讀取過程中拋出例外"""
        code, resp = create_cart("uuid-error", token="any")
        assert code == ResultCode.TOOL_FILE_LOAD_FAILED
        assert resp == {}

    @patch("workspace.modules.cart.create_cart.get_headers", return_value={"Content-Type": "application/json"})
    @patch("workspace.modules.cart.create_cart.load_json", return_value={"userId": 1})
    @patch("workspace.modules.cart.create_cart.post_and_parse_json", return_value=(200, {"id": 99}))
    def test_create_cart_token_header_attached(self, mock_post, mock_load, mock_headers):
        """🔒 測試 headers 是否附加 Bearer token"""
        token = "abc123"
        create_cart("uuid-123", token)
        headers = mock_post.call_args.kwargs.get("headers", {})
        assert headers["Authorization"] == f"Bearer {token}"
        assert headers["Content-Type"] == "application/json"

    @patch("workspace.modules.cart.create_cart.load_json", return_value={"userId": 1})
    @patch("workspace.modules.cart.create_cart.post_and_parse_json", return_value=(200, {}))
    def test_create_cart_response_empty(self, mock_post, mock_load):
        """📏 測試狀態碼為 200 但無內容"""
        code, resp = create_cart("uuid-123", token="abc")
        assert code == ResultCode.SUCCESS
        assert resp == {}

    @patch("workspace.modules.cart.create_cart.load_json", side_effect=FileNotFoundError("no such file"))
    def test_create_cart_missing_file(self, mock_load):
        """💥 測試檔案不存在（FileNotFoundError）"""
        code, resp = create_cart("uuid-404", token="abc")
        assert code == ResultCode.TOOL_FILE_LOAD_FAILED
        assert resp == {}

    @patch("workspace.modules.cart.create_cart.get_headers", return_value={"X-Custom": "test-header"})
    @patch("workspace.modules.cart.create_cart.load_json", return_value={"userId": 1})
    @patch("workspace.modules.cart.create_cart.post_and_parse_json", return_value=(200, {"id": 1}))
    def test_create_cart_content_type_preserved(self, mock_post, mock_load, mock_headers):
        """🔧 測試自訂 headers 是否保留"""
        token = "mytoken"
        create_cart("uuid-123", token)
        headers = mock_post.call_args.kwargs["headers"]
        assert headers["Authorization"] == f"Bearer {token}"
        assert headers["X-Custom"] == "test-header"
