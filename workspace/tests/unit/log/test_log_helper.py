import pytest
from io import StringIO
from contextlib import redirect_stdout

from workspace.utils.logger.log_helper import log_simple_result
from workspace.config.rules import error_codes
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.log]

ERROR_MESSAGES = error_codes.ERROR_MESSAGES


def capture_print_output(func, *args, **kwargs) -> str:
    """輔助函式：捕捉 print() 輸出內容"""
    buffer = StringIO()
    with redirect_stdout(buffer):
        func(*args, **kwargs)
    return buffer.getvalue().strip()


def test_success_code_prints_success_status():
    """✅ 測試成功碼輸出 ✅ 成功"""
    output = capture_print_output(log_simple_result, ResultCode.CREATE_PRODUCT_SUCCESS)
    assert "✅ 成功" in output
    assert f"(code={ResultCode.CREATE_PRODUCT_SUCCESS}" in output
    assert "商品建構成功" in output


def test_tool_error_code_prints_tool_status():
    """❌ 測試工具錯誤碼輸出 ❌ 工具錯誤"""
    output = capture_print_output(log_simple_result, ResultCode.TOOL_FILE_WRITE_FAILED)
    assert "❌ 工具錯誤" in output
    assert f"(code={ResultCode.TOOL_FILE_WRITE_FAILED}" in output
    assert "寫入檔案失敗" in output


def test_task_error_code_prints_task_status():
    """▲ 測試任務錯誤碼輸出 ▲ 任務錯誤"""
    output = capture_print_output(log_simple_result, ResultCode.CREATE_PRODUCT_FAILED)
    assert "▲ 任務錯誤" in output
    assert f"(code={ResultCode.CREATE_PRODUCT_FAILED}" in output
    assert "商品建立失敗" in output


def test_generic_error_code_prints_generic_status():
    """❓ 測試通用錯誤碼輸出 ❓ 通用錯誤"""
    output = capture_print_output(log_simple_result, ResultCode.GENERIC_ERROR)
    assert "❓ 通用錯誤" in output
    assert f"(code={ResultCode.GENERIC_ERROR}" in output
    assert "未知錯誤" in output


def test_unknown_error_code_fallback():
    """❓ 測試未知錯誤碼應 fallback 為 '未知錯誤' + ❓ 未知類型"""
    unknown_code = 999999
    output = capture_print_output(log_simple_result, unknown_code)
    assert "❓ 未知類型" in output
    assert f"(code={unknown_code}" in output
    assert "未知錯誤" in output


def test_message_missing_fallback(monkeypatch):
    """🧪 測試錯誤碼存在但訊息為 None 時 fallback 為 '未知錯誤'"""
    monkeypatch.setitem(ERROR_MESSAGES, 88888, None)
    output = capture_print_output(log_simple_result, 88888)
    assert "❓ 未知類型" in output
    assert "未知錯誤" in output


def test_context_appends_to_output():
    """🧪 測試 context 能正常附加在輸出末尾"""
    output = capture_print_output(
        log_simple_result, ResultCode.SUCCESS, context="建構流程結束"
    )
    assert "建構流程結束" in output


def test_logger_info_is_called(caplog):
    """🧪 測試 logger 是否同步寫入 log"""
    with caplog.at_level("INFO"):
        log_simple_result(ResultCode.SUCCESS, context="模擬寫入")
        matched = any("模擬寫入" in msg for msg in caplog.messages)
        assert matched


def test_combined_success_code_and_message():
    """🧪 測試完整輸出格式含狀態、錯誤碼、訊息"""
    output = capture_print_output(log_simple_result, ResultCode.SUCCESS)
    assert "[✅ 成功]" in output
    assert "msg=操作成功" in output
