import sys
from pathlib import Path

# 強制加入 workspace 根目錄，支援 config 路徑
sys.path.append(str(Path(__file__).resolve().parents[3]))

import tempfile
from config.paths import ENV_PATH
from utils.env import env_manager
import pytest

pytestmark = [pytest.mark.env, pytest.mark.unit]

def test_load_env_and_get_env(monkeypatch):
    # 建立暫存 .env 檔
    content = "TEST_KEY=12345\n"
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".env", delete=False) as f:
        f.write(content)
        f_path = Path(f.name)

    # 模擬 paths.ENV_PATH 指向該檔案位置
    monkeypatch.setattr("config.paths.ENV_PATH", f_path.parent)

    # 測試是否正確載入並讀取（補上 filename）
    env_manager.load_env(filename=f_path.name)
    value = env_manager.get_env("TEST_KEY")
    assert value == "12345"

def test_get_env_with_default():
    # 未載入任何 .env，但有提供預設值
    value = env_manager.get_env("NON_EXIST_KEY", default="fallback")
    assert value == "fallback"
