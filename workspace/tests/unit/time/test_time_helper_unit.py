import pytest
import datetime
from utils.time.time_helper import (
    get_time,
    wait_seconds,
    timestamp_to_iso,
    iso_to_timestamp
)

pytestmark = [pytest.mark.unit, pytest.mark.time]

def test_get_time_default_utc_str():
    """測試預設 UTC 時區格式化字串輸出"""
    value = get_time()
    assert isinstance(value, str)
    assert len(value) == 19  # YYYY-MM-DD HH:MM:SS

@pytest.mark.parametrize("tz", ["UTC", "Asia/Taipei", "local"])
def test_get_time_different_tz_str(tz):
    """測試不同時區字串輸出"""
    val = get_time(tz=tz)
    assert isinstance(val, str)
    assert len(val) > 10

def test_get_time_custom_format():
    """測試自訂格式字串輸出"""
    val = get_time(fmt="%d/%m/%Y-%H")
    assert "/" in val and "-" in val

@pytest.mark.parametrize("output, expected_type", [
    ("str", str),
    ("datetime", datetime.datetime),
    ("timestamp", float),
])
def test_get_time_output_types(output, expected_type):
    """測試不同 output 型態"""
    val = get_time(output=output)
    assert isinstance(val, expected_type)

def test_get_time_all_args():
    """全參數同時測試（Asia/Taipei, custom format, datetime output）"""
    result = get_time(tz="Asia/Taipei", fmt="%Y-%m-%d", output="datetime")
    assert isinstance(result, datetime.datetime)

def test_get_time_invalid_tz(monkeypatch):
    """異常：傳入無效時區，應拋錯"""
    with pytest.raises(Exception):
        get_time(tz="NotAZone")

def test_get_time_invalid_output():
    """異常：output 傳入不支援值"""
    with pytest.raises(Exception):
        get_time(output="badtype")

def test_get_time_invalid_format():
    """異常：fmt 格式錯誤（strftime 應拋 ValueError）"""
    with pytest.raises(ValueError):
        get_time(fmt="%%%QQQ")

def test_iso_to_timestamp_and_back():
    """ISO 與 timestamp 互轉驗證"""
    now = get_time(output="datetime")
    iso = now.isoformat()
    ts = iso_to_timestamp(iso)
    # 時間戳相差不得超過 1 秒
    assert abs(now.timestamp() - ts) < 1

def test_timestamp_to_iso_type():
    """timestamp_to_iso 型態驗證"""
    ts = 1716898800
    iso = timestamp_to_iso(ts, tz="Asia/Taipei")
    assert isinstance(iso, str)
    assert "T" in iso

def test_wait_seconds(monkeypatch):
    """wait_seconds 只驗證 sleep 被呼叫（不實際等待）"""
    called = {"flag": False}
    def fake_sleep(sec):
        called["flag"] = True
        assert sec == 2
    monkeypatch.setattr("time.sleep", fake_sleep)
    wait_seconds(2)
    assert called["flag"] is True

def test_timestamp_to_iso_invalid_tz():
    """timestamp_to_iso 異常：無效時區"""
    with pytest.raises(Exception):
        timestamp_to_iso(1716898800, tz="NoSuchZone")

def test_iso_to_timestamp_invalid():
    """iso_to_timestamp 異常：非法格式"""
    with pytest.raises(ValueError):
        iso_to_timestamp("bad-format")
