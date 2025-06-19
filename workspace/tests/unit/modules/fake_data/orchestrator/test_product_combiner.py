import pytest
from unittest.mock import patch, MagicMock
from workspace.modules.fake_data.orchestrator.build_product_data_and_write import build_product_data_and_write
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.orchestrator]

# ✅ 結構性測試：build_product_data_and_write 是否正確串接底層模組

@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.get_product_path")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.ensure_dir")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.ensure_file")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.generate_product_data")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.save_json")
def test_build_product_data_success(mock_save, mock_gen, mock_file, mock_dir, mock_path):
    """測試整體流程成功，應回傳 SUCCESS"""
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()

    mock_dir.return_value = ResultCode.SUCCESS
    mock_file.return_value = ResultCode.SUCCESS
    mock_gen.return_value = {
        "title": "Item",
        "price": 99.9,
        "description": "test desc",
        "image": "url",
        "category": "Clothes"
    }
    mock_save.return_value = ResultCode.SUCCESS

    result = build_product_data_and_write("abc123")
    assert result == ResultCode.SUCCESS

@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.get_product_path")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.ensure_dir")
def test_build_product_data_dir_fail(mock_dir, mock_path):
    """測試資料夾建立失敗"""
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()
    mock_dir.return_value = ResultCode.TOOL_DIR_CREATE_FAILED

    result = build_product_data_and_write("abc123")
    assert result == ResultCode.TOOL_DIR_CREATE_FAILED

@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.get_product_path")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.ensure_dir")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.ensure_file")
def test_build_product_data_file_fail(mock_file, mock_dir, mock_path):
    """測試檔案建立失敗"""
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()
    mock_dir.return_value = ResultCode.SUCCESS
    mock_file.return_value = ResultCode.TOOL_FILE_CREATE_FAILED

    result = build_product_data_and_write("abc123")
    assert result == ResultCode.TOOL_FILE_CREATE_FAILED

@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.get_product_path")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.ensure_dir")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.ensure_file")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.generate_product_data")
def test_build_product_data_generation_fail(mock_gen, mock_file, mock_dir, mock_path):
    """測試測資產生失敗"""
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()
    mock_dir.return_value = ResultCode.SUCCESS
    mock_file.return_value = ResultCode.SUCCESS
    mock_gen.return_value = ResultCode.PRODUCT_GENERATION_FAILED

    result = build_product_data_and_write("abc123")
    assert result == ResultCode.PRODUCT_GENERATION_FAILED

@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.get_product_path")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.ensure_dir")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.ensure_file")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.generate_product_data")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.save_json")
def test_build_product_data_save_fail(mock_save, mock_gen, mock_file, mock_dir, mock_path):
    """測試寫入測資失敗"""
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()
    mock_dir.return_value = ResultCode.SUCCESS
    mock_file.return_value = ResultCode.SUCCESS
    mock_gen.return_value = {
        "title": "X",
        "price": 0,
        "description": "d",
        "image": "i",
        "category": "test"
    }
    mock_save.return_value = ResultCode.TOOL_FILE_WRITE_FAILED

    result = build_product_data_and_write("abc123")
    assert result == ResultCode.TOOL_FILE_WRITE_FAILED
