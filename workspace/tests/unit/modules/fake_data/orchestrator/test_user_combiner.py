# 📦 測試工具
import pytest
from unittest.mock import patch, MagicMock

# 🧪 被測模組
from workspace.modules.fake_data.orchestrator.build_user_data_and_write import build_user_data_and_write

# ⚠️ 錯誤碼常數
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.combiner]


@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.get_user_path")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.ensure_dir")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.ensure_file")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.generate_user_data")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.save_json")
def test_build_user_data_success(mock_save, mock_gen, mock_file, mock_dir, mock_path):
    """
    測試整體流程成功，資料產生與儲存皆正常
    """
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()
    mock_dir.return_value = ResultCode.SUCCESS
    mock_file.return_value = ResultCode.SUCCESS
    mock_gen.return_value = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "12345678"
    }
    mock_save.return_value = ResultCode.SUCCESS

    result = build_user_data_and_write("abc123")
    assert result == ResultCode.SUCCESS


@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.get_user_path")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.ensure_dir")
def test_build_user_data_dir_fail(mock_dir, mock_path):
    """
    資料夾建立失敗，應直接回傳錯誤碼
    """
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()
    mock_dir.return_value = ResultCode.TOOL_DIR_CREATE_FAILED

    result = build_user_data_and_write("abc123")
    assert result == ResultCode.TOOL_DIR_CREATE_FAILED


@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.get_user_path")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.ensure_dir")
@patch("workspace.modules.fake_data.orchestrator.build_user_data_and_write.ensure_file")
def test_build_user_data_file_fail(mock_file, mock_dir, mock_path):
    """
    檔案建立失敗，應回傳錯誤碼
    """
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
def test_build_user_data_generate_fail(mock_gen, mock_file, mock_dir, mock_path):
    """
    模擬資料產生器失敗（回傳錯誤碼），應回傳 FAKER_GENERATE_FAILED
    """
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
    """
    模擬存檔失敗，應回傳對應錯誤
    """
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()
    mock_dir.return_value = ResultCode.SUCCESS
    mock_file.return_value = ResultCode.SUCCESS
    mock_gen.return_value = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "12345678"
    }
    mock_save.return_value = ResultCode.TOOL_FILE_WRITE_FAILED

    result = build_user_data_and_write("abc123")
    assert result == ResultCode.TOOL_FILE_WRITE_FAILED
