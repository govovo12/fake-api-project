import pytest

pytestmark = [pytest.mark.unit, pytest.mark.fixture]

def tool(func):
    func.is_tool = True
    return func

@pytest.fixture
@tool
def fake_logger():
    """回傳可監控呼叫紀錄的假 logger [TOOL]"""
    class Logger:
        def __init__(self):
            self.messages = []
        def info(self, msg): self.messages.append(('info', msg))
        def warn(self, msg): self.messages.append(('warn', msg))
        def error(self, msg): self.messages.append(('error', msg))
    return Logger()
