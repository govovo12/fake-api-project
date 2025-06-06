# workspace/modules/fake_data/orchestrator/testdata_generator.py

from pathlib import Path

from workspace.config.rules.error_codes import ResultCode
from workspace.modules.fake_data.fake_user.user_generator import generate_fake_user
from workspace.modules.fake_data.fake_product.product_generator import generate_fake_product
from workspace.utils.uuid.uuid_generator import generate_batch_uuid_with_code
from workspace.utils.data.data_enricher import enrich_with_uuid
from workspace.utils.file.file_helper import file_exists, is_file_empty
from workspace.utils.data.data_loader import save_json

TESTDATA_PATH = Path("workspace/testdata")
USER_PATH = TESTDATA_PATH / "user"
PRODUCT_PATH = TESTDATA_PATH / "product"


def _check_if_testdata_exists(uuid: str) -> bool:
    """檢查該 UUID 對應的 user 與 product 測資是否已存在且非空"""
    user_file = USER_PATH / f"{uuid}.json"
    product_file = PRODUCT_PATH / f"{uuid}.json"

    return all([
        file_exists(user_file) and not is_file_empty(user_file),
        file_exists(product_file) and not is_file_empty(product_file),
    ])


def generate_testdata() -> tuple[int, dict | None]:
    # Step 1: 產生 UUID
    code, uuid = generate_batch_uuid_with_code()
    if code != ResultCode.SUCCESS or not uuid:
        return ResultCode.UUID_GEN_FAIL, None

    # Step 2: 產生商品測資
    code, product = generate_fake_product()
    if code != ResultCode.SUCCESS or not product:
        return ResultCode.PRODUCT_GENERATION_FAILED, None

    # Step 3: 產生帳號測資
    code, user = generate_fake_user()
    if code != ResultCode.SUCCESS or not user:
        return ResultCode.USER_GENERATION_FAILED, None

    # Step 4: enrich UUID（工具模組）
    try:
        product = enrich_with_uuid(product, uuid)
    except Exception:
        return ResultCode.PRODUCT_UUID_ATTACH_FAILED, None

    try:
        user = enrich_with_uuid(user, uuid)
    except Exception:
        return ResultCode.USER_UUID_ATTACH_FAILED, None

    # Step 5: 存檔
    user_file = USER_PATH / f"{uuid}.json"
    product_file = PRODUCT_PATH / f"{uuid}.json"

    if save_json(user, user_file) != ResultCode.SUCCESS:
        return ResultCode.USER_TESTDATA_SAVE_FAILED, None

    if save_json(product, product_file) != ResultCode.SUCCESS:
        return ResultCode.PRODUCT_TESTDATA_SAVE_FAILED, None

    # Step 6: 成功
    return ResultCode.SUCCESS, {
        "uuid": uuid,
        "user_file": str(user_file),
        "product_file": str(product_file),
        "user": user,
        "product": product
    }
