import pytest
from io import StringIO
from contextlib import redirect_stdout
from workspace.utils.logger.log_helper import log_simple_result
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.log]

def capture_output(func, *args, **kwargs):
    """
    捕捉 print 輸出的輔助函式
    """
    buffer = StringIO()
    with redirect_stdout(buffer):
        func(*args, **kwargs)
    return buffer.getvalue().strip()

def test_log_simple_result_success_code_0():
    """
    測試成功碼 SUCCESS（0）應輸出對應成功訊息
    """
    output = capture_output(log_simple_result, ResultCode.SUCCESS)
    assert "✅ 成功" in output
    assert "(code=0, msg=操作成功)" in output

def test_log_simple_result_success_code_10000():
    """
    測試成功碼 TASK_USER_TESTDATA_GENERATED（10000）應輸出對應訊息
    """
    output = capture_output(log_simple_result, ResultCode.TESTDATA_TASK_SUCCESS)
    assert "✅ 成功" in output
    assert f"(code=10000, msg={ResultCode.ERROR_MESSAGES[ResultCode.TESTDATA_TASK_SUCCESS]})" in output


def test_log_simple_result_failure_known_error():
    """
    測試已知錯誤碼應正確顯示失敗訊息
    """
    output = capture_output(log_simple_result, ResultCode.TOOL_FILE_WRITE_FAILED)
    assert "❌ 失敗" in output
    assert f"(code={ResultCode.TOOL_FILE_WRITE_FAILED}, msg={ResultCode.ERROR_MESSAGES[ResultCode.TOOL_FILE_WRITE_FAILED]})" in output

def test_log_simple_result_failure_unknown_error():
    """
    測試未知錯誤碼應顯示「未知錯誤」
    """
    output = capture_output(log_simple_result, 99999)
    assert "❌ 失敗" in output
    assert "(code=99999, msg=未知錯誤)" in output
