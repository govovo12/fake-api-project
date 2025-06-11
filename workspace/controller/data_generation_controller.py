from workspace.modules.fake_data.orchestrator.testdata_file_preparer import prepare_testdata_files
from workspace.modules.fake_data.orchestrator.generate_and_write_data import generate_and_write_data
from workspace.utils.logger.log_helper import log_step, is_success_code
from workspace.utils.logger.trace_helper import print_trace
from workspace.config.rules.error_codes import ResultCode

def run_generate_testdata_flow(uuid: str) -> int:
    """
    測資產生子控制器，依序處理測資任務流程
    僅回傳最終錯誤碼，並統一透過 log_helper 印出狀態
    """
    print("\n[DEBUG] 開始執行 run_generate_testdata_flow()...\n")
    print("🔹 UUID:", uuid)

    # Step 1: 建立空檔案
    step = "create_empty_files"
    code = prepare_testdata_files(uuid)
    log_step(code, step)
    print_trace(uuid, step)
    if not is_success_code(code):
        return code

    # Step 2: 建立並儲存商品測資
    step = "generate_and_save_product_data"
    code = generate_and_write_data("product", uuid)  # 呼叫生成並寫入商品資料的組合器
    log_step(code, step)
    print_trace(uuid, step)
    if not is_success_code(code):
        return code

    # Step 3: 建立並儲存使用者測資
    step = "generate_and_save_user_data"
    code = generate_and_write_data("user", uuid)  # 呼叫生成並寫入使用者資料的組合器
    log_step(code, step)
    print_trace(uuid, step)
    if not is_success_code(code):
        return code

    # ✅ 全部成功
    print(f"\n✅ 測資產生流程完成，UUID: {uuid}")
    return ResultCode.TESTDATA_GENERATION_SUCCESS
