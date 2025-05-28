## ✅ 功能對照表（FEATURE MAP）

---

### 🔹 工具模組 | utils

📁 workspace/utils/
├── logger/logger.py              ✅ log 記錄模組（統一格式、寫檔）
├── print/printer.py              ✅ 終端輸出格式化（含色碼）
├── print/color_helper.py         ✅ ANSI 色碼輔助工具
├── retry/retry_handler.py        ✅ retry 控制邏輯（支援 backoff）
├── request/request_handler.py    ✅ requests 封裝，含 log、錯誤處理
├── data/data_loader.py           ✅ JSON 測資載入工具
├── env/env_manager.py            ✅ .env 載入與路徑管理
├── time/time_helper.py           ✅ 時間轉換與 sleep 工具
├── asserts/assert_helper.py      ✅ 常用斷言封裝（符合蝦皮測試風格）
├── file/file_helper.py           ✅ 檔案處理工具（建立 temp file, 檢查存在）
├── file/folder_helper.py         ✅ 資料夾處理工具（ensure, 清空）

📁 workspace/tests/unit/
├── logger/test_logger.py
├── print/test_printer_unit.py
├── retry/test_retry_handler_unit.py
├── request/test_request_handler_unit.py
├── data/test_data_loader_unit.py
├── env/test_env_manager_unit.py
├── time/test_time_helper_unit.py
├── asserts/test_assert_helper_unit.py
├── file/test_file_folder_helper_unit.py

📁 pytest.ini
└── ✅ 測試標記已註冊：log, printer, retry, request, data, env, time, asserts, file

📁 bat/run_all_tests.bat
└── ✅ 一鍵執行所有測試（unit + integration）+ 產出報告

📁 workspace/utils/summary_writer.py
└── ✅ 測試統計摘要輸出工具（log 整理）

---

🔹 其餘模組（帳號產生、登入、註冊）目前暫不列入，待重構後更新
