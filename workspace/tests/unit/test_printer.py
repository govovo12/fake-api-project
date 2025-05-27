import re
from utils.printer import print_info, print_error
import pytest

pytestmark = [pytest.mark.account_generator, pytest.mark.unit]



def test_print_info_format(capfd):
    print_info("info message")
    out, _ = capfd.readouterr()
    assert re.search(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] INFO\s*- info message", out)

def test_print_error_format(capfd):
    print_error("error message")
    out, _ = capfd.readouterr()
    assert re.search(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] ERROR\s*- error message", out)
