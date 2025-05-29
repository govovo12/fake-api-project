import re
from configparser import ConfigParser
from pathlib import Path

pytest_ini_path = Path(__file__).resolve().parents[1] / "pytest.ini"

config = ConfigParser(allow_no_value=True)
config.read(pytest_ini_path, encoding="utf-8")

marker_lines = []
inside_markers = False

with pytest_ini_path.open(encoding="utf-8") as f:
    for line in f:
        if line.strip().startswith("markers"):
            inside_markers = True
            continue
        if inside_markers:
            if line.strip() == "" or re.match(r"\w+\s*=", line):
                break
            marker_name = line.strip().split(":")[0].strip()
            marker_lines.append(marker_name)

if marker_lines:
    marker_expr = " or ".join(marker_lines)
    print(f'pytest -m "{marker_expr}" -v')
else:
    print("No markers found.")
