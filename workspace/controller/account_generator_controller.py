from workspace.config.global_config import ACCOUNT_GEN_CONFIG
from workspace.config.paths import BASE_PATH
from workspace.factory.module_factory import get_account_generator_module

def run_generate_account(config=ACCOUNT_GEN_CONFIG):
    deps = get_account_generator_module()

    username_cfg = config["username"]
    password_cfg = config["password"]
    path = BASE_PATH / "testdata" / "login" / "valid_case.json"

    account = deps["account_module"].generate_account(username_cfg, password_cfg, deps["random_fn"])
    result_path = deps["account_module"].save_account_to_json(account, path, deps["writer_fn"])

    print(f"[INFO] Account saved to: {result_path}")

