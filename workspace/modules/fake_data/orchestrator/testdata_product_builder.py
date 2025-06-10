from typing import Optional

from workspace.modules.fake_data.fake_product.product_generator import generate_product_data
from workspace.utils.data.data_enricher import enrich_with_uuid, enrich_payload
from workspace.utils.retry.retry_handler import safe_call
from workspace.config.rules.error_codes import ResultCode


def build_product_data(uuid: str) -> Optional[int]:
    """
    建立商品測資資料，並進行欄位補強與 UUID 附加

    成功 → 不回傳  
    失敗 → 回傳錯誤碼（ResultCode）
    """
    try:
        code = safe_call(generate_product_data, uuid)
        if code is not None:
            return code

        code = safe_call(enrich_with_uuid, {}, uuid)
        if code is not None:
            return code

        code = safe_call(enrich_payload, {})
        if code is not None:
            return code

        return ResultCode.SUCCESS

    except Exception as e:
        print(f"[DEBUG] build_product_data 例外：{type(e).__name__} - {str(e)}")
        return ResultCode.UNKNOWN_FILE_SAVE_ERROR
