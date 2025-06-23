# 📦 測試工具
import pytest
from unittest.mock import patch, MagicMock

# 🧪 被測模組
from workspace.modules.fake_data.orchestrator.build_product_data_and_write import build_product_data_and_write

# ⚠️ 錯誤碼常數
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.combiner]


@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.get_product_path")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.ensure_dir")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.ensure_file")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.generate_product_data")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.save_json")
def test_build_product_data_success(mock_save, mock_gen, mock_file, mock_dir, mock_path):
    """
    測試整體流程成功，應正確產生並儲存商品資料
    """
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()
    mock_dir.return_value = ResultCode.SUCCESS
    mock_file.return_value = ResultCode.SUCCESS
    mock_gen.return_value = {
        "title": "Test Product",
        "price": 99.99,
        "description": "sampledata",
        "image": "https://example.com",
        "category": "jewelery"
    }
    mock_save.return_value = ResultCode.SUCCESS

    result = build_product_data_and_write("abc123")
    assert result == ResultCode.SUCCESS


@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.get_product_path")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.ensure_dir")
def test_build_product_data_dir_fail(mock_dir, mock_path):
    """
    資料夾建立失敗，應立即回傳對應錯誤碼
    """
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()
    mock_dir.return_value = ResultCode.TOOL_DIR_CREATE_FAILED

    result = build_product_data_and_write("abc123")
    assert result == ResultCode.TOOL_DIR_CREATE_FAILED


@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.get_product_path")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.ensure_dir")
@patch("workspace.modules.fake_data.orchestrator.build_product_data_and_write.ensure_file")
def test_build_product_data_file_fail(mock_file, mock_dir, mock_path):
    """
    檔案建立失敗，應回傳對應錯誤碼
    """
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
def test_build_product_data_generate_fail(mock_gen, mock_file, mock_dir, mock_path):
    """
    測試商品資料產生失敗（回傳錯誤碼），應轉換為 PRODUCT_GENERATION_FAILED
    """
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
    """
    測試商品資料存檔失敗，應回傳 TOOL_FILE_WRITE_FAILED
    """
    mock_path.return_value = MagicMock()
    mock_path.return_value.parent = MagicMock()
    mock_dir.return_value = ResultCode.SUCCESS
    mock_file.return_value = ResultCode.SUCCESS
    mock_gen.return_value = {
        "title": "Another Product",
        "price": 25.00,
        "description": "aaaaaaa",
        "image": "https://test.com",
        "category": "electronics"
    }
    mock_save.return_value = ResultCode.TOOL_FILE_WRITE_FAILED

    result = build_product_data_and_write("abc123")
    assert result == ResultCode.TOOL_FILE_WRITE_FAILED
