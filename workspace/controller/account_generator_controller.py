# workspace/controller/account_generator_controller.py

from workspace.config.rules.account_config import ACCOUNT_GEN_CONFIG
from workspace.config.rules.paths import BASE_PATH
from workspace.factory.module_factory import get_account_generator_module
from workspace.utils.logger import log_info, log_error


def run_generate_account(config=ACCOUNT_GEN_CONFIG):
    deps = get_account_generator_module()

    rules = config["rules"]
    params = config["params"]
    username_cfg = rules["username"]
    password_cfg = rules["password"]
    count = params.get("generate_count", 1)

    path = BASE_PATH / "testdata" / "login" / "valid_case.json"

    try:
        log_info(f"開始產生帳號，共 {count} 組")

        if count == 1:
            account = deps["account_module"].generate_account(username_cfg, password_cfg, deps["random_fn"])
        else:
            account = deps["account_module"].generate_accounts(username_cfg, password_cfg, deps["random_fn"], count)

        result_path = deps["account_module"].save_account_to_json(account, path, deps["writer_fn"])
        log_info(f"帳號產生完成，已儲存至：{result_path}")

        return {
            "success": True,
            "data": account
        }
    except Exception as e:
        log_error("產生帳號過程發生例外：" + str(e), code="ACCOUNT_GEN_FAIL")
        return {
            "success": False,
            "error_code": "ACCOUNT_GEN_FAIL",
            "message": str(e)
        }


__task_info__ = {
    "desc": "產生假帳號資料並輸出至測資檔",
    "entry": run_generate_account
}
