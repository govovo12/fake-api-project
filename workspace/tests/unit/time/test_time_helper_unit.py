# workspace/tests/unit/time/test_time_helper_unit.py

import pytest
import datetime
from workspace.utils.time import time_helper
from utils.mock.mock_helper import mock_function

real_datetime = datetime.datetime  # 保留原始 datetime

pytestmark = [pytest.mark.unit, pytest.mark.time]


def test_get_current_timestamp(monkeypatch):
    # stub time.time 為固定值
    time_stub = mock_function(return_value=1716898800)
    monkeypatch.setattr("time.time", time_stub)
    assert time_helper.get_current_timestamp() == 1716898800


def test_get_current_iso(monkeypatch):
    # stub datetime.datetime.utcnow
    class MockDatetime(datetime.datetime):
        @staticmethod
        def utcnow():
            return real_datetime(2024, 6, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
    monkeypatch.setattr(datetime, "datetime", MockDatetime)
    result = time_helper.get_current_iso()
    assert result.startswith("2024-06-01T12:00:00")


def test_timestamp_to_iso(monkeypatch):
    # stub datetime.datetime.utcfromtimestamp
    class MockDatetime(datetime.datetime):
        @staticmethod
        def utcfromtimestamp(ts):
            return real_datetime(2024, 6, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
    monkeypatch.setattr(datetime, "datetime", MockDatetime)
    iso = time_helper.timestamp_to_iso(1716898800)
    assert iso.startswith("2024-06-01T12:00:00")


def test_iso_to_timestamp():
    iso = "2024-06-01T12:00:00Z"
    ts = time_helper.iso_to_timestamp(iso)
    assert ts == 1717243200


def test_wait_seconds(monkeypatch):
    # stub time.sleep 為 noop 並記錄呼叫參數
    sleep_stub = mock_function()
    monkeypatch.setattr("time.sleep", sleep_stub)
    time_helper.wait_seconds(3.5)
    assert sleep_stub.call_count == 1
    assert sleep_stub.call_args_list[0][0][0] == 3.5
