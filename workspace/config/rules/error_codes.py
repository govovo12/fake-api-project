class ResultCode:
    """統一定義任務模組與控制器可用的錯誤碼"""

    # ✅ 通用
    SUCCESS = 0  # 任務成功

    # ✅ UUID 任務
    UUID_GEN_FAIL = 10101  # UUID 產生失敗

    # ✅ User 任務
    ACCOUNT_GEN_FAIL = 20101  # 假帳號產生失敗
    USER_WRITE_FAIL = 20201   # 寫入用戶資料失敗

    # ✅ Product 任務
    PRODUCT_GEN_FAIL = 30101  # 假商品產生失敗
    PRODUCT_WRITE_FAIL = 30201  # 寫入商品資料失敗
