import pytest
from utils.mock.mock_helper import get_mock
from workspace.config.rules.error_codes import ResultCode

# ✅ pytest 標記：單元 + 測資模組
pytestmark = [pytest.mark.unit, pytest.mark.testdata]

# ✅ 固定 UUID fixture（可複用）
@pytest.fixture
def mock_uuid():
    return "mock-product-uuid"

# ✅ Case 1：模擬 generate_product_data 失敗（Step 1）
def test_generate_product_fail(mocker, mock_uuid):
    # 模擬 Step 1 回傳錯誤
    mock_gen = get_mock("mock_function", return_value=(9999, None, {"reason": "gen_failed"}))
    mocker.patch("workspace.modules.fake_data.orchestrator.testdata_product_builder.generate_product_data", mock_gen)

    from workspace.modules.fake_data.orchestrator.testdata_product_builder import build_product_data
    code, data, meta = build_product_data(mock_uuid)

    assert mock_gen.called
    assert code == 9999
    assert data is None
    assert isinstance(meta, dict)
    assert meta["reason"] == "gen_failed"

# ✅ Case 2：模擬 enrich_with_uuid 失敗（Step 2）
def test_enrich_product_uuid_fail(mocker, mock_uuid):
    # Step 1 mock 回成功資料
    mock_gen = get_mock("mock_function", return_value=(0, {"title": "some item"}, None))
    # Step 2 模擬 enrich UUID 失敗
    mock_enrich = get_mock("mock_function", return_value=(False, None, {"reason": "missing_product_field"}))

    mocker.patch("workspace.modules.fake_data.orchestrator.testdata_product_builder.generate_product_data", mock_gen)
    mocker.patch("workspace.modules.fake_data.orchestrator.testdata_product_builder.enrich_with_uuid", mock_enrich)

    from workspace.modules.fake_data.orchestrator.testdata_product_builder import build_product_data
    code, data, meta = build_product_data(mock_uuid)

    # 🔍 驗參數
    assert mock_enrich.called
    args, _ = mock_enrich.call_args
    assert isinstance(args[0], dict)  # product_data
    assert args[1] == mock_uuid       # UUID 傳入是否正確

    # 🔍 驗錯誤碼與 meta
    assert code == ResultCode.PRODUCT_UUID_ATTACH_FAILED
    assert data is None
    assert isinstance(meta, dict)
    assert meta["reason"] == "missing_product_field"

# ✅ Case 3：成功流程
def test_success_product_build(mocker, mock_uuid):
    fake_product = {"title": "item"}
    enriched_product = {"title": "item", "uuid": mock_uuid}

    mock_gen = get_mock("mock_function", return_value=(0, fake_product, None))
    mock_enrich = get_mock("mock_function", return_value=(True, enriched_product, None))

    mocker.patch("workspace.modules.fake_data.orchestrator.testdata_product_builder.generate_product_data", mock_gen)
    mocker.patch("workspace.modules.fake_data.orchestrator.testdata_product_builder.enrich_with_uuid", mock_enrich)

    from workspace.modules.fake_data.orchestrator.testdata_product_builder import build_product_data
    code, data, meta = build_product_data(mock_uuid)

    # 🔍 驗 enrich 參數是否正確
    args, _ = mock_enrich.call_args
    assert args[0] == fake_product
    assert args[1] == mock_uuid

    # 🔍 驗整體輸出
    assert code == ResultCode.SUCCESS
    assert data == enriched_product
    assert meta is None
