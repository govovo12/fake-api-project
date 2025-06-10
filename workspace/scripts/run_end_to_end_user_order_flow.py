from workspace.controller.data_generation_controller import run_generate_testdata_flow
from workspace.utils.logger.trace_helper import print_trace
from workspace.utils.logger.log_helper import log_step
from workspace.utils.uuid.uuid_generator import generate_batch_uuid_with_code
from workspace.config.rules.error_codes import ResultCode


def run_end_to_end_user_order_flow():
    """
    主控流程：產生 UUID 並傳入子控處理測資任務
    僅回傳錯誤碼並統一透過 log_helper 印出狀態
    """
    print("\n[DEBUG] 開始執行 run_end_to_end_user_order_flow()...\n")

    # Step 0: 產生 UUID（不會失敗）
    uuid = generate_batch_uuid_with_code()
    print("\n🔹 UUID:", uuid)

    # Step 1: 呼叫子控
    code = run_generate_testdata_flow(uuid)

    # Step 2: log 結果
    log_step(code, "run_end_to_end_user_order_flow")
    print_trace(uuid, "run_end_to_end_user_order_flow", None)

    return code




# ✅ 任務資訊（供主控註冊）
__task_info__ = {
    "task": "run_end_to_end_user_order_flow",
    "desc": "產生使用者與商品測資（由主流程提供 UUID）",
    "entry": "run_end_to_end_user_order_flow"
}
