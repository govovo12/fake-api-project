import pytest
from unittest.mock import patch
from workspace.modules.fake_data.orchestrator import testdata_file_preparer
from workspace.config.rules.error_codes import ResultCode, TaskModuleError

pytestmark = [pytest.mark.unit, pytest.mark.orchestrator]


class TestPrepareTestdataFiles:
    """Unit tests for prepare_testdata_files using safe_call + retry."""

    def test_successful_creation(self):
        """
        ✅ 正常建立 user / product 測資檔案，應回傳 None。
        """
        with patch.object(testdata_file_preparer, "generate_testdata_path") as mock_path, \
             patch.object(testdata_file_preparer, "file_exists", return_value=False), \
             patch.object(testdata_file_preparer, "safe_call", return_value=None):

            mock_path.side_effect = ["user_path.json", "product_path.json"]
            result = testdata_file_preparer.prepare_testdata_files("fba3f655350842c5b94a2fa50e42c65e")
            assert result is None

    def test_file_already_exists(self):
        """
        ❌ 若任一檔案已存在，應回傳 USER_TESTDATA_ALREADY_EXISTS。
        """
        with patch.object(testdata_file_preparer, "generate_testdata_path") as mock_path, \
             patch.object(testdata_file_preparer, "file_exists", return_value=True):

            mock_path.side_effect = ["user.json", "product.json"]
            result = testdata_file_preparer.prepare_testdata_files("fba3f655350842c5b94a2fa50e42c65e")
            assert result == ResultCode.USER_TESTDATA_ALREADY_EXISTS

    def test_user_creation_failed(self):
        """
        ❌ 建立 user 測資檔案失敗，應回傳錯誤碼。
        """
        with patch.object(testdata_file_preparer, "generate_testdata_path") as mock_path, \
             patch.object(testdata_file_preparer, "file_exists", return_value=False), \
             patch.object(testdata_file_preparer, "safe_call") as mock_safe:

            mock_path.side_effect = ["user.json", "product.json"]
            mock_safe.side_effect = [40015, None]  # user fail, product success
            result = testdata_file_preparer.prepare_testdata_files("fba3f655350842c5b94a2fa50e42c65e")
            assert result == ResultCode.TESTDATA_USER_FILE_WRITE_FAILED

    def test_product_creation_failed(self):
        """
        ❌ 建立 product 測資檔案失敗，應回傳錯誤碼。
        """
        with patch.object(testdata_file_preparer, "generate_testdata_path") as mock_path, \
             patch.object(testdata_file_preparer, "file_exists", return_value=False), \
             patch.object(testdata_file_preparer, "safe_call") as mock_safe:

            mock_path.side_effect = ["user.json", "product.json"]
            mock_safe.side_effect = [None, 40014]  # user success, product fail
            result = testdata_file_preparer.prepare_testdata_files("fba3f655350842c5b94a2fa50e42c65e")
            assert result == ResultCode.TESTDATA_PRODUCT_FILE_WRITE_FAILED

    def test_generate_path_failed(self):
        """
        ❌ 若 generate_testdata_path 拋出錯誤（未包在 safe_call），應由最外層 except 捕捉。
        """
        with patch.object(testdata_file_preparer, "generate_testdata_path", side_effect=Exception("mock error")):
            result = testdata_file_preparer.prepare_testdata_files("fba3f655350842c5b94a2fa50e42c65e")
            assert result == ResultCode.UNKNOWN_FILE_SAVE_ERROR
