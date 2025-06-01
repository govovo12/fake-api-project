import datetime
import time

try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except ImportError:
    ZoneInfo = None

def tool(func):
    """自製工具標記裝飾器（供工具表自動辨識）"""
    func.is_tool = True
    return func

@tool
def get_time(
    tz: str = "UTC",
    fmt: str = "%Y-%m-%d %H:%M:%S",
    output: str = "str"
):
    """
    彈性取得目前時間（可選時區、格式、輸出型態）[TOOL]
    - tz: 時區（預設 'UTC'，支援 'Asia/Taipei', 'local'）
    - fmt: strftime 格式字串（預設 "%Y-%m-%d %H:%M:%S"），output="str" 時用
    - output: 回傳型態，"str"（格式化字串）、"datetime"、"timestamp"（float秒）
    
    範例：
        get_time()  # 預設 UTC "%Y-%m-%d %H:%M:%S"
        get_time("Asia/Taipei")
        get_time(fmt="%Y/%m/%d %H:%M")
        get_time(output="datetime")
        get_time("Asia/Taipei", output="timestamp")
        get_time("local", output="str", fmt="%H:%M")
    """
    # 選擇時區
    if tz == "local":
        now = datetime.datetime.now()
    else:
        if ZoneInfo:
            zone = ZoneInfo(tz)
            now = datetime.datetime.now(zone)
        else:
            try:
                import pytz
                zone = pytz.timezone(tz)
                now = datetime.datetime.now(zone)
            except ImportError:
                raise RuntimeError("需安裝 zoneinfo (Py3.9+) 或 pytz")
    # 回傳型態
    if output == "datetime":
        return now
    elif output == "timestamp":
        return now.timestamp()
    elif output == "str":
        return now.strftime(fmt)
    else:
        raise ValueError(f"Unsupported output type: {output}")


@tool
def wait_seconds(seconds: int) -> None:
    """讓程式等待指定秒數 [TOOL]"""
    time.sleep(seconds)

@tool
def timestamp_to_iso(ts: float, tz: str = "UTC") -> str:
    """將 timestamp 轉換為指定時區的 ISO 格式字串 [TOOL]"""
    if ZoneInfo:
        zone = ZoneInfo(tz)
        dt = datetime.datetime.fromtimestamp(ts, zone)
    else:
        try:
            import pytz
            zone = pytz.timezone(tz)
            dt = datetime.datetime.fromtimestamp(ts, zone)
        except ImportError:
            raise RuntimeError("需安裝 zoneinfo (Py3.9+) 或 pytz")
    return dt.isoformat()

@tool
def iso_to_timestamp(iso_str: str) -> float:
    """將 ISO 格式字串轉換為 timestamp（float秒） [TOOL]"""
    return datetime.datetime.fromisoformat(iso_str).timestamp()
