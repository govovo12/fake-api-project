import pytest
from unittest.mock import patch
from workspace.modules.fake_data.orchestrator import testdata_product_writer
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.orchestrator]


class TestWriteProductData:
    """Unit tests for write_product_data using safe_call."""

    def test_successful_write(self):
        """
        ✅ 正常產生路徑並寫入資料，應回傳 None。
        """
        with patch.object(testdata_product_writer, "generate_testdata_path", return_value="product.json"), \
             patch.object(testdata_product_writer, "safe_call", return_value=None):
            result = testdata_product_writer.write_product_data("fba3f655350842c5b94a2fa50e42c65e")
            assert result is None

    def test_generate_path_failed(self):
        """
        ❌ 若 generate_testdata_path 發生錯誤，應回傳 UNKNOWN_FILE_SAVE_ERROR。
        """
        with patch.object(testdata_product_writer, "generate_testdata_path", side_effect=Exception("boom")):
            result = testdata_product_writer.write_product_data("fba3f655350842c5b94a2fa50e42c65e")
            assert result == ResultCode.UNKNOWN_FILE_SAVE_ERROR

    def test_safe_call_failed(self):
        """
        ❌ 若 safe_call 回傳錯誤碼（寫入失敗），應直接回傳該錯誤碼。
        """
        with patch.object(testdata_product_writer, "generate_testdata_path", return_value="product.json"), \
             patch.object(testdata_product_writer, "safe_call", return_value=ResultCode.PRODUCT_TESTDATA_SAVE_FAILED):
            result = testdata_product_writer.write_product_data("fba3f655350842c5b94a2fa50e42c65e")
            assert result == ResultCode.PRODUCT_TESTDATA_SAVE_FAILED
