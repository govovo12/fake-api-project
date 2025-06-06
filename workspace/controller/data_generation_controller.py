# workspace/controller/data_generation_controller.py

from workspace.modules.fake_data.orchestrator.testdata_generator import generate_testdata
from workspace.utils.logger.log_helper import log_step

def run_data_generation_controller():
    """
    控制器：呼叫組合器建立測資，並負責 log 顯示與流程判斷
    """
    code, data = generate_testdata()
    log_step("建立測資", code)

    if code != 0:
        return code, None  # 中止流程時也記得回傳

    print("✅ 測資成功，檔案儲存位置：")
    print(" - 使用者測資：", data["user_file"])
    print(" - 商品測資：", data["product_file"])

    return code, data  # ✅ 把 uuid 包在 data 裡回傳給總控器



__task_info__ = {
    "name": "產生測資",
    "module": "data_generation_controller",
    "function": "run_data_generation_controller",
    "desc": "若測資尚不存在，則產生一組含 UUID 的 user 與 product 並寫入檔案。",
    "path": "workspace/controller/data_generation_controller.py",
    "entry": run_data_generation_controller,  # ✅ main.py 會用到
    "default_params": {}  # 若未來要支援 CLI 傳參數，可在這裡預設
}
