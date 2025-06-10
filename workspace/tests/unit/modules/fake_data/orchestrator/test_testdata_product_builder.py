import pytest
from unittest.mock import patch
from workspace.modules.fake_data.orchestrator import testdata_product_builder
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.orchestrator]


class TestBuildProductData:
    """Unit tests for build_product_data using safe_call."""

    def test_successful_build(self):
        """
        ✅ 三個階段全部成功，應回傳 None。
        """
        with patch.object(testdata_product_builder, "safe_call", return_value=None):
            result = testdata_product_builder.build_product_data("fba3f655350842c5b94a2fa50e42c65e")
            assert result is None

    def test_generate_product_failed(self):
        """
        ❌ generate_product_data() 失敗，應回傳錯誤碼。
        """
        with patch.object(testdata_product_builder, "safe_call") as mock_safe:
            mock_safe.side_effect = [ResultCode.PRODUCT_GENERATION_FAILED]
            result = testdata_product_builder.build_product_data("fba3f655350842c5b94a2fa50e42c65e")
            assert result == ResultCode.PRODUCT_GENERATION_FAILED

    def test_enrich_with_uuid_failed(self):
        """
        ❌ enrich_with_uuid() 失敗，應回傳錯誤碼。
        """
        with patch.object(testdata_product_builder, "safe_call") as mock_safe:
            mock_safe.side_effect = [
                None,  # generate 成功
                ResultCode.PRODUCT_UUID_ATTACH_FAILED
            ]
            result = testdata_product_builder.build_product_data("fba3f655350842c5b94a2fa50e42c65e")
            assert result == ResultCode.PRODUCT_UUID_ATTACH_FAILED

    def test_enrich_payload_failed(self):
        """
        ❌ enrich_payload() 失敗，應回傳錯誤碼。
        """
        with patch.object(testdata_product_builder, "safe_call") as mock_safe:
            mock_safe.side_effect = [
                None,  # generate 成功
                None,  # enrich uuid 成功
                ResultCode.ENRICH_WITH_UUID_FAILED
            ]
            result = testdata_product_builder.build_product_data("fba3f655350842c5b94a2fa50e42c65e")
            assert result == ResultCode.ENRICH_WITH_UUID_FAILED
