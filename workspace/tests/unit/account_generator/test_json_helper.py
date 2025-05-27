import tempfile
import json
from utils.json_helper import write_json
from pathlib import Path


def test_write_json_creates_file():
    data = {"key": "value"}
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / "test_output.json"
        write_json(data, temp_path)

        assert temp_path.exists()
        with open(temp_path, "r", encoding="utf-8") as f:
            content = json.load(f)
        assert content == data
