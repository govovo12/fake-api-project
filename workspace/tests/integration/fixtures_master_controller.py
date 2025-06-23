import pytest
from workspace.config.rules.error_codes import ResultCode

# ---------------------------------------------------
# Fixture：UUID 模擬（兩種不能同時出現）
# ---------------------------------------------------

@pytest.fixture
def patch_uuid(monkeypatch):
    """
    一般情境：產生固定 UUID 字串。
    """
    monkeypatch.setattr(
        "workspace.utils.uuid.uuid_generator.generate_batch_uuid_with_code",
        lambda *args, **kwargs: "mock-fixed-uuid-1234567890abcdef"
    )


@pytest.fixture
def uuid_invalid_case(monkeypatch):
    """
    專供 test_master_uuid_fail 使用：模擬 UUID 回傳非字串型別。
    注意要 patch 主控實際 import 的版本。
    """
    monkeypatch.setattr(
        "workspace.controller.master_controller.generate_batch_uuid_with_code",
        lambda *args, **kwargs: 123456
    )
    return {"expected_result": ResultCode.UUID_GEN_FAIL}



# ---------------------------------------------------
# Fixture：主控整合測試情境
# ---------------------------------------------------

@pytest.fixture
def all_success_scenario(monkeypatch, patch_uuid):
    """
    模擬所有子控制器皆成功的情況。
    """
    monkeypatch.setattr(
        "workspace.controller.master_controller.generate_user_and_product_data",
        lambda *args, **kwargs: ResultCode.TESTDATA_TASK_SUCCESS
    )
    monkeypatch.setattr(
        "workspace.controller.master_controller.register_user_with_log",
        lambda *args, **kwargs: ResultCode.REGISTER_TASK_SUCCESS
    )
    monkeypatch.setattr(
        "workspace.controller.master_controller.login_and_report",
        lambda *args, **kwargs: (ResultCode.LOGIN_TASK_SUCCESS, "mock-token")
    )
    monkeypatch.setattr(
        "workspace.controller.master_controller.create_product_and_report",
        lambda *args, **kwargs: (ResultCode.CREATE_PRODUCT_SUCCESS, {})
    )
    monkeypatch.setattr(
        "workspace.controller.master_controller.create_cart_and_report",
        lambda *args, **kwargs: (ResultCode.CREATE_CART_SUCCESS, {})
    )
    monkeypatch.setattr(
        "workspace.controller.master_controller.clear_user_and_product_data",
        lambda *args, **kwargs: ResultCode.TASK_CLEAN_TESTDATA_SUCCESS
    )
    return {"expected_result": ResultCode.MASTER_TASK_SUCCESS}


@pytest.fixture
def fail_step2(monkeypatch, patch_uuid):
    """模擬測資產生失敗"""
    monkeypatch.setattr(
        "workspace.controller.master_controller.generate_user_and_product_data",
        lambda *args, **kwargs: ResultCode.TOOL_FILE_WRITE_FAILED
    )
    return {"expected_result": ResultCode.TOOL_FILE_WRITE_FAILED}


@pytest.fixture
def fail_step3(monkeypatch, patch_uuid):
    """模擬註冊帳號失敗"""
    monkeypatch.setattr(
        "workspace.controller.master_controller.generate_user_and_product_data",
        lambda *args, **kwargs: ResultCode.TESTDATA_TASK_SUCCESS
    )
    monkeypatch.setattr(
        "workspace.controller.master_controller.register_user_with_log",
        lambda *args, **kwargs: ResultCode.FAKER_REGISTER_FAILED
    )
    return {"expected_result": ResultCode.FAKER_REGISTER_FAILED}


@pytest.fixture
def fail_step4(monkeypatch, patch_uuid):
    """模擬登入失敗"""
    monkeypatch.setattr(
        "workspace.controller.master_controller.generate_user_and_product_data",
        lambda *args, **kwargs: ResultCode.TESTDATA_TASK_SUCCESS
    )
    monkeypatch.setattr(
        "workspace.controller.master_controller.register_user_with_log",
        lambda *args, **kwargs: ResultCode.REGISTER_TASK_SUCCESS
    )
    monkeypatch.setattr(
        "workspace.controller.master_controller.login_and_report",
        lambda *args, **kwargs: (ResultCode.LOGIN_API_FAILED, None)
    )
    return {"expected_result": ResultCode.LOGIN_API_FAILED}


@pytest.fixture
def fail_step5(monkeypatch, patch_uuid):
    """模擬建立商品失敗"""
    monkeypatch.setattr(
        "workspace.controller.master_controller.generate_user_and_product_data",
        lambda *args, **kwargs: ResultCode.TESTDATA_TASK_SUCCESS
    )
    monkeypatch.setattr(
        "workspace.controller.master_controller.register_user_with_log",
        lambda *args, **kwargs: ResultCode.REGISTER_TASK_SUCCESS
    )
    monkeypatch.setattr(
        "workspace.controller.master_controller.login_and_report",
        lambda *args, **kwargs: (ResultCode.LOGIN_TASK_SUCCESS, "mock-token")
    )
    monkeypatch.setattr(
        "workspace.controller.master_controller.create_product_and_report",
        lambda *args, **kwargs: (ResultCode.CREATE_PRODUCT_FAILED, None)
    )
    return {"expected_result": ResultCode.CREATE_PRODUCT_FAILED}


@pytest.fixture
def fail_step6(monkeypatch, patch_uuid):
    """模擬建立購物車失敗"""
    monkeypatch.setattr(
        "workspace.controller.master_controller.generate_user_and_product_data",
        lambda *args, **kwargs: ResultCode.TESTDATA_TASK_SUCCESS
    )
    monkeypatch.setattr(
        "workspace.controller.master_controller.register_user_with_log",
        lambda *args, **kwargs: ResultCode.REGISTER_TASK_SUCCESS
    )
    monkeypatch.setattr(
        "workspace.controller.master_controller.login_and_report",
        lambda *args, **kwargs: (ResultCode.LOGIN_TASK_SUCCESS, "mock-token")
    )
    monkeypatch.setattr(
        "workspace.controller.master_controller.create_product_and_report",
        lambda *args, **kwargs: (ResultCode.CREATE_PRODUCT_SUCCESS, {})
    )
    monkeypatch.setattr(
        "workspace.controller.master_controller.create_cart_and_report",
        lambda *args, **kwargs: (ResultCode.CART_CREATE_FAILED, None)
    )
    return {"expected_result": ResultCode.CART_CREATE_FAILED}


@pytest.fixture
def fail_step7(monkeypatch, patch_uuid):
    """模擬清除測資失敗（主控應中止並回傳錯誤碼）"""
    monkeypatch.setattr(
        "workspace.controller.master_controller.generate_user_and_product_data",
        lambda *args, **kwargs: ResultCode.TESTDATA_TASK_SUCCESS
    )
    monkeypatch.setattr(
        "workspace.controller.master_controller.register_user_with_log",
        lambda *args, **kwargs: ResultCode.REGISTER_TASK_SUCCESS
    )
    monkeypatch.setattr(
        "workspace.controller.master_controller.login_and_report",
        lambda *args, **kwargs: (ResultCode.LOGIN_TASK_SUCCESS, "mock-token")
    )
    monkeypatch.setattr(
        "workspace.controller.master_controller.create_product_and_report",
        lambda *args, **kwargs: (ResultCode.CREATE_PRODUCT_SUCCESS, {})
    )
    monkeypatch.setattr(
        "workspace.controller.master_controller.create_cart_and_report",
        lambda *args, **kwargs: (ResultCode.CREATE_CART_SUCCESS, {})
    )
    monkeypatch.setattr(
        "workspace.controller.master_controller.clear_user_and_product_data",
        lambda *args, **kwargs: ResultCode.REMOVE_USER_DATA_FAILED
    )
    return {"expected_result": ResultCode.REMOVE_USER_DATA_FAILED}
