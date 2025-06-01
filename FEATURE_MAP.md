✅ 功能對照表（FEATURE MAP）
🔹 工具模組 | utils
📁 workspace/utils/

檔案 / 資料夾	功能說明	pytest 標記
asserts/assert_helper.py	常用斷言封裝（符合蝦皮測試風格）	asserts
callback/callback_helper.py	callback 工具（事件觸發、回呼管理）	callback
data/data_loader.py	JSON 測資載入工具	data
env/env_manager.py	.env 載入與路徑管理	env
error/error_handler.py	錯誤處理模組（封裝例外與格式化）	error
export/export_helper.py	資料匯出工具（格式轉換、寫檔）	export
file/file_helper.py	檔案處理工具（建立 temp file, 檢查存在）	file
file/folder_helper.py	資料夾處理工具（ensure, 清空）	file
logger/logger.py	log 記錄模組（統一格式、寫檔）	log
logger/log_writer.py	log 檔寫入輔助	log
notifier/base.py	Notifier 介面/基底類別	notifier
notifier/factory.py	Notifier 工廠管理多種通知管道	notifier
notifier/telegram_notifier.py	Telegram 通知發送（send API 實作）	notifier
print/printer.py	終端輸出格式化（含色碼）	printer
request/request_handler.py	requests 封裝，含 log、錯誤處理	request
retry/retry_handler.py	retry 控制邏輯（支援 backoff）	retry
stub/data_stub.py	測試用 stub 數據管理	stub
time/time_helper.py	時間轉換與 sleep 工具	time
fake/fake_helper.py	假資料產生工具（faker 簡易版）	fake

🔹 未來擴充建議（可依需再補寫）：

強化 random_factory.py 或改寫為更完整的 faker 模組

整合 mock_helper.py，提升測試模擬能力

引入 pytest-html / allure-pytest 自動化報告取代舊式 summary_writer

增加多通道 notifier (Slack、Line、Email)

建立環境切換與 profile 管理工具

加入測試資料的自動建立與清理模組

🔹 測試規則說明：

每個工具模組都有對應的 test_xxx_unit.py 單元測試

大部分核心功能均已涵蓋測試

Marker 註冊於 pytest.ini，務必保持同步與更新

