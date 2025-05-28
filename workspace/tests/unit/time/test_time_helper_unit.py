import pytest
import datetime
from workspace.utils.time import time_helper

real_datetime = datetime.datetime  # 保留原始 datetime 以供 mock 使用

@pytest.mark.time
def test_get_current_timestamp(monkeypatch):
    monkeypatch.setattr("time.time", lambda: 1716898800)
    assert time_helper.get_current_timestamp() == 1716898800

@pytest.mark.time
def test_get_current_iso(monkeypatch):
    class MockDatetime(datetime.datetime):
        @staticmethod
        def utcnow():
            return real_datetime(2024, 6, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)

    monkeypatch.setattr(datetime, "datetime", MockDatetime)
    result = time_helper.get_current_iso()
    assert result.startswith("2024-06-01T12:00:00")

@pytest.mark.time
def test_timestamp_to_iso(monkeypatch):
    class MockDatetime(datetime.datetime):
        @staticmethod
        def utcfromtimestamp(ts):
            return real_datetime(2024, 6, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)

    monkeypatch.setattr(datetime, "datetime", MockDatetime)
    iso = time_helper.timestamp_to_iso(1716898800)
    assert iso.startswith("2024-06-01T12:00:00")

@pytest.mark.time
def test_iso_to_timestamp():
    iso = "2024-06-01T12:00:00Z"
    ts = time_helper.iso_to_timestamp(iso)
    assert ts == 1717243200  # UTC 2024-06-01 12:00:00

@pytest.mark.time
def test_wait_seconds(monkeypatch):
    called = {}
    monkeypatch.setattr("time.sleep", lambda x: called.setdefault("slept", x))
    time_helper.wait_seconds(3.5)
    assert called["slept"] == 3.5