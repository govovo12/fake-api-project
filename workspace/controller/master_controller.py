from workspace.utils.uuid.uuid_generator import generate_batch_uuid_with_code
from workspace.utils.logger.log_helper import log_simple_result
from workspace.controller.data_generation_controller import generate_user_and_product_data
from workspace.config.rules.error_codes import ResultCode

__task_info__ = {
    "task": "generate-testdata",
    "entry": "run",
}


def run() -> int:
    """
    總控制器：執行測資產生任務（單一 UUID）
    1. 產生 UUID（透過工具模組）
    2. 印 log：產生成功或錯誤
    3. 呼叫子控制器進行測資產生
    4. 印 log：子控執行結果
    5. 回傳通用成功碼
    """
    # 1. 產生 UUID
    uuid = generate_batch_uuid_with_code()

    # 2. 若失敗（回傳錯誤碼 int），印 log 並中斷
    if not isinstance(uuid, str):
        log_simple_result(uuid)
        return uuid

    log_simple_result(ResultCode.SUCCESS)  # ✅ UUID 產生成功

    # 3. 呼叫子控制器產測資
    code = generate_user_and_product_data(uuid)

    # 4. 印執行結果
    log_simple_result(code)

    # 5. 總控本身結束成功
    return ResultCode.SUCCESS
