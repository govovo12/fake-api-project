# Account Generator 模組實作進度圖（已完成 ✅）

Account Generator
├── controller/
│   └── account_generator_controller.py     # ✅ 控制流程、錯誤處理、呼叫模組與寫入測資（含 __task_info__）
├── modules/
│   └── account_generator.py                # ✅ 負責帳號資料生成與存檔（不處理 log、流程、IO）
├── factory/
│   └── module_factory.py                   # ✅ 提供 account_module + 注入依賴（random_fn, writer_fn）
├── config/
│   ├── rules/
│   │   └── account_config.py               # ✅ 設定結構與欄位組合邏輯（prefix, 密碼長度等）
│   └── envs/
│       └── account_gen.env                 # ✅ 實際產測用參數（長度、筆數等）
├── testdata/
│   └── login/
│       └── valid_case.json                 # ✅ 帳號產生後儲存位置（controller 寫入，格式已調整為 List）
└── utils/
    ├── random_factory.py                   # ✅ 隨機工具（如 simple_random_string）
    ├── json_helper.py                      # ✅ JSON 寫入工具（含目錄建立）
    ├── printer.py                          # ✅ 格式化輸出（INFO/ERROR 時間戳）
    └── logger.py                           # ✅ log 包裝與錯誤碼輸出（支援代碼）
