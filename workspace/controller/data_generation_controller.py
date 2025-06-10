from workspace.modules.fake_data.orchestrator.testdata_file_preparer import prepare_testdata_files
from workspace.modules.fake_data.orchestrator.testdata_product_builder import build_product_data
from workspace.modules.fake_data.orchestrator.testdata_product_writer import write_product_data
from workspace.modules.fake_data.orchestrator.testdata_user_builder import build_user_data
from workspace.modules.fake_data.orchestrator.testdata_user_writer import write_user_data
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

    # Step 2: 建立商品測資
    step = "generate_product_data"
    code = build_product_data(uuid)
    log_step(code, step)
    print_trace(uuid, step)
    if not is_success_code(code):
        return code

    # Step 3: 儲存商品測資
    step = "save_product_data"
    code = write_product_data(uuid)
    log_step(code, step)
    print_trace(uuid, step)
    if not is_success_code(code):
        return code

    # Step 4: 建立使用者測資
    step = "generate_user_data"
    code = build_user_data(uuid)
    log_step(code, step)
    print_trace(uuid, step)
    if not is_success_code(code):
        return code

    # Step 5: 儲存使用者測資
    step = "save_user_data"
    code = write_user_data(uuid)
    log_step(code, step)
    print_trace(uuid, step)
    if not is_success_code(code):
        return code

    # ✅ 全部成功
    print(f"\n✅ 測資產生流程完成，UUID: {uuid}")
    return ResultCode.TESTDATA_GENERATION_SUCCESS
