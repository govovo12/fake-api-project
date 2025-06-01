import pytest

pytestmark = [pytest.mark.unit, pytest.mark.fixture]

def tool(func):
    func.is_tool = True
    return func

@pytest.fixture
@tool
def fake_status_code():
    """產生固定 status_code，for 斷言測試 [TOOL]"""
    return 200
