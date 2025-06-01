import pytest
from requests import Session

pytestmark = [pytest.mark.unit, pytest.mark.fixture]

def tool(func):
    func.is_tool = True
    return func

@pytest.fixture
@tool
def fake_session():
    """產生假 requests session（或可加 mock/patch）[TOOL]"""
    return Session()
