import pytest
from uuid import uuid4
from workspace.controller.data_generation_controller import run_generate_testdata_flow
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.testdatacontroller, pytest.mark.integration]


def test_controller_all_success(monkeypatch, controller_mock):
    uuid = uuid4().hex

    controller_mock.patch_all_success(monkeypatch, {
        "prepare_testdata_files": (ResultCode.SUCCESS, {}, {}),
        "build_product_data": (ResultCode.SUCCESS, {"title": "mock", "price": 10.0}, {}),
        "write_product_data": (ResultCode.SUCCESS, {}, {}),
        "build_user_data": (ResultCode.SUCCESS, {"username": "tester", "email": "a@b.com"}, {}),
        "write_user_data": (ResultCode.SUCCESS, {}, {}),
    }, base_path="workspace.controller.data_generation_controller")

    code, user_data, product_data = run_generate_testdata_flow(uuid)

    assert code == ResultCode.TESTDATA_GENERATION_SUCCESS
    assert "username" in user_data
    assert "title" in product_data


def test_controller_fail_on_product_build(monkeypatch, controller_mock):
    uuid = uuid4().hex

    controller_mock.patch_all_success(monkeypatch, {
        "prepare_testdata_files": (ResultCode.SUCCESS, {}, {}),
    }, base_path="workspace.controller.data_generation_controller")

    controller_mock.patch_fail_on(
        monkeypatch,
        fail_step="build_product_data",
        fail_code=ResultCode.PRODUCT_GENERATION_FAILED,
        reason="unexpected_exception",
        base_path="workspace.controller.data_generation_controller"
    )

    code, user_data, product_data = run_generate_testdata_flow(uuid)

    assert code == ResultCode.PRODUCT_GENERATION_FAILED
    assert user_data is None
    assert product_data is None


def test_controller_fail_on_user_write(monkeypatch, controller_mock):
    uuid = uuid4().hex

    controller_mock.patch_all_success(monkeypatch, {
        "prepare_testdata_files": (ResultCode.SUCCESS, {}, {}),
        "build_product_data": (ResultCode.SUCCESS, {"title": "mock product"}, {}),
        "write_product_data": (ResultCode.SUCCESS, {}, {}),
        "build_user_data": (ResultCode.SUCCESS, {"username": "tester"}, {}),
    }, base_path="workspace.controller.data_generation_controller")

    controller_mock.patch_fail_on(
        monkeypatch,
        fail_step="write_user_data",
        fail_code=ResultCode.USER_TESTDATA_FILE_WRITE_FAILED,
        reason="save_failed_user",
        base_path="workspace.controller.data_generation_controller"
    )

    code, user_data, product_data = run_generate_testdata_flow(uuid)

    assert code == ResultCode.USER_TESTDATA_FILE_WRITE_FAILED
    assert user_data is None or isinstance(user_data, dict)
    assert product_data is None or isinstance(product_data, dict)
