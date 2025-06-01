# workspace/tests/unit/env/test_env_manager_unit.py

import pytest
import os
from pathlib import Path
from utils.env.env_manager import load_env, get_env

pytestmark = [pytest.mark.unit, pytest.mark.env]

def test_load_env_and_get_env(tmp_path, monkeypatch):
    """
    [BASIC] 載入 .env 檔並正確取得 key/value
    """
    content = "TEST_KEY=12345\nANOTHER=foo\n"
    env_file = tmp_path / ".env"
    env_file.write_text(content, encoding="utf-8")
    assert load_env(env_file) is True
    assert get_env("TEST_KEY") == "12345"
    assert get_env("ANOTHER") == "foo"

def test_get_env_with_default(monkeypatch):
    """
    [DEFAULT] 取得不存在 key 時應回傳 default
    """
    monkeypatch.delenv("NON_EXIST_KEY", raising=False)
    assert get_env("NON_EXIST_KEY", default="fallback") == "fallback"

def test_load_env_ignores_comments_and_blank(tmp_path):
    """
    [COMMENT] .env 可正確忽略註解與空行
    """
    content = """
# Comment line
KEY1=val1

# Another comment
KEY2=  val2  
"""
    env_file = tmp_path / ".env"
    env_file.write_text(content, encoding="utf-8")
    assert load_env(env_file) is True
    assert get_env("KEY1") == "val1"
    assert get_env("KEY2") == "val2"

def test_load_env_trims_whitespace(tmp_path):
    """
    [SPACE] .env 應修剪鍵與值的空白
    """
    content = "  SPACED_KEY = spaced value \n"
    env_file = tmp_path / ".env"
    env_file.write_text(content, encoding="utf-8")
    assert load_env(env_file) is True
    assert get_env("SPACED_KEY") == "spaced value"

def test_load_env_with_equals_in_value(tmp_path):
    """
    [EQUALS] 值中包含等號，應正確解析
    """
    content = "COMPLEX=some=value=with=equals\n"
    env_file = tmp_path / ".env"
    env_file.write_text(content, encoding="utf-8")
    assert load_env(env_file) is True
    assert get_env("COMPLEX") == "some=value=with=equals"

def test_load_env_overrides_existing_env(tmp_path, monkeypatch):
    """
    [OVERRIDE] .env 載入後會覆蓋已存在的環境變數
    """
    monkeypatch.setenv("OVERRIDE", "oldvalue")
    content = "OVERRIDE=newvalue\n"
    env_file = tmp_path / ".env"
    env_file.write_text(content, encoding="utf-8")
    assert load_env(env_file) is True
    assert get_env("OVERRIDE") == "newvalue"

def test_load_env_file_not_exist(tmp_path):
    """
    [NOT FOUND] 檔案不存在應回傳 False，不會報錯
    """
    env_file = tmp_path / "notfound.env"
    assert load_env(env_file) is False
