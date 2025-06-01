import pytest
from datetime import datetime

pytestmark = [pytest.mark.unit, pytest.mark.fixture]

def tool(func):
    func.is_tool = True
    return func

@pytest.fixture
@tool
def fake_now():
    """產生固定當前時間物件，for 測試用 [TOOL]"""
    return datetime(2024, 6, 1, 12, 0, 0)
