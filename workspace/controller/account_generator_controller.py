from config.rules.account_config import ACCOUNT_GEN_CONFIG
from config.paths import get_default_account_json_path
from factory.module_factory import get_account_generator_module
from controller.log_controller import info, error
from utils.retry_helper import retry
from utils.print.printer import print_info, print_warn, print_error

@retry(max_attempts=3, delay=1)
def execute_generate_account(deps, config, path):
    rules = config["rules"]
    params = config["params"]
    username_cfg = rules["username"]
    password_cfg = rules["password"]
    count = params.get("generate_count", 1)

    info(f"開始產生帳號，共 {count} 組")
    print_info(f"🚀 開始產生帳號，共 {count} 組")

    if count == 1:
        account = deps["account_module"].generate_account(
            username_cfg, password_cfg, deps["random_fn"]
        )
    else:
        account = deps["account_module"].generate_accounts(
            username_cfg, password_cfg, deps["random_fn"], count
        )

    result_path = deps["account_module"].save_account_to_json(
        account, path, deps["writer_fn"]
    )

    info(f"帳號產生完成，已儲存至：{result_path}")
    print_info(f"✅ 帳號已儲存：{result_path}")

    return account


def run_generate_account(config=ACCOUNT_GEN_CONFIG):
    deps = get_account_generator_module()
    path = get_default_account_json_path()

    try:
        account = execute_generate_account(deps, config, path)
        return {
            "success": True,
            "data": account,
        }
    except Exception as e:
        error("產生帳號過程發生例外：" + str(e), code="ACCOUNT_GEN_FAIL")
        print_error(f"❌ 產生帳號錯誤：{str(e)}")
        return {
            "success": False,
            "error_code": "ACCOUNT_GEN_FAIL",
            "message": str(e),
        }

def run_account_generator_task():
    print("[task entry] 執行 run_account_generator_task()")
    result = run_generate_account()
    print("[task entry] 任務結果：", result)


# ✅ CLI 用的簡化入口
def run():
    return run_generate_account()
