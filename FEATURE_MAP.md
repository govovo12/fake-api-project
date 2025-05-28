✅ 功能對照表（FEATURE MAP）
🔹 工具模組 | utils
📁 workspace/utils/

檔案	功能說明	pytest 標記
logger/logger.py	log 記錄模組（統一格式、寫檔）	log
print/printer.py	終端輸出格式化（含色碼）	printer
print/color_helper.py	ANSI 色碼輔助工具	-
retry/retry_handler.py	retry 控制邏輯（支援 backoff）	retry
request/request_handler.py	requests 封裝，含 log、錯誤處理	request
data/data_loader.py	JSON 測資載入工具	data
env/env_manager.py	.env 載入與路徑管理	env
time/time_helper.py	時間轉換與 sleep 工具	time
asserts/assert_helper.py	常用斷言封裝（符合蝦皮測試風格）	asserts
file/file_helper.py	檔案處理工具（建立 temp file, 檢查存在）	file
file/folder_helper.py	資料夾處理工具（ensure, 清空）	file
callback/callback_helper.py	callback 工具（事件觸發、回呼管理）	callback
export/export_helper.py	資料匯出工具（格式轉換、寫檔）	export
error/error_handler.py	錯誤處理模組（封裝例外與格式化）	error
error/error_controller.py	錯誤控制邏輯（集中管理 error flow）	error
notifier/telegram_notifier.py	Telegram 通知發送（send API 實作）	notifier
notifier/factory.py	Notifier 工廠管理多種通知管道	notifier
notifier/controller.py	Notifier 控制器邏輯（發送包裝）	notifier

📁 workspace/tests/unit/

單元測試檔都已齊全：每個工具模組都有對應 test_xxx_unit.py

Marker 配合功能：log, printer, retry, request, data, env, time, asserts, file, callback, export, error, notifier

📁 workspace/tests/integration/

整合測試檔與各大功能模組對應：request, notifier, file, error...（依據需求新增）

📁 pytest.ini

✅ 測試標記已註冊：log, printer, retry, request, data, env, time, asserts, file, callback, export, error, notifier, integration, unit

📁 bat/run_all_tests.bat

✅ 一鍵執行所有 unit+integration 測試，產出報告

📁 workspace/utils/summary_writer.py

✅ 測試統計摘要輸出工具（log 統計、測試報告用）

🔹 其餘模組
帳號產生、登入、註冊等功能
目前暫時未列入，等重構與測試補完再統整進 feature map

⚠️ 提醒
每個模組的單元/整合測試都要補 marker（不然 pytest -m 搜尋會漏）

新增工具務必同步註冊 marker，更新 map 與 pytest.ini，保持一致性！