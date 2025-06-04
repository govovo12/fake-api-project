from workspace.utils.file.file_helper import ensure_dir
from workspace.utils.data.save_json import save_json
from workspace.utils.data.data_enricher import enrich_with_uuid
from workspace.utils.uuid.uuid_generator import generate_batch_uuid
from workspace.modules.fake_data.fake_user.user_generator import generate_user_data
from workspace.modules.fake_data.fake_product.product_generator import generate_product_data
from workspace.paths import USER_TESTDATA_ROOT, PRODUCT_TESTDATA_ROOT, get_user_testdata_path, get_product_testdata_path


# 任務資訊結構，可依需求加欄位
__task_info__ = {
    "task": "testdata_generation",
    "desc": "自動產生一組帳號與商品測資，並以相同 uuid 作為關聯，資料分別落地",
    "author": "Tony",
    "version": "1.0.0",
    "input": "無需外部輸入（自動隨機產生）",
    "output": "user.json, product.json 各一筆，檔名以 uuid 區分",
    "entry": None  # 這裡要填 entry function
}

def generate_and_save_testdata():
    """
    控制器：自動產生一組帳號與商品測資，加上同組 uuid，分別落地
    回傳 (錯誤碼, 狀態字典)
    """
    # 1. 檢查目錄
    ensure_dir(USER_TESTDATA_ROOT)
    ensure_dir(PRODUCT_TESTDATA_ROOT)

    # 2. 產生帳號/商品資料
    code_user, user_data = generate_user_data()
    code_product, product_data = generate_product_data()

    if code_user != 0 or user_data is None:
        return 1001, {"msg": "帳號資料產生失敗", "code": code_user}
    if code_product != 0 or product_data is None:
        return 1002, {"msg": "商品資料產生失敗", "code": code_product}

    # 3. 產生 UUID
    batch_uuid = generate_batch_uuid()

    # 4. 各自 enrich
    user_with_uuid = enrich_with_uuid(user_data, batch_uuid)
    product_with_uuid = enrich_with_uuid(product_data, batch_uuid)

    # 5. 命名檔案並存檔
    user_filename = f"{batch_uuid}_user.json"
    product_filename = f"{batch_uuid}_product.json"
    save_json(user_with_uuid, get_user_testdata_path(user_filename))
    save_json(product_with_uuid, get_product_testdata_path(product_filename))

    # 6. 回傳成功狀態
    return 0, {
        "msg": "資料產生並存檔成功",
        "uuid": batch_uuid,
        "user_file": str(get_user_testdata_path(user_filename)),
        "product_file": str(get_product_testdata_path(product_filename)),
    }

# 執行範例
if __name__ == "__main__":
    code, info = generate_and_save_testdata()
    if code == 0:
        print("[SUCCESS]", info)
    else:
        print("[FAIL]", info)
        
__task_info__["entry"] = generate_and_save_testdata
