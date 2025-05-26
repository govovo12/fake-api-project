## ✅ 功能對照表（FEATURE MAP）

---

### 🔹 測資模組 | account_generator

📁 workspace/modules/account_generator.py
├── ✅ 帳號產生核心模組（支援單組/多組產生）
├── ✅ 採用參數化控制帳號格式（由 .env.account_gen 管理）
├── ✅ 自動寫入測資 json，供 login 登入測試使用

📁 workspace/controller/account_generator_controller.py
└── ✅ 控制層模組，接收 task_info 呼叫，觸發模組執行 + log 記錄

📁 workspace/task/task_account_generator.py
└── ✅ 註冊 __task_info__ 任務，可由 main.py 透過 --task account_generator 執行

📁 workspace/tests/integration/test_account_generator.py
└── ✅ 整合測試：驗證多組帳號產生流程，並檢查輸出 json 完整性

📁 workspace/tests/unit/
├── test_json_helper.py
├── test_logger.py
├── test_printer.py
└── test_random_factory.py
    ✅ 工具層模組測試已完整覆蓋

📁 bat/run_all_tests.bat
└── ✅ 測試啟動入口：一鍵執行 unit + integration + 產出報告

📁 workspace/utils/run_launcher.py
├── ✅ 控制整體測試流程：分段執行 unit / integration 測試
├── ✅ 支援 venv 啟動與自動修正路徑（避免報告錯位）
└── ✅ 匯整 pytest 執行 log 至 run_log.txt，並呼叫 summary_writer

📁 workspace/utils/summary_writer.py
└── ✅ 統計測試通過/失敗數量，支援換行/異常格式，輸出摘要區塊

📁 workspace/reports/
├── run_log.txt       ⬅ 所有測試 log 匯整於此
├── unit_report.html  ⬅ 單元測試報告
└── integration_report.html ⬅ 整合測試報告
