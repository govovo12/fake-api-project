
# ✅ 載入 .env 檔案中的環境變數
from dotenv import load_dotenv
load_dotenv()

pytest_plugins = [
    "workspace.tests.fixtures.controller_fixtures",            # ✅ 真實參數 fixture
    "workspace.tests.integration.fixtures_master_controller",  # ✅ 原本整合用 mock fixture
]