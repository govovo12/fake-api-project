# 🧪 fake-api-project

專案目標為展示一套符合業界標準的 API 自動化測試框架，涵蓋功能測試與整合測試，並結合 CI/CD、測試報告與通知機制，作為作品集與實務開發基礎。

---

## 📁 專案結構說明

```bash
fake-api-project/
├── main.py                     # 專案主入口，統一處理 log、通知、錯誤管理
├── requirements.txt            # 所有依賴套件
├── bat/                        # 一鍵腳本工具（如切分支、推送、更新套件）
├── workspace/                  # 專案主要邏輯與測試模組
│   ├── .github/workflows/      # GitHub Actions 流程檔（自動測試與部署）
│   ├── config/                 # 全域設定檔（如路徑、金鑰、錯誤碼）
│   ├── controller/             # 控制器：處理模組流程、錯誤整合
│   ├── modules/                # 單一模組：執行實際 API 請求邏輯
│   ├── notifier/               # 通知模組抽象化架構（目前為 telegram）
│   ├── telegram/               # Telegram 實際發送邏輯（可移入 notifier）
│   ├── testdata/              # 測資（每模組一資料夾，含 schema）
│   ├── tests/                 # pytest 測試檔案（每模組對應一支）
│   ├── utils/                 # log 工具、斷言工具
│   ├── logs/                  # log 寫入目錄（每日一檔）
│   ├── reports/               # pytest-html 測試報告輸出
```

---

## ✅ 設計原則

### 模組分層原則

| 層級            | 負責內容                         |
| ------------- | ---------------------------- |
| `main.py`     | 統一呼叫 controller，集中 log、錯誤、通知 |
| `controller/` | 串接模組邏輯、處理流程與錯誤彙整             |
| `modules/`    | 負責實際 API 請求與資料處理             |
| `testdata/`   | 儲存測資 JSON（支援多筆、自動讀取）         |
| `tests/`      | 撰寫 pytest 測試案例（與模組一對一）       |

### 補充模組原則

* `error_codes.py`: 集中管理錯誤碼
* `logger.py`: 使用 log\_step 裝飾器，集中 log 等級設定（由 global\_config 控制）
* `notifier/`: 採抽象介面設計，未來可替換為 Slack/Email 等

---

## 🔧 輔助工具

### bat/

* `commit_and_push.bat`: 輸入 commit message 後自動 git 推送
* `switch_branch.bat`: 一鍵切換分支
* `print_structure.bat`: 顯示目前專案結構
* `update_requirements.bat`: 自動合併套件與 requirements.txt（英文無亂碼）

### 測試與報告

* 使用 `pytest-html`：產出 HTML 報告存至 `workspace/reports/`
* 測試報告會上傳 GitHub Pages
* 測試結果摘要會通知 Telegram（由 main.py 控制）

---

## 🧠 維護策略

* 所有檔案皆使用旗標式路徑：`Path(__file__).resolve()` 作為基礎
* 模組責任明確：每層只處理單一任務
* 可搭配 `create_module.py`（未啟用）自動產生模組結構
* 測資資料建議搭配 schema 驗證，使用 `jsonschema` 套件

---

## 🚀 開始測試

```bash
# 安裝依賴
pip install -r requirements.txt

# 執行測試並產出報告
pytest --html=workspace/reports/report.html --self-contained-html
```

---
