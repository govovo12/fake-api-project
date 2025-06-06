# 🛠️ Fake API 專案自製工具對照表（含分類分段）

## asserts

| 模組 | 名稱 | 說明 | @tool |
|---|---|---|---|
| asserts | assert_contains_substring | 驗證 substring 是否出現在 text 中 [TOOL] | ✅ |
| asserts | assert_in_keys | 驗證 obj 是否包含所有指定 keys [TOOL] | ✅ |
| asserts | assert_json_equal | 驗證兩個 JSON 結構是否一致 [TOOL] | ✅ |
| asserts | assert_status_code | 驗證 response.status_code 是否等於預期 [TOOL] | ✅ |

---

## callback

| 模組 | 名稱 | 說明 | @tool |
|---|---|---|---|
| callback | run_with_callback | 執行目標函式，若成功可觸發成功回呼，失敗可觸發錯誤回呼 | ✅ |

---

## data

| 模組 | 名稱 | 說明 | @tool |
|---|---|---|---|
| data | enrich_payload | 根據 .env 的欄位設定（逗號分隔）從資料中取值並組裝 payload。 | ✅ |
| data | enrich_with_uuid | [TOOL] 將 dict 加工，附上 uuid 欄位，回傳新 dict（不修改原資料） | ✅ |
| data | load_json | [TOOL] 通用 JSON 讀取器，回傳 (錯誤碼, 資料 or None) | ✅ |
| data | save_json | [TOOL] 通用 JSON 寫入器，成功回傳 0，失敗回傳錯誤碼 | ✅ |

---

## env

| 模組 | 名稱 | 說明 | @tool |
|---|---|---|---|
| env | EnvManager | [TOOL] 通用 .env 管理工具 | ✅ |

---

## error

| 模組 | 名稱 | 說明 | @tool |
|---|---|---|---|
| error | APIError | [TOOL] API 相關自定義錯誤，可攜帶 status_code 與 code。 | ✅ |
| error | ValidationError | [TOOL] 資料驗證相關錯誤，可攜帶 code 字串。 | ✅ |
| error | handle_exception | [TOOL] 統一將 Exception 轉為標準 dict，可選擇傳入 log callback。 | ✅ |

---

## export

| 模組 | 名稱 | 說明 | @tool |
|---|---|---|---|
| export | export_json | 將任意資料寫入 JSON 檔案，自動建立上層資料夾 [TOOL] | ✅ |
| export | export_text | 將文字寫入純文字檔案，支援自動建立資料夾 [TOOL] | ✅ |

---

## fake

| 模組 | 名稱 | 說明 | @tool |
|---|---|---|---|
| fake | fake_address | [TOOL] 隨機地址 | ✅ |
| fake | fake_cart | [TOOL] 一組購物車資料 dict | ✅ |
| fake | fake_cart_date | [TOOL] 隨機日期字串（可自訂格式） | ✅ |
| fake | fake_cart_quantity | [TOOL] 隨機購物車數量 1~10 | ✅ |
| fake | fake_company_name | [TOOL] 隨機公司名稱 | ✅ |
| fake | fake_email | [TOOL] 隨機 email | ✅ |
| fake | fake_order_id | [TOOL] 隨機訂單 ID | ✅ |
| fake | fake_password | [TOOL] 隨機密碼 | ✅ |
| fake | fake_phone | [TOOL] 隨機電話號碼（台灣格式） | ✅ |
| fake | fake_product | [TOOL] 一組完整產品資料 dict | ✅ |
| fake | fake_product_description | [TOOL] 隨機產品描述 | ✅ |
| fake | fake_product_id | [TOOL] 隨機產品 ID | ✅ |
| fake | fake_product_price | [TOOL] 隨機產品價格（可自訂範圍） | ✅ |
| fake | fake_product_title | [TOOL] 隨機產品名稱 | ✅ |
| fake | fake_url | [TOOL] 隨機網址 | ✅ |
| fake | fake_user | [TOOL] 一組完整用戶資料 dict | ✅ |
| fake | fake_username | [TOOL] 隨機帳號名稱 | ✅ |

---

## file

| 模組 | 名稱 | 說明 | @tool |
|---|---|---|---|
| file | clear_file | [TOOL] 清空指定檔案內容，若不存在則略過。 | ✅ |
| file | ensure_dir | [TOOL] 確保資料夾存在，若不存在則建立。 | ✅ |
| file | ensure_file | [TOOL] 確保檔案存在，若上層資料夾不存在則一併建立。 | ✅ |
| file | file_exists | [TOOL] 檢查檔案是否存在。 | ✅ |
| file | get_file_name_from_path | [TOOL] 取得檔案名稱（含副檔名）。 | ✅ |
| file | is_file_empty | [TOOL] 判斷指定檔案是否為空。 | ✅ |
| file | load_json | [TOOL] 載入 JSON 檔案內容，失敗回傳 None。 | ✅ |
| file | save_json | [TOOL] 安全儲存 JSON。成功回傳 True，失敗 False。使用臨時檔確保原檔不被破壞。 | ✅ |
| file | write_temp_file | [TOOL] 寫入暫存檔案，回傳檔案路徑。 | ✅ |

---

## fixture

| 模組 | 名稱 | 說明 | @tool |
|---|---|---|---|
| fixture | fake_logger | 回傳可監控呼叫紀錄的假 logger [TOOL] | ✅ |
| fixture | fake_now | 產生固定當前時間物件，for 測試用 [TOOL] | ✅ |
| fixture | fake_session | 產生假 requests session（或可加 mock/patch）[TOOL] | ✅ |
| fixture | fake_status_code | 產生固定 status_code，for 斷言測試 [TOOL] | ✅ |
| fixture | fake_user_data | 產生一組假的使用者資料 dict [TOOL] | ✅ |
| fixture | stub_cart_payload | 產生購物車 payload dict（for stub/mock）[TOOL] | ✅ |
| fixture | temp_env_fixture | 臨時切換 os.environ 的 fixture [TOOL] | ✅ |
| fixture | temp_file | 產生一個臨時檔案，for 檔案測試 [TOOL] | ✅ |

---

## logger

| 模組 | 名稱 | 說明 | @tool |
|---|---|---|---|
| logger | format_log_message | [TOOL] 格式化 log 字串，標準格式：[timestamp] [level] message | ✅ |
| logger | log_step | 根據狀態碼自動印出【步驟】成功/失敗訊息與錯誤說明 | ✅ |
| logger | write_log | [TOOL] 寫入 log 訊息到指定檔案。 | ✅ |

---

## mock

| 模組 | 名稱 | 說明 | @tool |
|---|---|---|---|
| mock | mock_api_response | 產生模擬 API response 物件 | ✅ |
| mock | mock_function | 產生模擬任意函數 | ✅ |
| mock | mock_logger | 產生模擬 logger 物件 | ✅ |

---

## notifier

| 模組 | 名稱 | 說明 | @tool |
|---|---|---|---|
| notifier | Notifier | [TOOL] 抽象通知介面：所有通知模組（如 Telegram/Slack/Email）皆應繼承。 | ✅ |
| notifier | NotifierFactory | [TOOL] Notifier 工廠：依參數產生對應通知工具。 | ✅ |
| notifier | TelegramNotifier | [TOOL] Telegram 發送通知 | ✅ |

---

## print

| 模組 | 名稱 | 說明 | @tool |
|---|---|---|---|
| print | apply_color | 將字串以指定 ANSI 色碼包裝後回傳 [TOOL] | ✅ |
| print | print_error | 彩色 error log 輸出，含時間 [TOOL] | ✅ |
| print | print_info | 彩色 info log 輸出，含時間 [TOOL] | ✅ |
| print | print_success | 彩色 success log 輸出，含時間 [TOOL] | ✅ |
| print | print_warn | 彩色 warn log 輸出，含時間 [TOOL] | ✅ |

---

## request

| 模組 | 名稱 | 說明 | @tool |
|---|---|---|---|
| request | get | 發送 GET 請求（純粹工具，不做錯誤處理與 log） | ✅ |
| request | parse_json_safe | 安全解析 JSON：成功回傳 (True, dict)，失敗回傳 (False, None) | ✅ |
| request | post | 發送 POST 請求（純粹工具，不做錯誤處理與 log） | ✅ |
| request | post_and_parse_json | 發送 POST 並解析 JSON（不判斷成功與否、不印 log、不處理錯誤碼） | ✅ |

---

## response

| 模組 | 名稱 | 說明 | @tool |
|---|---|---|---|
| response | get_code_from_dict | 取得 code 欄位（若不存在則回傳 None） | ✅ |
| response | get_data_field_from_dict | 從 data 區塊中提取指定欄位值 | ✅ |
| response | get_data_field_from_response | 從 JSON 的 data 區塊中擷取指定欄位 | ✅ |
| response | get_error_message_from_dict | 優先從 msg，其次 error 擷取錯誤訊息 | ✅ |
| response | get_error_message_from_response | 擷取 msg 或 error 為錯誤訊息 | ✅ |
| response | get_json_field_from_response | 從 JSON 中擷取指定欄位值 | ✅ |
| response | get_status_code_from_response | 取得 HTTP status code | ✅ |
| response | get_token_from_dict | 從 data 區塊中提取 token | ✅ |
| response | get_token_from_response | 擷取 JSON 的 data.token 欄位 | ✅ |

---

## retry

| 模組 | 名稱 | 說明 | @tool |
|---|---|---|---|
| retry | retry_call | [TOOL] 通用 retry 函式。可重試任意函數，支援延遲、倍增、指定例外、重試 callback。 | ✅ |
| retry | retry_decorator | [TOOL] Retry 裝飾器。加在 function 上，讓其自動支援失敗重試。 | ✅ |

---

## stub

| 模組 | 名稱 | 說明 | @tool |
|---|---|---|---|
| stub | stub_cart_payload | 產生購物車 payload dict [TOOL] | ✅ |
| stub | stub_invalid_json_file | 建立一個格式錯誤的 JSON 檔案並回傳其路徑 [TOOL] | ✅ |
| stub | stub_nonexistent_path | 回傳一個一定不存在的檔案路徑 [TOOL] | ✅ |
| stub | stub_product_payload | 產生範例商品 payload dict [TOOL] | ✅ |
| stub | stub_shiftjis_encoded_json | 回傳 Shift-JIS 編碼的假 JSON 資料 (格式測試用) [TOOL] | ✅ |
| stub | stub_user_payload | 產生登入用戶 payload dict [TOOL] | ✅ |
| stub | stub_valid_user_json | 產生範例使用者 dict [TOOL] | ✅ |

---

## time

| 模組 | 名稱 | 說明 | @tool |
|---|---|---|---|
| time | get_time | 彈性取得目前時間（可選時區、格式、輸出型態）[TOOL] | ✅ |
| time | iso_to_timestamp | 將 ISO 格式字串轉換為 timestamp（float秒） [TOOL] | ✅ |
| time | timestamp_to_iso | 將 timestamp 轉換為指定時區的 ISO 格式字串 [TOOL] | ✅ |
| time | wait_seconds | 讓程式等待指定秒數 [TOOL] | ✅ |

---

## uuid

| 模組 | 名稱 | 說明 | @tool |
|---|---|---|---|
| uuid | generate_batch_uuid_with_code | 產生一組全域唯一的 UUID，標準回傳（error_code, uuid） | ✅ |

---

