import pytest
from unittest.mock import patch
from workspace.controller.master_controller import run
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.controller]


def test_run_all_success():
    """✅ 測試 run() 正常成功流程，應回傳主控成功碼"""
    with patch("workspace.controller.master_controller.generate_batch_uuid_with_code", return_value="mock-uuid"), \
         patch("workspace.controller.master_controller.generate_user_and_product_data", return_value=ResultCode.TESTDATA_TASK_SUCCESS), \
         patch("workspace.controller.master_controller.register_user_with_log", return_value=ResultCode.REGISTER_TASK_SUCCESS), \
         patch("workspace.controller.master_controller.login_and_report", return_value=(ResultCode.LOGIN_TASK_SUCCESS, "token-abc")), \
         patch("workspace.controller.master_controller.create_product_and_report", return_value=(ResultCode.CREATE_PRODUCT_SUCCESS, {})), \
         patch("workspace.controller.master_controller.create_cart_and_report", return_value=(ResultCode.CREATE_CART_SUCCESS, {})), \
         patch("workspace.controller.master_controller.clear_user_and_product_data", return_value=ResultCode.TASK_CLEAN_TESTDATA_SUCCESS):

        result = run(headers={}, url="https://fake.store", login_cred={})
        assert result == ResultCode.MASTER_TASK_SUCCESS


@pytest.mark.parametrize("fail_step, fail_return", [
    # 測資產生失敗 ➜ 模組錯誤
    ("generate_user_and_product_data", ResultCode.CART_GENERATION_FAILED),

    # 註冊失敗 ➜ 模組 API 失敗
    ("register_user_with_log", ResultCode.FAKER_REGISTER_FAILED),

    # 登入失敗 ➜ 模組 API 失敗（需傳 tuple）
    ("login_and_report", (ResultCode.LOGIN_API_FAILED, None)),

    # 建立商品失敗 ➜ 工具欄位缺失
    ("create_product_and_report", (ResultCode.TOOL_RESPONSE_FIELD_MISSING, None)),

    # 建立購物車失敗 ➜ 工具檔案寫入錯誤
    ("create_cart_and_report", (ResultCode.TOOL_FILE_WRITE_FAILED, None)),

    # 清除資料失敗 ➜ 模組錯誤
    ("clear_user_and_product_data", ResultCode.REMOVE_USER_DATA_FAILED),
])
def test_run_fails_on_each_step(fail_step, fail_return):
    """❌ 測試每個任務失敗時 run() 應提早中止並回傳對應錯誤碼"""
    patches = {
        "generate_batch_uuid_with_code": "mock-uuid",
        "generate_user_and_product_data": ResultCode.TESTDATA_TASK_SUCCESS,
        "register_user_with_log": ResultCode.REGISTER_TASK_SUCCESS,
        "login_and_report": (ResultCode.LOGIN_TASK_SUCCESS, "token-abc"),
        "create_product_and_report": (ResultCode.CREATE_PRODUCT_SUCCESS, {}),
        "create_cart_and_report": (ResultCode.CREATE_CART_SUCCESS, {}),
        "clear_user_and_product_data": ResultCode.TASK_CLEAN_TESTDATA_SUCCESS,
    }
    patches[fail_step] = fail_return

    with patch("workspace.controller.master_controller.generate_batch_uuid_with_code", return_value=patches["generate_batch_uuid_with_code"]), \
         patch("workspace.controller.master_controller.generate_user_and_product_data", return_value=patches["generate_user_and_product_data"]), \
         patch("workspace.controller.master_controller.register_user_with_log", return_value=patches["register_user_with_log"]), \
         patch("workspace.controller.master_controller.login_and_report", return_value=patches["login_and_report"]), \
         patch("workspace.controller.master_controller.create_product_and_report", return_value=patches["create_product_and_report"]), \
         patch("workspace.controller.master_controller.create_cart_and_report", return_value=patches["create_cart_and_report"]), \
         patch("workspace.controller.master_controller.clear_user_and_product_data", return_value=patches["clear_user_and_product_data"]):

        result = run(headers={}, url="https://fake.store", login_cred={})

        if isinstance(fail_return, tuple):
            expected_code = fail_return[0]
        else:
            expected_code = fail_return

        assert result == expected_code
