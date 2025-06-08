import pytest
import uuid

# 模組級標記：整合測試 + 控制器類別
pytestmark = [pytest.mark.integration, pytest.mark.controller]

from workspace.controller import data_generation_controller
from workspace.config.paths import USER_TESTDATA_ROOT as USER_PATH, PRODUCT_TESTDATA_ROOT as PRODUCT_PATH
from workspace.utils.file.file_helper import file_exists

def test_run_data_generation_controller(monkeypatch, capsys):
    test_uuid = uuid.uuid4().hex

    def mock_generate_testdata(uuid):
        return 0, {
            "uuid": uuid,
            "user_file": USER_PATH / f"{uuid}.json",
            "product_file": PRODUCT_PATH / f"{uuid}.json",
            "user": {},
            "product": {}
        }

    monkeypatch.setattr(
        data_generation_controller,
        "generate_testdata",
        mock_generate_testdata,
    )

    code, result = data_generation_controller.run_data_generation_controller(test_uuid)

    # ✅ 捕捉印出內容，並確認關鍵訊息存在
    captured = capsys.readouterr()
    print("\n=== CAPTURED OUTPUT ===")
    print(captured.out)

    # ✅ 改成更保險的字串檢查，不再使用 emoji 符號
    assert "測資成功" in captured.out
    assert "使用者測資：" in captured.out
    assert "商品測資：" in captured.out

    assert code == 0
    assert result["uuid"] == test_uuid

