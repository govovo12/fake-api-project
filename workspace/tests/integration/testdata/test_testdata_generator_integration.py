import pytest
import uuid

from workspace.modules.fake_data.orchestrator import testdata_generator
from workspace.config.paths import USER_TESTDATA_ROOT as USER_PATH, PRODUCT_TESTDATA_ROOT as PRODUCT_PATH
from workspace.utils.file.file_helper import file_exists
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.integration, pytest.mark.testdata]

# ✅ 成功產生測資測試
def test_generate_testdata_success():
    test_uuid = uuid.uuid4().hex

    code, result = testdata_generator.generate_testdata(test_uuid)

    assert code == ResultCode.SUCCESS
    assert isinstance(result, dict)
    assert result["uuid"] == test_uuid

    user_file = USER_PATH / f"{test_uuid}.json"
    product_file = PRODUCT_PATH / f"{test_uuid}.json"
    assert file_exists(user_file)
    assert file_exists(product_file)
# ✅ 產生測資失敗
def test_generate_testdata_fail_if_user_generator_fails(monkeypatch):
    test_uuid = uuid.uuid4().hex

    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.testdata_generator.generate_fake_user",
        lambda: (99999, None)
    )

    code, result = testdata_generator.generate_testdata(test_uuid)

    assert code != ResultCode.SUCCESS
    assert result is None

