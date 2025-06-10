import pytest
from unittest.mock import patch
from workspace.modules.fake_data.orchestrator import testdata_user_builder
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.orchestrator]


class TestBuildUserData:
    """Unit tests for build_user_data using safe_call."""

    def test_successful_build(self):
        """
        ✅ 正常產生 user 並加上 UUID，應回傳 None。
        """
        with patch.object(testdata_user_builder, "safe_call", return_value=None):
            result = testdata_user_builder.build_user_data("fba3f655350842c5b94a2fa50e42c65e")
            assert result is None

    def test_generate_user_data_failed(self):
        """
        ❌ 若產生 user 資料失敗，應回傳對應錯誤碼。
        """
        with patch.object(testdata_user_builder, "safe_call") as mock_safe:
            mock_safe.side_effect = [ResultCode.USER_GENERATION_FAILED]
            result = testdata_user_builder.build_user_data("fba3f655350842c5b94a2fa50e42c65e")
            assert result == ResultCode.USER_GENERATION_FAILED

    def test_enrich_with_uuid_failed(self):
        """
        ❌ 若附加 UUID 失敗，應回傳對應錯誤碼。
        """
        with patch.object(testdata_user_builder, "safe_call") as mock_safe:
            mock_safe.side_effect = [
                None,  # generate_user_data 成功
                ResultCode.USER_UUID_ATTACH_FAILED  # enrich 失敗
            ]
            result = testdata_user_builder.build_user_data("fba3f655350842c5b94a2fa50e42c65e")
            assert result == ResultCode.USER_UUID_ATTACH_FAILED

    def test_unexpected_exception(self):
        """
        ❌ 若整體流程有非預期錯誤，應回傳 UNKNOWN_FILE_SAVE_ERROR。
        """
        with patch.object(testdata_user_builder, "safe_call", side_effect=Exception("boom")):
            result = testdata_user_builder.build_user_data("fba3f655350842c5b94a2fa50e42c65e")
            assert result == ResultCode.UNKNOWN_FILE_SAVE_ERROR
