import pytest

# 模組級標記：整合測試 + 控制器類別
pytestmark = [pytest.mark.integration, pytest.mark.controller]

from workspace.controller import data_generation_controller
from workspace.config.paths import USER_TESTDATA_ROOT as USER_PATH, PRODUCT_TESTDATA_ROOT as PRODUCT_PATH
from workspace.utils.file.file_helper import file_exists

def test_run_data_generation_controller(monkeypatch, capsys):
    # ✅ mock 組合器：產生固定 uuid 與檔案
    def mock_generate_testdata():
        return 0, {
            "uuid": "mock-uuid",
            "user_file": USER_PATH / "mock-uuid.json",
            "product_file": PRODUCT_PATH / "mock-uuid.json",
            "user": {},
            "product": {}
        }

    monkeypatch.setattr(
        data_generation_controller,
        "generate_testdata",
        mock_generate_testdata,
    )

    # ✅ 執行控制器，並捕捉回傳值
    code, result = data_generation_controller.run_data_generation_controller()

    # ✅ 確認印出結果
    captured = capsys.readouterr()
    assert "✅ 測資成功" in captured.out
    assert "使用者測資：" in captured.out
    assert "商品測資：" in captured.out

    # ✅ 核心驗證：是否回傳 uuid 給總控器
    assert code == 0
    assert result["uuid"] == "mock-uuid"

