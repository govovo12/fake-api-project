import pytest
import uuid

from workspace.controller import data_generation_controller
from workspace.config.paths import USER_TESTDATA_ROOT as USER_PATH, PRODUCT_TESTDATA_ROOT as PRODUCT_PATH
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.controller, pytest.mark.testdatacontroller]

def test_controller_all_success(monkeypatch):
    test_uuid = uuid.uuid4().hex

    # ✅ 回傳完整欄位
    monkeypatch.setattr(
        data_generation_controller,
        "generate_testdata",
        lambda uuid: (
            ResultCode.SUCCESS,
            {
                "uuid": uuid,
                "user_file": USER_PATH / f"{uuid}.json",
                "product_file": PRODUCT_PATH / f"{uuid}.json",
                "user": {},
                "product": {}
            }
        )
    )

    code, info = data_generation_controller.run_data_generation_controller(test_uuid)
    assert code == ResultCode.SUCCESS
    assert info["uuid"] == test_uuid

def test_controller_fail_code(monkeypatch):
    test_uuid = uuid.uuid4().hex

    # ✅ 使用 ResultCode 中存在的錯誤碼：UUID_GEN_FAIL
    monkeypatch.setattr(
        data_generation_controller,
        "generate_testdata",
        lambda uuid: (ResultCode.UUID_GEN_FAIL, None)
    )

    code, info = data_generation_controller.run_data_generation_controller(test_uuid)
    assert code == ResultCode.UUID_GEN_FAIL
    assert info is None


