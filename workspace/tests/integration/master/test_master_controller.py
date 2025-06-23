import pytest
from workspace.controller.master_controller import run
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.integration, pytest.mark.controller]


def test_master_success(all_success_scenario):
    """
    測試主控流程全部成功時，是否正確回傳 MASTER_TASK_SUCCESS。
    """
    result = run(
        headers={"Authorization": "Bearer mock-token"},
        url="https://fake.store",
        login_cred={"account": "test", "password": "1234"}
    )
    assert result == all_success_scenario["expected_result"]


def test_master_uuid_fail(uuid_invalid_case):
    """
    測試 UUID 產生異常時，主控應中止並回傳 UUID_GEN_FAIL。
    """
    result = run(headers={}, url="", login_cred={})
    assert result == uuid_invalid_case["expected_result"]


def test_master_step2_fail(fail_step2):
    """
    測試測資產生失敗時，主控應中止並回傳 TOOL_FILE_WRITE_FAILED。
    """
    result = run(headers={}, url="", login_cred={})
    assert result == fail_step2["expected_result"]


def test_master_step3_fail(fail_step3):
    """
    測試註冊帳號失敗時，主控應中止並回傳 FAKER_REGISTER_FAILED。
    """
    result = run(headers={}, url="", login_cred={})
    assert result == fail_step3["expected_result"]


def test_master_step4_fail(fail_step4):
    """
    測試登入帳號失敗時，主控應中止並回傳 LOGIN_API_FAILED。
    """
    result = run(headers={}, url="", login_cred={})
    assert result == fail_step4["expected_result"]


def test_master_step5_fail(fail_step5):
    """
    測試建立商品失敗時，主控應中止並回傳 CREATE_PRODUCT_FAILED。
    """
    result = run(headers={}, url="", login_cred={})
    assert result == fail_step5["expected_result"]


def test_master_step6_fail(fail_step6):
    """
    測試建立購物車失敗時，主控應中止並回傳 CART_CREATE_FAILED。
    """
    result = run(headers={}, url="", login_cred={})
    assert result == fail_step6["expected_result"]


def test_master_step7_fail(fail_step7):
    """
    測試清除測資失敗時，主控應中止並回傳 REMOVE_USER_DATA_FAILED。
    """
    result = run(headers={}, url="", login_cred={})
    assert result == fail_step7["expected_result"]
