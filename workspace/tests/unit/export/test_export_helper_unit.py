import pytest
from pathlib import Path
import json
from workspace.utils.export import export_helper

@pytest.mark.export
def test_export_json(tmp_path):
    data = {"x": 1, "y": [2, 3]}
    out_path = tmp_path / "report" / "data.json"
    export_helper.export_json(data, out_path)
    assert out_path.exists()
    loaded = json.loads(out_path.read_text(encoding="utf-8"))
    assert loaded == data

@pytest.mark.export
def test_export_text(tmp_path):
    msg = "測試輸出內容"
    out_path = tmp_path / "log" / "output.log"
    export_helper.export_text(msg, out_path)
    assert out_path.exists()
    assert out_path.read_text(encoding="utf-8") == msg
