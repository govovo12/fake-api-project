from typing import Tuple, Optional
from workspace.utils.file.file_helper import generate_testdata_path, save_json
from workspace.config.rules.error_codes import ResultCode, ResultCode


def write_product_data(uuid: str, data: dict) -> Tuple[int, Optional[str], Optional[dict]]:
    """
    子組合器：將商品測資儲存為 JSON 檔案
    """
    path, meta_path = generate_testdata_path("product", uuid)
    if path is None:
        reason = meta_path.get("reason", "")
        code = ResultCode.get(reason, ResultCode.PRODUCT_TESTDATA_PATH_ERROR)
        return code, None, meta_path

    success, meta = save_json(path, data)
    if not success:
        reason = meta.get("reason", "")
        code = ResultCode.get(reason, ResultCode.PRODUCT_TESTDATA_SAVE_FAILED)
        return code, None, meta

    return ResultCode.SUCCESS, str(path), None
