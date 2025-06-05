from workspace.utils.response.response_helper import (
    is_status_code_success,
    extract_token_dict,
    is_register_success_dict,
    get_error_message_dict
)
from workspace.utils.request.request_handler import post_json
from workspace.utils.file.file_helper import read_json
from workspace.modules.register.build_register_payload import build_register_payload
from workspace.utils.logger.log_helper import print_info as log_info
from workspace.utils.logger.log_helper import print_error as log_error
from workspace.config.paths import get_user_testdata_path
from workspace.utils.error.error_handler import handle_exception
from workspace.utils.print.printer import print_info, print_error, print_success

__task_info__ = {
    "name": "user_register_controller",
    "desc": "註冊帳號（使用測資）",
    "version": "v1.0",
    "entry": lambda: run_user_register("023e4f2fb7ba46279caf9687d1e1c36b_user.json"),
}

def run_user_register(filename: str):
    try:
        print_info("檢查測資")
        data = read_json(get_user_testdata_path(filename))
        log_info("【檢查測資】成功", code=0)
    except Exception as e:
        err = handle_exception(e)
        print_error(f"❌ 測資讀取失敗：{err.get('msg')}")
        return

    try:
        code, payload = build_register_payload(data)
        if code != 0:
            log_error("【組裝註冊 payload】失敗", code=code)
            print_error(f"❌ 組裝註冊資料失敗（code={code}）")
            return
        log_info("【組裝註冊 payload】成功", code=0)
    except Exception as e:
        err = handle_exception(e)
        print_error(f"❌ 組裝流程錯誤：{err.get('msg')}")
        return

    try:
        res = post_json("https://fakestoreapi.com/users", payload)
        if not is_status_code_success(res.status_code):
            print_error(f"❌ 狀態碼錯誤：{res.status_code}")
            return

        res_json = res.json()
        if is_register_success_dict(res_json):
            print_success(f"✅ 註冊成功，帳號 ID：{res_json.get('id')}")
        else:
            msg = get_error_message_dict(res_json)
            print_error(f"❌ 註冊失敗：{msg}")
    except Exception as e:
        err = handle_exception(e)
        print_error(f"❌ 發送註冊流程失敗（code={err.get('code', -1)}）：{err.get('msg')}")
