# 🛒 Fake Store API 測試框架

本專案是一個模擬電商平台的自動化測試框架，涵蓋使用者註冊、登入、建立訂單、購物車操作與登出流程，並整合完整的單元、整合、端對端測試與覆蓋率報告，支援 GitHub Actions 與 Telegram 通知。

---

## 📁 專案結構（四層架構）

```shell
workspace/
├── scripts/             # 第四層：測試執行入口（run_test_pipeline.py）
├── config/              # 第三層：paths、錯誤碼與環境設定
├── modules/             # 第二層：子控制器與任務模組（各功能如登入、註冊、購物等）
├── tools/               # 第一層：底層工具模組（如 request、token、log、printer）
└── tests/               # 各階段測試（unit, infra, integration, e2e）
```

---

## ✅ 測試階段說明

| 測試階段 | 說明                          | 標記       |
|----------|-------------------------------|------------|
| Unit     | 工具模組與任務模組的單元測試  | `unit`     |
| Infra    | 第三層設定模組與環境驗證測試  | `infra`    |
| Integration | 子控制器串接流程與資源互動測試 | `integration` |
| E2E      | 跨多層模組的端對端驗證測試     | `e2e`      |

---

## 📈 覆蓋率與報告說明

所有測試階段皆整合 `pytest-cov`，會依階段產出測試報告與覆蓋率：

```
workspace/
├── reports/
│   ├── unit/
│   │   └── unit_test_report_*.html
│   ├── integration/
│   ├── e2e/
│   ├── coverage/
│   │   ├── .coverage.unit
│   │   ├── .coverage.integration
│   │   └── ...
│   └── TOTAL/
│       └── index.html  ← ✅ 總覆蓋率報告
```

---

## 🚀 執行方式

### ✅ 本地執行整體測試流程

```bash
python workspace/scripts/run_test_pipeline.py
```

### ✅ 執行指定階段測試（帶標記）

```bash
pytest -m "unit or integration" --cov=workspace
```

### ✅ 一鍵清理與格式化

```bash
clean_and_format.bat
```

---

## 🧪 CI/CD 機制（GitHub Actions）

- CI 自動執行四階段測試
- TG 機器人推送簡要測試結果（含成功/失敗與時間戳）
- 報告自動部署至 GitHub Pages，附帶連結點開瀏覽

---

## 🔐 機密管理（Telegram）

- 本地：使用 `.env` 管理 TG Token 與 Chat ID
- GitHub：採用 Secret 機制設定同名環境變數

---

## 📄 備註

- 若專案中有部分檔案不需測試（如 paths.py 等輔助模組），可透過 `.coveragerc` 或合理排除，不影響整體評估。
- 若需更改測試報告輸出格式或路徑，請編輯 `run_test_pipeline.py` 與 `report_setup.py`

---

### 📝 E2E 測試容錯說明

因部分第三方 API（如 fakestoreapi.com）在 GitHub Actions 上可能因 IP 封鎖導致測試失敗，為避免 CI 流程中斷，本框架設計如下容錯策略：

- `run_test_pipeline.py` 中的 `e2e` 測試階段會照常執行並產出報告
- 若 `e2e` 測試失敗，流程 **不會中止**，仍會產出總體報告與觸發後續流程
- 本地執行 `e2e` 測試仍會完整驗證所有功能，建議開發時完整執行

如需強制 CI 上中斷流程，請調整 `run_test_pipeline.py` 中對 `e2e` 階段的錯誤處理策略。

## 👨‍💻 作者資訊

- Author: 自學測試開發者
- Last Update: 2025-07-28
