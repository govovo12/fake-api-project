import datetime
import time

def get_current_timestamp() -> int:
    """取得目前 UTC 時間戳（秒）"""
    return int(time.time())

def get_current_iso() -> str:
    """取得目前 UTC ISO 格式字串（Z 結尾）"""
    return datetime.datetime.utcnow().isoformat() + "Z"

def timestamp_to_iso(ts: int) -> str:
    """時間戳轉換為 ISO 格式"""
    return datetime.datetime.utcfromtimestamp(ts).isoformat() + "Z"

def iso_to_timestamp(iso_str: str) -> int:
    """ISO 字串轉換為時間戳（秒）"""
    dt = datetime.datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    dt_utc = dt.astimezone(datetime.timezone.utc)
    return int(dt_utc.timestamp())

def wait_seconds(seconds: float):
    """延遲指定秒數（for retry 等用途）"""
    time.sleep(seconds)
