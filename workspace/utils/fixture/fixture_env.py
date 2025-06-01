import pytest
import os

pytestmark = [pytest.mark.unit, pytest.mark.fixture]

def tool(func):
    func.is_tool = True
    return func

@pytest.fixture
@tool
def temp_env_fixture(monkeypatch):
    """臨時切換 os.environ 的 fixture [TOOL]"""
    monkeypatch.setenv("TEST_ENV", "1")
    yield
    monkeypatch.delenv("TEST_ENV")
