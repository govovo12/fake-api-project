class ResultCode:
    SUCCESS = 0  # ✅ 成功

    # ✅ UUID
    UUID_GEN_FAIL = 10100
    UUID_ATTACH_FAILED = 10101  # enrich_with_uuid 發生例外

    # ✅ 使用者測資
    USER_GENERATION_FAILED = 20101
    USER_TESTDATA_SAVE_FAILED = 20103
    USER_UUID_ATTACH_FAILED = 20104

    # ✅ 商品測資
    PRODUCT_GENERATION_FAILED = 30101
    PRODUCT_TESTDATA_SAVE_FAILED = 30103
    PRODUCT_UUID_ATTACH_FAILED = 30104

    # ✅ 組合器通用
    TESTDATA_ALREADY_EXISTS = 90101

      # ✅ 註冊任務
    REGISTER_PAYLOAD_BUILD_FAILED = 40101
    REGISTER_REQUEST_FAILED = 40102
    
    # ✅ 註冊控制器步驟（Controller 可讀性用）
    REGISTER_STEP_BUILD_PAYLOAD = 40901
    REGISTER_STEP_SEND_REQUEST = 40902
    REGISTER_STEP_SAVE_RESULT = 40903
    ERROR_CODE_MSG_MAP = {
    0: "success",

    10100: "UUID 產生失敗",
    10101: "加入 UUID 至測資失敗",

    20101: "使用者測資產生失敗",
    20103: "user 檔案寫入失敗",
    20104: "user 附加 UUID 失敗",

    30101: "商品測資產生失敗",
    30103: "product 檔案寫入失敗",
    30104: "product 附加 UUID 失敗",

    40101: "註冊 payload 組裝失敗",
    40102: "發送註冊 API 失敗",
    40901: "組裝註冊 payload",
    40902: "發送註冊請求",
    40903: "儲存註冊結果",

    90101: "測資已存在，不需重新建立",
}
