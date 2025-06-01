🧪 fake-api-project
這是個示範用的 API 自動化測試框架，
包含功能測試、整合測試，還支援 CI/CD 流程和測試通知，
適合拿來當作品集或實務練習。

📁 專案結構簡介

fake-api-project/
├── main.py             # 入口，集中管理 log、錯誤、通知
├── requirements.txt    # Python 套件依賴
├── bat/                # 常用一鍵腳本（切分支、推送、更新套件等）
├── workspace/          # 主要程式碼與測試
│   ├── config/         # 全域設定（路徑、金鑰、錯誤碼）
│   ├── controller/     # 控制器，串接模組流程與錯誤處理
│   ├── modules/        # 真正的 API 請求邏輯
│   ├── notifier/       # 通知系統（目前用 Telegram）
│   ├── testdata/       # 測試用資料（JSON）
│   ├── tests/          # pytest 測試檔
│   ├── utils/          # 工具類模組（log、assert、retry 等）
│   ├── logs/           # 日誌檔案目錄
│   └── reports/        # 測試報告
✅ 設計原則
每個模組職責分明，互不干擾

main.py 是統一入口，負責錯誤、log、通知整合

由 controller 處理流程與錯誤彙整

真正跟 API 請求相關邏輯寫在 modules

測試跟模組一一對應，方便管理

🔧 輔助工具
bat/ 裡有常用腳本，像是切換分支、推送、更新套件、顯示專案結構

測試會產出漂亮的 HTML 報告放在 workspace/reports

測試結果會自動通知 Telegram

🧠 維護策略
都用 Path(__file__).resolve() 做路徑管理，避免錯誤

模組拆得細，單一職責好維護

將來可搭配 JSON schema 驗證測試資料

🚀 如何開始

# 安裝套件
pip install -r requirements.txt

# 執行所有測試並產出 HTML 報告
pytest --html=workspace/reports/report.html --self-contained-html
