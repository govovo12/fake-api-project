✅ 功能對照表（FEATURE MAP）

🔹 工具模組 | utils
📁 workspace/utils/

| 檔案 / 資料夾                  | 功能說明                                      | pytest 標記   |
|--------------------------------|-----------------------------------------------|---------------|
| asserts/assert_helper.py       | 常用斷言封裝（符合蝦皮測試風格）                | asserts       |
| callback/callback_helper.py    | callback 工具（事件觸發、回呼管理）             | callback      |
| data/data_loader.py            | JSON 測資載入工具                              | data          |
| env/env_manager.py             | .env 載入與路徑管理                            | env           |
| error/error_handler.py         | 錯誤處理模組（封裝例外與格式化）                | error         |
| export/export_helper.py        | 資料匯出工具（格式轉換、寫檔）                  | export        |
| file/file_helper.py            | 檔案處理工具（建立 temp file, 檢查存在）         | file          |
| file/folder_helper.py          | 資料夾處理工具（ensure, 清空）                  | file          |
| logger/logger.py               | log 記錄模組（統一格式、寫檔）                  | log           |
| logger/log_writer.py           | log 檔寫入輔助                                 | log           |
| notifier/telegram_notifier.py  | Telegram 通知發送（send API 實作）              | notifier      |
| notifier/factory.py            | Notifier 工廠管理多種通知管道                   | notifier      |
| notifier/base.py               | Notifier 介面/基底類別                         | notifier      |
| print/printer.py               | 終端輸出格式化（含色碼）                        | printer       |
| print/color_helper.py          | ANSI 色碼輔助工具                              | -             |
| report/summary_writer.py       | 測試統計摘要輸出工具（log 統計、測試報告用，已淘汰） | -         |
| request/request_handler.py     | requests 封裝，含 log、錯誤處理                  | request       |
| retry/retry_handler.py         | retry 控制邏輯（支援 backoff）                  | retry         |
| time/time_helper.py            | 時間轉換與 sleep 工具                           | time          |
| json_helper.py                 | JSON 處理通用工具                              | -             |
| random_factory.py              | 隨機資料生成工廠（簡易版 faker，可再擴充）       | -             |
| run_launcher.py                | 執行入口                                       | -             |
| requirements.txt               | 套件需求清單                                   | -             |

---

🔹 **未來擴充建議（進階）：**
- **faker.py**：強化 random_factory，加入更完整的假資料產生（帳號、手機、金流等）
- **mock_helper.py**：支援 requests-mock/pytest-mock 等單元測試用 mock
- **fixtures/**：pytest fixture 共用、測資初始化/清理腳本
- **pytest-html / allure-pytest**：自動測試報告，建議取代 summary_writer
- **多通道 notifier**（slack/line/email，非必須）
- **teardown/init.py**：測試資料自動建立、清理
- **多環境 profile 管理**：prod/dev/stage 切換

---

🔹 **單元/整合測試**
- 每個工具模組都有對應的 test_xxx_unit.py（unit）
- 各大功能整合測試已對應 test_xxx_integration.py（integration）
- 所有 marker 註冊於 pytest.ini，需保持同步

---

⚠️ **提醒**
- 每個模組的單元/整合測試都要補 marker（不然 pytest -m 搜尋會漏）
- 新增工具務必同步註冊 marker，更新本對照表與 pytest.ini，保持一致性！

---

**目前主線已補齊 error/notifier 相關模組，random_factory.py 建議升級為 faker 工具，summary_writer 已可用 pytest-html/allure 取代。**
