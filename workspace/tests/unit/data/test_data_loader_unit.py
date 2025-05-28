import pytest
import json
from utils.data import data_loader
from pathlib import Path
import tempfile

pytestmark = [pytest.mark.unit, pytest.mark.data]



def test_load_json_success():
    test_data = {"key": "value"}
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as f:
        json.dump(test_data, f)
        f_path = Path(f.name)

    result = data_loader.load_json(f_path)
    assert result == test_data


def test_load_json_file_not_found():
    result = data_loader.load_json(Path("not_exist_file.json"))
    assert result == {}  # fallback safe
