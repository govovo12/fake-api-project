# ==============================
# 自製工具標記裝飾器
# ------------------------------
def tool(func):
    """自製工具標記裝飾器（供工具表自動辨識）"""
    func.is_tool = True
    return func


# ==============================
# 內建與第三方模組
# ------------------------------
import datetime
import time
from typing import Union

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

# ==============================
# 自訂錯誤碼
# ------------------------------
from workspace.config.rules.error_codes import ResultCode


@tool
def get_time(
    tz: str = "UTC",
    fmt: str = "%Y-%m-%d %H:%M:%S",
    output: str = "str",
) -> Union[int, float, str]:
    """
    取得指定時區的當前時間，支援多種輸出格式。
    成功時回傳格式化字串、datetime 或 timestamp。
    發生錯誤時回傳對應錯誤碼。
    """
    try:
        if tz == "local":
            now = datetime.datetime.now()
        else:
            if ZoneInfo:
                zone = ZoneInfo(tz)
                now = datetime.datetime.now(zone)
            else:
                import pytz
                zone = pytz.timezone(tz)
                now = datetime.datetime.now(zone)

        if output == "datetime":
            return now
        elif output == "timestamp":
            return now.timestamp()
        elif output == "str":
            return now.strftime(fmt)
        else:
            return ResultCode.TOOL_TIME_UNSUPPORTED_OUTPUT

    except ValueError:
        return ResultCode.TOOL_TIME_INVALID_FORMAT
    except Exception as e:
        if "timezone" in str(e).lower():
            return ResultCode.TOOL_TIME_INVALID_TIMEZONE
        return ResultCode.TOOL_TIME_UNSUPPORTED_OUTPUT


@tool
def timestamp_to_iso(timestamp: float, tz: str = "UTC") -> Union[str, int]:
    try:
        dt = datetime.datetime.fromtimestamp(timestamp)
        if tz != "UTC":
            if ZoneInfo:
                dt = dt.astimezone(ZoneInfo(tz))
            else:
                import pytz
                dt = dt.astimezone(pytz.timezone(tz))
        return dt.isoformat()
    except Exception:
        return ResultCode.TOOL_TIME_INVALID_TIMEZONE


@tool
def iso_to_timestamp(iso_str: str) -> Union[float, int]:
    """
    將 ISO 格式時間字串轉為 UNIX timestamp。
    發生錯誤時回傳錯誤碼。
    """
    try:
        dt = datetime.datetime.fromisoformat(iso_str)
        return dt.timestamp()
    except Exception:
        return ResultCode.TOOL_TIME_INVALID_FORMAT


@tool
def wait_seconds(sec: int):
    if sec < 0:
        return ResultCode.TOOL_TIME_INVALID_FORMAT  # 或其他錯誤碼
    time.sleep(sec)
    return ResultCode.SUCCESS