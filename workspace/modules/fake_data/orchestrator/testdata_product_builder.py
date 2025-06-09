from typing import Tuple, Optional
from workspace.modules.fake_data.fake_product.product_generator import generate_product_data
from workspace.utils.data.data_enricher import enrich_with_uuid
from workspace.config.rules.error_codes import ResultCode, REASON_CODE_MAP


def build_product_data(uuid: str) -> Tuple[int, Optional[dict], Optional[dict]]:
    """
    子組合器：產生商品測資並附加 UUID
    回傳格式：code, product_data or None, meta or None
    """
    success, product_data, meta = generate_product_data()
    if not success:
        reason = meta.get("reason", "")
        code = REASON_CODE_MAP.get(reason, ResultCode.PRODUCT_GENERATION_FAILED)
        return code, None, meta

    success, product_with_uuid, meta = enrich_with_uuid(product_data, uuid)
    if not success:
        reason = meta.get("reason", "")
        code = REASON_CODE_MAP.get(reason, ResultCode.PRODUCT_UUID_ATTACH_FAILED)
        return code, None, meta

    return ResultCode.SUCCESS, product_with_uuid, None
