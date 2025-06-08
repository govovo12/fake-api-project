from workspace.modules.fake_data.orchestrator.testdata_file_preparer import prepare_testdata_files
from workspace.modules.fake_data.orchestrator.testdata_product_builder import build_product_data
from workspace.modules.fake_data.orchestrator.testdata_product_writer import write_product_data
from workspace.modules.fake_data.orchestrator.testdata_user_builder import build_user_data
from workspace.modules.fake_data.orchestrator.testdata_user_writer import write_user_data
from workspace.utils.logger.trace_helper import print_trace
from workspace.utils.logger.log_helper import log_step
from workspace.config.rules.error_codes import ResultCode
from typing import Tuple, Optional

def run_generate_testdata_flow(uuid: str) -> Tuple[int, Optional[dict], Optional[dict]]:
    """
    子控制器：執行完整測資產生流程（user + product）
    - 每一步都會印 trace / log
    - 若任一步出錯則中斷並回傳錯誤碼與 meta
    - 若成功則回傳 user_data, product_data
    """
    print(f"\n🧭 子控制器啟動，接收到 UUID: {uuid}")

    # Step 1: 建立資料夾與空白測資檔案
    code, _, meta = prepare_testdata_files(uuid)
    print_trace(uuid, "prepare_testdata_files", meta)
    log_step("prepare_testdata_files", code)
    if code != ResultCode.SUCCESS:
        return code, None, None

    # Step 2: 產生商品資料
    code, product_data, meta = build_product_data(uuid)
    print_trace(uuid, "build_product_data", meta)
    log_step("build_product_data", code)
    if code != ResultCode.SUCCESS:
        return code, None, None

    # Step 3: 儲存商品資料
    code, _, meta = write_product_data(uuid, product_data)
    print_trace(uuid, "write_product_data", meta)
    log_step("write_product_data", code)
    if code != ResultCode.SUCCESS:
        return code, None, None

    # Step 4: 產生使用者資料
    code, user_data, meta = build_user_data(uuid)
    print_trace(uuid, "build_user_data", meta)
    log_step("build_user_data", code)
    if code != ResultCode.SUCCESS:
        return code, None, None

    # Step 5: 儲存使用者資料
    code, _, meta = write_user_data(uuid, user_data)
    print_trace(uuid, "write_user_data", meta)
    log_step("write_user_data", code)
    if code != ResultCode.SUCCESS:
        return code, None, None

    return ResultCode.TESTDATA_GENERATION_SUCCESS, user_data, product_data
