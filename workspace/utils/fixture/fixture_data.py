import pytest

pytestmark = [pytest.mark.unit, pytest.mark.fixture]

def tool(func):
    func.is_tool = True
    return func

@pytest.fixture
@tool
def fake_user_data():
    """產生一組假的使用者資料 dict [TOOL]"""
    return {"id": 1, "name": "Alice", "email": "alice@example.com"}
