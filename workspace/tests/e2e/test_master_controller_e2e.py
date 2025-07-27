import pytest
from workspace.controller.master_controller import run
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.e2e, pytest.mark.controller]

def test_master_controller_real_flow(controller_inputs):
    """
    ✅ 主控 E2E 測試：
    使用 controller_inputs fixture 注入 headers, url, login_cred。
    驗證從產測資 ➜ 註冊 ➜ 登入 ➜ 建商品 ➜ 建購物車 ➜ 清除資料流程是否成功。
    """
    headers, url, login_cred = controller_inputs

    result = run(headers, url, login_cred)

    assert result == ResultCode.MASTER_TASK_SUCCESS 
