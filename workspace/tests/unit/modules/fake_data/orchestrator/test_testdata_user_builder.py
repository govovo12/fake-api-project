import pytest
from utils.mock.mock_helper import get_mock
from workspace.config.rules.error_codes import ResultCode

# ✅ pytest 標記：單元 + 測資模組
pytestmark = [pytest.mark.unit, pytest.mark.testdata]

# ✅ 固定 UUID fixture
@pytest.fixture
def mock_uuid():
    return "mock-user-uuid"

# ✅ Case 1：模擬 generate_user_data 失敗
def test_generate_user_fail(mocker, mock_uuid):
    mock_gen = get_mock("mock_function", return_value=(8888, None, {"reason": "gen_user_failed"}))
    mocker.patch("workspace.modules.fake_data.orchestrator.testdata_user_builder.generate_user_data", mock_gen)

    from workspace.modules.fake_data.orchestrator.testdata_user_builder import build_user_data
    code, data, meta = build_user_data(mock_uuid)

    assert mock_gen.called
    assert code == 8888
    assert data is None
    assert isinstance(meta, dict)
    assert meta["reason"] == "gen_user_failed"

# ✅ Case 2：模擬 enrich_with_uuid 失敗
def test_enrich_user_uuid_fail(mocker, mock_uuid):
    fake_user = {"email": "test@example.com"}
    mock_gen = get_mock("mock_function", return_value=(0, fake_user, None))
    mock_enrich = get_mock("mock_function", return_value=(False, None, {"reason": "missing_user_field"}))

    mocker.patch("workspace.modules.fake_data.orchestrator.testdata_user_builder.generate_user_data", mock_gen)
    mocker.patch("workspace.modules.fake_data.orchestrator.testdata_user_builder.enrich_with_uuid", mock_enrich)

    from workspace.modules.fake_data.orchestrator.testdata_user_builder import build_user_data
    code, data, meta = build_user_data(mock_uuid)

    assert mock_enrich.called
    args, _ = mock_enrich.call_args
    assert args[0] == fake_user
    assert args[1] == mock_uuid

    assert code == ResultCode.USER_UUID_ATTACH_FAILED
    assert data is None
    assert isinstance(meta, dict)
    assert meta["reason"] == "missing_user_field"

# ✅ Case 3：成功流程
def test_success_user_build(mocker, mock_uuid):
    fake_user = {"email": "test@example.com"}
    enriched_user = {"email": "test@example.com", "uuid": mock_uuid}

    mock_gen = get_mock("mock_function", return_value=(0, fake_user, None))
    mock_enrich = get_mock("mock_function", return_value=(True, enriched_user, None))

    mocker.patch("workspace.modules.fake_data.orchestrator.testdata_user_builder.generate_user_data", mock_gen)
    mocker.patch("workspace.modules.fake_data.orchestrator.testdata_user_builder.enrich_with_uuid", mock_enrich)

    from workspace.modules.fake_data.orchestrator.testdata_user_builder import build_user_data
    code, data, meta = build_user_data(mock_uuid)

    args, _ = mock_enrich.call_args
    assert args[0] == fake_user
    assert args[1] == mock_uuid

    assert code == ResultCode.SUCCESS
    assert data == enriched_user
    assert meta is None
