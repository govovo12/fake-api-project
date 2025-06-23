"""
單元測試：remove_product_data 任務模組
"""

# ------------------------
# 📦 測試框架與 Mock
# ------------------------
import pytest
from unittest.mock import patch

# ------------------------
# 🧪 被測模組與錯誤碼
# ------------------------
from workspace.modules.cleaner.remove_product_data import remove_product_data
from workspace.config.rules.error_codes import ResultCode

# ------------------------
# 🏷️ 測試標記
# ------------------------
pytestmark = [pytest.mark.unit, pytest.mark.cleaner]


class TestRemoveProductData:
    @patch("workspace.modules.cleaner.remove_product_data.get_product_path")
    @patch("workspace.modules.cleaner.remove_product_data.delete_file", return_value=ResultCode.SUCCESS)
    def test_remove_product_data_success(self, mock_delete, mock_path):
        """✅ 測試成功刪除商品測資檔案"""
        code = remove_product_data("uuid-123")
        assert code == ResultCode.SUCCESS

    @patch("workspace.modules.cleaner.remove_product_data.get_product_path")
    @patch("workspace.modules.cleaner.remove_product_data.delete_file", return_value=ResultCode.TOOL_FILE_DELETE_FAILED)
    def test_remove_product_data_failed(self, mock_delete, mock_path):
        """❌ 測試刪除失敗時回傳任務層錯誤碼"""
        code = remove_product_data("uuid-456")
        assert code == ResultCode.REMOVE_PRODUCT_DATA_FAILED

    @patch("workspace.modules.cleaner.remove_product_data.get_product_path")
    @patch("workspace.modules.cleaner.remove_product_data.delete_file", side_effect=Exception("unexpected error"))
    def test_remove_product_data_exception(self, mock_delete, mock_path):
        """💥 測試工具層拋出例外時回傳任務層錯誤碼"""
        code = remove_product_data("uuid-exception")
        assert code == ResultCode.REMOVE_PRODUCT_DATA_FAILED

    def test_remove_product_data_empty_uuid(self):
        """🧪 測試空 UUID 行為（視業務需求可強化）"""
        code = remove_product_data("")
        assert isinstance(code, int)
