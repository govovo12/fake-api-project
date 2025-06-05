"""
總控器（簡化版）：產生測資 → 註冊帳號
"""

from workspace.controller.data_generation_controller import generate_and_save_testdata
from workspace.controller.user_register_controller import run as run_user_register
from workspace.utils.logger.log_helper import log_step
from workspace.config.rules import error_codes

__task_info__ = {
    "task": "run_end_to_end_user_order_flow",
    "desc": "產生使用者測資，並執行註冊流程",
    "version": "1.0.0",
}


def run():
    ResultCode = error_codes.ResultCode

    print("\n🚀 開始執行 [使用者註冊流程] ...")

    # Step 1: 產生測資
    code, result = generate_and_save_testdata()
    log_step("產生測資", code)
    if code != ResultCode.SUCCESS or "uuid" not in result:
        print(f"❌ 測資產生失敗：{result}")
        return

    uuid = result["uuid"]
    print(f"✅ 測資產生成功，UUID：{uuid}")

    # Step 2: 執行註冊控制器，傳入 UUID
    run_user_register(user_uuid=uuid)

    print("✅ [使用者註冊流程] 已完成。\n")
