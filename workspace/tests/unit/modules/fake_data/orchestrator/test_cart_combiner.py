import pytest
from unittest.mock import patch, MagicMock
from workspace.modules.fake_data.orchestrator.build_cart_data_and_write import build_cart_data_and_write
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.orchestrator]


@patch("workspace.modules.fake_data.orchestrator.build_cart_data_and_write.get_cart_path")
@patch("workspace.modules.fake_data.orchestrator.build_cart_data_and_write.ensure_dir")
@patch("workspace.modules.fake_data.orchestrator.build_cart_data_and_write.ensure_file")
@patch("workspace.modules.fake_data.orchestrator.build_cart_data_and_write.generate_cart_data")
@patch("workspace.modules.fake_data.orchestrator.build_cart_data_and_write.save_json")
def test_build_cart_data_success(mock_save, mock_gen, mock_file, mock_dir, mock_path):
    """測試整體流程成功"""
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()

    mock_dir.return_value = ResultCode.SUCCESS
    mock_file.return_value = ResultCode.SUCCESS
    mock_gen.return_value = {
        "userId": 1,
        "date": "2025-06-20",
        "products": [{"productId": 7, "quantity": 2}]
    }
    mock_save.return_value = ResultCode.SUCCESS

    result = build_cart_data_and_write("abc123")
    assert result == ResultCode.SUCCESS


@patch("workspace.modules.fake_data.orchestrator.build_cart_data_and_write.get_cart_path")
@patch("workspace.modules.fake_data.orchestrator.build_cart_data_and_write.ensure_dir")
def test_build_cart_data_dir_fail(mock_dir, mock_path):
    """測試資料夾建立失敗"""
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()
    mock_dir.return_value = ResultCode.TOOL_DIR_CREATE_FAILED

    result = build_cart_data_and_write("abc123")
    assert result == ResultCode.TOOL_DIR_CREATE_FAILED


@patch("workspace.modules.fake_data.orchestrator.build_cart_data_and_write.get_cart_path")
@patch("workspace.modules.fake_data.orchestrator.build_cart_data_and_write.ensure_dir")
@patch("workspace.modules.fake_data.orchestrator.build_cart_data_and_write.ensure_file")
def test_build_cart_data_file_fail(mock_file, mock_dir, mock_path):
    """測試檔案建立失敗"""
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()
    mock_dir.return_value = ResultCode.SUCCESS
    mock_file.return_value = ResultCode.TOOL_FILE_CREATE_FAILED

    result = build_cart_data_and_write("abc123")
    assert result == ResultCode.TOOL_FILE_CREATE_FAILED


@patch("workspace.modules.fake_data.orchestrator.build_cart_data_and_write.get_cart_path")
@patch("workspace.modules.fake_data.orchestrator.build_cart_data_and_write.ensure_dir")
@patch("workspace.modules.fake_data.orchestrator.build_cart_data_and_write.ensure_file")
@patch("workspace.modules.fake_data.orchestrator.build_cart_data_and_write.generate_cart_data")
def test_build_cart_data_generation_fail(mock_gen, mock_file, mock_dir, mock_path):
    """測試測資產生失敗（回傳非 dict）"""
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()
    mock_dir.return_value = ResultCode.SUCCESS
    mock_file.return_value = ResultCode.SUCCESS
    mock_gen.return_value = None  # 非 dict 即為錯誤

    result = build_cart_data_and_write("abc123")
    assert result == ResultCode.CART_GENERATION_FAILED


@patch("workspace.modules.fake_data.orchestrator.build_cart_data_and_write.get_cart_path")
@patch("workspace.modules.fake_data.orchestrator.build_cart_data_and_write.ensure_dir")
@patch("workspace.modules.fake_data.orchestrator.build_cart_data_and_write.ensure_file")
@patch("workspace.modules.fake_data.orchestrator.build_cart_data_and_write.generate_cart_data")
@patch("workspace.modules.fake_data.orchestrator.build_cart_data_and_write.save_json")
def test_build_cart_data_save_fail(mock_save, mock_gen, mock_file, mock_dir, mock_path):
    """測試測資寫入失敗"""
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()
    mock_dir.return_value = ResultCode.SUCCESS
    mock_file.return_value = ResultCode.SUCCESS
    mock_gen.return_value = {
        "userId": 3,
        "date": "2025-06-19",
        "products": [{"productId": 2, "quantity": 4}]
    }
    mock_save.return_value = ResultCode.TOOL_FILE_WRITE_FAILED

    result = build_cart_data_and_write("abc123")
    assert result == ResultCode.TOOL_FILE_WRITE_FAILED
