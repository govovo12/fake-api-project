import pytest
from unittest.mock import patch
from workspace.modules.fake_data.orchestrator import testdata_user_writer
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.orchestrator]


class TestWriteUserData:
    """Unit tests for write_user_data using safe_call."""

    def test_successful_write(self):
        """
        ✅ 正常產生路徑並成功寫入，應回傳 None。
        """
        with patch.object(testdata_user_writer, "generate_testdata_path", return_value="user.json"), \
             patch.object(testdata_user_writer, "safe_call", return_value=None):
            result = testdata_user_writer.write_user_data("fba3f655350842c5b94a2fa50e42c65e")
            assert result is None

    def test_generate_path_failed(self):
        """
        ❌ 若產生路徑時拋出非 TaskModuleError，應回傳 UNKNOWN_FILE_SAVE_ERROR。
        """
        with patch.object(testdata_user_writer, "generate_testdata_path", side_effect=Exception("boom")):
            result = testdata_user_writer.write_user_data("fba3f655350842c5b94a2fa50e42c65e")
            assert result == ResultCode.UNKNOWN_FILE_SAVE_ERROR

    def test_safe_call_failed(self):
        """
        ❌ 若 safe_call 回傳錯誤碼，應直接回傳該錯誤碼。
        """
        with patch.object(testdata_user_writer, "generate_testdata_path", return_value="user.json"), \
             patch.object(testdata_user_writer, "safe_call", return_value=ResultCode.USER_TESTDATA_SAVE_FAILED):
            result = testdata_user_writer.write_user_data("fba3f655350842c5b94a2fa50e42c65e")
            assert result == ResultCode.USER_TESTDATA_SAVE_FAILED
