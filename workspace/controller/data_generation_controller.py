from workspace.utils.file import file_helper
from workspace.utils.data import data_loader, data_enricher
from workspace.modules.fake_data.fake_user import user_generator
from workspace.modules.fake_data.fake_product import product_generator
from workspace.config import paths
from workspace.utils.logger import log_helper
from workspace.config.rules import error_codes
from workspace.utils.uuid import uuid_generator  

__task_info__ = {
    "task": "testdata_generation",
    "desc": "自動產生一組帳號與商品測資，並以相同 uuid 作為關聯，資料分別落地",
    "author": "Tony",
    "version": "1.0.0",
    "input": "無需外部輸入（自動隨機產生）",
    "output": "user.json, product.json 各一筆，檔名以 uuid 區分",
    "entry": None
}


def generate_and_save_testdata():
    ResultCode = error_codes.ResultCode
    log_step = log_helper.log_step

    # 開始
    log_step("開始產生測試資料", ResultCode.SUCCESS)

    # 1. 確認資料夾
    try:
        file_helper.ensure_dir(paths.USER_TESTDATA_ROOT)
        file_helper.ensure_dir(paths.PRODUCT_TESTDATA_ROOT)
        log_step("建立 testdata 目錄", ResultCode.SUCCESS)
    except Exception as e:
        log_step("建立 testdata 目錄", ResultCode.USER_WRITE_FAIL)
        return ResultCode.USER_WRITE_FAIL, {"msg": f"建立資料夾失敗: {e}"}

    # 2. 產生帳號資料
    code_user, user_data = user_generator.generate_user_data()
    log_step("產生帳號資料", code_user)
    if code_user != ResultCode.SUCCESS or not user_data:
        return code_user, {"msg": "帳號資料產生失敗"}

    # 3. 產生商品資料
    code_product, product_data = product_generator.generate_product_data()
    log_step("產生商品資料", code_product)
    if code_product != ResultCode.SUCCESS or not product_data:
        return code_product, {"msg": "商品資料產生失敗"}

    # 4. 產生 UUID
    code_uuid, batch_uuid = uuid_generator.generate_batch_uuid_with_code()
    log_step("產生 UUID", code_uuid)
    if code_uuid != ResultCode.SUCCESS or not batch_uuid:
        return code_uuid, {"msg": "UUID 產生失敗"}

    # 5. enrich with uuid
    user_with_uuid = data_enricher.enrich_with_uuid(user_data, batch_uuid)
    product_with_uuid = data_enricher.enrich_with_uuid(product_data, batch_uuid)
    log_step("組裝帳號資料", ResultCode.SUCCESS)
    log_step("組裝商品資料", ResultCode.SUCCESS)

    # 6. 寫檔案（覆蓋同名檔案）
    user_filename = f"{batch_uuid}_user.json"
    product_filename = f"{batch_uuid}_product.json"
    try:
        data_loader.save_json(user_with_uuid, paths.get_user_testdata_path(user_filename))
        log_step("寫入帳號資料", ResultCode.SUCCESS)
    except Exception as e:
        log_step("寫入帳號資料", ResultCode.USER_WRITE_FAIL)
        return ResultCode.USER_WRITE_FAIL, {"msg": f"帳號資料寫入失敗: {e}"}

    try:
        data_loader.save_json(product_with_uuid, paths.get_product_testdata_path(product_filename))
        log_step("寫入商品資料", ResultCode.SUCCESS)
    except Exception as e:
        log_step("寫入商品資料", ResultCode.PRODUCT_WRITE_FAIL)
        return ResultCode.PRODUCT_WRITE_FAIL, {"msg": f"商品資料寫入失敗: {e}"}

    # 結束
    log_step("資料產生並存檔", ResultCode.SUCCESS)
    return ResultCode.SUCCESS, {
        "msg": "資料產生並存檔成功",
        "uuid": batch_uuid,
        "user_file": str(paths.get_user_testdata_path(user_filename)),
        "product_file": str(paths.get_product_testdata_path(product_filename)),
    }


__task_info__["entry"] = generate_and_save_testdata
