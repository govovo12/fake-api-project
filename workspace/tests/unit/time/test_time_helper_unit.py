import sys
import pytest
from workspace.config.rules.error_codes import ResultCode
from utils.time.time_helper import (
    get_time,
    timestamp_to_iso,
    iso_to_timestamp,
    wait_seconds,
)

pytestmark = [pytest.mark.unit, pytest.mark.time]


def test_get_time_default_utc_str():
    """✅ 預設不帶參數，回傳 UTC 時區格式化字串"""
    val = get_time()
    assert isinstance(val, str)
    assert len(val) == 19  # YYYY-MM-DD HH:MM:SS


@pytest.mark.parametrize("tz", ["UTC", "Asia/Taipei", "local"])
def test_get_time_various_tz_str(tz):
    """✅ 傳入不同時區，皆可正常回傳格式化字串"""
    val = get_time(tz=tz)
    assert isinstance(val, str)
    assert len(val) > 10


def test_get_time_custom_format():
    """✅ 自訂格式輸出成功"""
    val = get_time(fmt="%d/%m/%Y-%H")
    assert "/" in val and "-" in val


@pytest.mark.parametrize("output, expected_type", [
    ("str", str),
    ("datetime", object),
    ("timestamp", (int, float)),
])
def test_get_time_output_types(output, expected_type):
    """✅ 測試不同輸出型態回傳正確"""
    val = get_time(output=output)
    assert isinstance(val, expected_type)


def test_get_time_invalid_tz_returns_error_code():
    """💥 傳入無效時區，回傳錯誤碼"""
    result = get_time(tz="Invalid/Timezone")
    assert result == ResultCode.TOOL_TIME_INVALID_TIMEZONE


def test_get_time_invalid_output_returns_error_code():
    """💥 傳入不支援的 output 參數，回傳錯誤碼"""
    result = get_time(output="unknown")
    assert result == ResultCode.TOOL_TIME_UNSUPPORTED_OUTPUT


def test_get_time_invalid_format_returns_error_code():
    """💥 使用非法格式（如 %Q）應回傳錯誤碼"""
    result = get_time(fmt="%Q")  # %Q 是非法格式
    assert result == ResultCode.TOOL_TIME_INVALID_FORMAT 



def test_get_time_without_zoneinfo(monkeypatch):
    """💥 模擬無 zoneinfo 模組，強制走 pytz 分支"""
    monkeypatch.delitem(sys.modules, "zoneinfo", raising=False)
    val = get_time(tz="UTC")
    assert isinstance(val, str)


def test_timestamp_to_iso_valid():
    """✅ timestamp_to_iso 正常回傳 ISO 格式字串"""
    val = timestamp_to_iso(1716898800, tz="UTC")
    assert isinstance(val, str)
    assert "T" in val


def test_timestamp_to_iso_invalid_timezone():
    """💥 傳入錯誤時區字串，回傳錯誤碼"""
    result = timestamp_to_iso(1716898800, tz="Invalid/Timezone")
    assert result == ResultCode.TOOL_TIME_INVALID_TIMEZONE


def test_timestamp_to_iso_invalid_timezone():
    result = timestamp_to_iso(1234567890, tz="Invalid/Timezone")
    assert result == ResultCode.TOOL_TIME_INVALID_TIMEZONE




def test_iso_to_timestamp_valid():
    """✅ ISO 字串成功轉 timestamp"""
    now = get_time(output="datetime")
    iso_str = now.isoformat()
    ts = iso_to_timestamp(iso_str)
    assert isinstance(ts, float) or isinstance(ts, int)


def test_iso_to_timestamp_invalid_format_returns_error_code():
    """💥 傳入錯誤格式 ISO 字串，回傳錯誤碼"""
    result = iso_to_timestamp("bad-format")
    assert result == ResultCode.TOOL_TIME_INVALID_FORMAT


def test_wait_seconds_positive(monkeypatch):
    """✅ 測試 wait_seconds 正常等待，使用 monkeypatch 避免實際等待"""
    called = {"flag": False}

    def fake_sleep(sec):
        called["flag"] = True
        assert sec == 2

    monkeypatch.setattr("time.sleep", fake_sleep)
    result = wait_seconds(2)
    assert called["flag"] is True
    assert result == ResultCode.SUCCESS


def test_wait_seconds_negative():
    """💥 負秒數輸入回傳錯誤碼"""
    result = wait_seconds(-5)
    assert result != ResultCode.SUCCESS
