import pytest
from unittest.mock import mock_open, patch
from pathlib import Path
from utils.logger.log_writer import write_log
from utils.logger.logger import format_log_message
from utils.mock.mock_helper import mock_function

pytestmark = [pytest.mark.unit, pytest.mark.log]

# -------------------------
# 測試 write_log (log_writer)
# -------------------------

class TestLogWriter:
    """log_writer 單元測試：只關心檔案寫入行為（不管格式）"""

    def test_write_log_appends_newline(self):
        """應自動補上換行字元"""
        mock_file = mock_open()
        message = "訊息"
        log_path = Path("mock_path.log")
        with patch("pathlib.Path.open", mock_file):
            write_log(log_path, message)
        mock_file().write.assert_called_once_with("訊息\n")

    def test_write_log_empty_message(self):
        """空訊息也會寫入換行"""
        mock_file = mock_open()
        with patch("pathlib.Path.open", mock_file):
            write_log(Path("mock_path.log"), "")
        mock_file().write.assert_called_once_with("\n")

    def test_write_log_special_characters(self):
        """支援特殊字元寫入"""
        mock_file = mock_open()
        msg = "特殊字元\n\t!@#"
        with patch("pathlib.Path.open", mock_file):
            write_log(Path("mock_path.log"), msg)
        mock_file().write.assert_called_once_with("特殊字元\n\t!@#\n")

    def test_write_log_large_message(self):
        """大型訊息不會出錯"""
        mock_file = mock_open()
        msg = "A" * 10000
        with patch("pathlib.Path.open", mock_file):
            write_log(Path("mock_path.log"), msg)
        mock_file().write.assert_called_once_with(msg + "\n")

    def test_write_log_multiple_calls(self):
        """多次寫入各自 append"""
        mock_file = mock_open()
        msgs = ["first", "second", "third"]
        with patch("pathlib.Path.open", mock_file):
            for m in msgs:
                write_log(Path("mock_path.log"), m)
        assert mock_file().write.call_count == 3
        for m in msgs:
            mock_file().write.assert_any_call(m + "\n")

# ---------------------------
# 測試 format_log_message (logger)
# ---------------------------

def test_format_log_message_basic():
    """標準格式組裝"""
    result = format_log_message("INFO", "Test message", "2024-01-01 12:00:00")
    assert result == "[2024-01-01 12:00:00] [INFO] Test message"

def test_format_log_message_empty():
    """全空輸入也能產生結果"""
    assert format_log_message("", "", "") == "[] [] "

def test_format_log_message_edge_level():
    """level 亂碼也支援"""
    msg = format_log_message("!@#$", "Edge case message", "2025-05-29 00:00:00")
    assert msg == "[2025-05-29 00:00:00] [!@#$] Edge case message"

def test_format_log_message_special_characters():
    """訊息帶有特殊字元亦正常"""
    msg = format_log_message("DEBUG", "Message with \n new line", "2025-05-29 12:00:00")
    assert msg == "[2025-05-29 12:00:00] [DEBUG] Message with \n new line"

def test_format_log_message_long_text():
    """超長內容無誤"""
    long_message = "A" * 1000
    msg = format_log_message("INFO", long_message, "2025-05-29 12:00:00")
    assert msg.startswith("[2025-05-29 12:00:00] [INFO] AAAAA")

def test_format_log_message_with_mocked_timestamp():
    """timestamp 可被 mock injection"""
    fake_time = mock_function("MOCK_TIME")
    msg = format_log_message("MOCK", "Log entry", fake_time())
    assert msg == "[MOCK_TIME] [MOCK] Log entry"
