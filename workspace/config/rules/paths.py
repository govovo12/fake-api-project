# workspace/config/rules/paths.py

from pathlib import Path

# 指向 fake-api-project/workspace
BASE_PATH = Path(__file__).resolve().parents[2]


# 預設測資儲存位置（給帳號產生器）
ACCOUNT_OUTPUT_PATH = BASE_PATH / "workspace" / "testdata" / "login" / "valid_case.json"
