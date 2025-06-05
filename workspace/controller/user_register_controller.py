"""
使用者註冊控制器：讀取帳號測資 → 組裝 payload → 發送註冊 API
"""

from __future__ import annotations
from pathlib import Path
import json

from workspace.config import paths
from workspace.config.rules import error_codes
from workspace.utils.env.env_manager import load_env, get_env
from workspace.utils.logger.log_helper import log_step
from workspace.utils.print.printer import print_info, print_error
from workspace.utils.data.data_loader import load_user_testdata
from workspace.modules.register.build_register_payload import build_register_payload
from workspace.utils.data.data_enricher import enrich_with_uuid
from workspace.utils.request.request_handler import post
from workspace.utils.response.response_helper import get_data_field_from_dict

__task_info__ = {
    "task": "user_register",
    "desc": "讀取帳號測資並註冊帳號",
    "version": "1.0.1",
    "input": "uuid（需先產生資料）",
    "output": "註冊結果與 log",
}


def run(user_uuid: str = None):
    ResultCode = error_codes.ResultCode

    # Step 0: 載入 API 設定檔
    if not load_env(paths.API_ENV_PATH):
        log_step("讀取 API 設定", ResultCode.USER_TESTDATA_NOT_FOUND)
        return

    # Step 1: 抓取設定變數
    REGISTER_URL = get_env("REGISTER_URL")
    REGISTER_HEADER_STR = get_env("REGISTER_HEADER", "{}")
    try:
        REGISTER_HEADER = json.loads(REGISTER_HEADER_STR)
    except Exception:
        print_error("❌ REGISTER_HEADER 格式錯誤")
        return

    # Step 2: 檢查 UUID 存在
    if not user_uuid:
        print_error("❌ 未提供 UUID，請確認是否有先執行資料產生任務")
        return
    print_info(f"📄 UUID = {user_uuid}")

    # Step 3: 讀取帳號測資
    code_data, user_data = load_user_testdata(user_uuid)
    log_step("讀取測資", code_data)
    if code_data != ResultCode.SUCCESS or not user_data:
        return

    # Step 4: 組裝 payload
    code_payload, payload = build_register_payload(user_data)
    log_step("組裝註冊 payload", code_payload)
    if code_payload != ResultCode.SUCCESS or not payload:
        return

    # Step 5: 加上 UUID
    enriched_payload = enrich_with_uuid(payload, user_uuid)
    print_info("✅ 已補完 payload 欄位")

    # Step 6: 發送 API
    try:
        response = post(REGISTER_URL, enriched_payload, headers=REGISTER_HEADER)
        register_id = get_data_field_from_dict(response.json(), "id")

        if register_id:
            log_step("註冊 API", ResultCode.SUCCESS)
        else:
            log_step("註冊 API", ResultCode.REGISTER_API_FAIL)
    except Exception:
        log_step("註冊 API", ResultCode.REGISTER_API_FAIL)
