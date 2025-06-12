import pytest
from unittest.mock import patch, MagicMock
from workspace.modules.fake_data.orchestrator.build_user_data_and_write import build_user_data_and_write
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.combiner]

# ✅ 結構性測試：build_user_data_and_write 是否正確串接底層模組

@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.get_user_path")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.ensure_dir")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.ensure_file")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.generate_user_data")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.save_json")
def test_build_user_data_success(mock_save, mock_gen, mock_file, mock_dir, mock_path):
    """測試整體流程成功"""
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()

    mock_dir.return_value = ResultCode.SUCCESS
    mock_file.return_value = ResultCode.SUCCESS
    mock_gen.return_value = {"name": "tony", "email": "a@b.com", "password": "12345678"}
    mock_save.return_value = ResultCode.SUCCESS

    result = build_user_data_and_write("abc123")
    assert result == ResultCode.SUCCESS

@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.get_user_path")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.ensure_dir")
def test_build_user_data_dir_fail(mock_dir, mock_path):
    """測試資料夾建立失敗"""
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()
    mock_dir.return_value = ResultCode.TOOL_DIR_CREATE_FAILED

    result = build_user_data_and_write("abc123")
    assert result == ResultCode.TOOL_DIR_CREATE_FAILED

@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.get_user_path")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.ensure_dir")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.ensure_file")
def test_build_user_data_file_fail(mock_file, mock_dir, mock_path):
    """測試檔案建立失敗"""
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()
    mock_dir.return_value = ResultCode.SUCCESS
    mock_file.return_value = ResultCode.TOOL_FILE_CREATE_FAILED

    result = build_user_data_and_write("abc123")
    assert result == ResultCode.TOOL_FILE_CREATE_FAILED

@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.get_user_path")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.ensure_dir")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.ensure_file")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.generate_user_data")
def test_build_user_data_generation_fail(mock_gen, mock_file, mock_dir, mock_path):
    """測試測資產生失敗"""
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()
    mock_dir.return_value = ResultCode.SUCCESS
    mock_file.return_value = ResultCode.SUCCESS
    mock_gen.return_value = ResultCode.FAKER_GENERATE_FAILED

    result = build_user_data_and_write("abc123")
    assert result == ResultCode.FAKER_GENERATE_FAILED

@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.get_user_path")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.ensure_dir")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.ensure_file")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.generate_user_data")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.save_json")
def test_build_user_data_save_fail(mock_save, mock_gen, mock_file, mock_dir, mock_path):
    """測試測資寫入失敗"""
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()
    mock_dir.return_value = ResultCode.SUCCESS
    mock_file.return_value = ResultCode.SUCCESS
    mock_gen.return_value = {"name": "tony", "email": "a@b.com", "password": "12345678"}
    mock_save.return_value = ResultCode.TOOL_FILE_WRITE_FAILED

    result = build_user_data_and_write("abc123")
    assert result == ResultCode.TOOL_FILE_WRITE_FAILED
