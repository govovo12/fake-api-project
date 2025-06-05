# workspace/modules/register/build_register_payload.py

from workspace.utils.data import data_loader
from workspace.utils.env import env_manager
from workspace.config import paths
from workspace.utils.logger import log_helper
from workspace.config.rules import error_codes


def build_register_payload(user_file_name: str):
    """
    [子模組] 組裝註冊 API 的 payload 結構（依據測資 json + env 指定欄位）

    Args:
        user_file_name (str): 使用者測資檔案名稱（不含路徑）

    Returns:
        (code, payload or msg): 結果狀態與資料或錯誤資訊
    """
    try:
        # 讀取 user 測資檔
        user_data = data_loader.load_json(paths.USER_TESTDATA_ROOT / user_file_name)
    except Exception as e:
        return error_codes.ResultCode.USER_TESTDATA_NOT_FOUND, {"msg": str(e)}

    try:
        # 讀取 env 變數（欄位）
        env_data = env_manager.EnvManager.load_env_dict(paths.LOGIN_ENV_PATH)
        register_fields = env_data.get("REGISTER_FIELDS", "username,password,email,name").split(",")
        payload = {}

        for field in register_fields:
            if field == "username":
                email = user_data.get("email", "")
                payload["username"] = email.split("@")[0]
            elif field == "name" and "name" in user_data:
                name = user_data["name"]
                if " " in name:
                    firstname, lastname = name.split(" ", 1)
                else:
                    firstname = lastname = name
                payload["name"] = {
                    "firstname": firstname,
                    "lastname": lastname
                }
            else:
                payload[field] = user_data[field]

        return error_codes.ResultCode.SUCCESS, payload

    except Exception as e:
        return error_codes.ResultCode.PAYLOAD_BUILD_FAIL, {"msg": str(e)}
