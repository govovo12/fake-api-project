from workspace.controller.data_generation_controller import run_generate_testdata_flow
from workspace.utils.logger.trace_helper import print_trace
from workspace.utils.logger.log_helper import log_step
from workspace.utils.uuid.uuid_generator import generate_batch_uuid_with_code
from workspace.config.rules.error_codes import ResultCode, SUCCESS_CODES, ResultCode


def run_end_to_end_user_order_flow():
    """
    主控：測試產生使用者與商品測資流程（由主控產生 UUID 並傳入）
    """
    print("\n[DEBUG] 開始執行 run()...\n")

    # Step 0: 使用 uuid 生成器產生 UUID（含錯誤處理）
    success, uuid, meta = generate_batch_uuid_with_code()
    if not success:
        code = ResultCode.get(meta.get("reason"), ResultCode.UUID_GEN_FAIL)
        print("❌ UUID 產生失敗，錯誤碼：", code)
        return
    code = ResultCode.SUCCESS

    print("\n🔹 UUID:", uuid)

    # Step 1: 傳入 UUID 給子控制器產測資
    code, result, meta = run_generate_testdata_flow(uuid)

    # Step 2: 印 trace 結果（用於 debug）
    print_trace(uuid, "run_end_to_end_user_order_flow", meta)

    # Step 3: 使用 log_helper 統一印出結果狀態
    log_step("run_end_to_end_user_order_flow", code)


# ✅ 放在檔案最底部，確保函式已定義
__task_info__ = {
    "task": "run_end_to_end_user_order_flow",
    "desc": "產生使用者測資（由主流程提供 UUID）",
    "entry": "run_end_to_end_user_order_flow"
}
