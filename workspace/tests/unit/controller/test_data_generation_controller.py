import pytest
from workspace.controller.data_generation_controller import generate_and_save_testdata
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.controller, pytest.mark.testdatacontroller]


def test_controller_all_success(monkeypatch):
    # 全部子模組都回傳成功
    monkeypatch.setattr(
        "workspace.modules.fake_data.fake_user.user_generator.generate_user_data",
        lambda: (ResultCode.SUCCESS, {"user": 1})
    )
    monkeypatch.setattr(
        "workspace.modules.fake_data.fake_product.product_generator.generate_product_data",
        lambda: (ResultCode.SUCCESS, {"product": 2})
    )
    monkeypatch.setattr(
        "workspace.utils.uuid.uuid_generator.generate_batch_uuid_with_code",
        lambda: (ResultCode.SUCCESS, "testuuid")
    )
    monkeypatch.setattr(
        "workspace.utils.data.data_enricher.enrich_with_uuid",
        lambda data, uuid: {**data, "uuid": uuid}
    )
    monkeypatch.setattr(
        "workspace.utils.data.data_loader.save_json",
        lambda data, path: None
    )
    monkeypatch.setattr(
        "workspace.utils.file.file_helper.ensure_dir",
        lambda path: None
    )

    code, info = generate_and_save_testdata()
    assert code == ResultCode.SUCCESS
    assert "uuid" in info

def test_controller_user_fail(monkeypatch):
    monkeypatch.setattr(
        "workspace.modules.fake_data.fake_user.user_generator.generate_user_data",
        lambda: (ResultCode.ACCOUNT_GEN_FAIL, None)
    )
    # 其他可以不 patch，因為流程會在這裡 return
    code, info = generate_and_save_testdata()
    assert code == ResultCode.ACCOUNT_GEN_FAIL
    assert "帳號資料產生失敗" in info["msg"]

def test_controller_product_fail(monkeypatch):
    monkeypatch.setattr(
        "workspace.modules.fake_data.fake_user.user_generator.generate_user_data",
        lambda: (ResultCode.SUCCESS, {"user": 1})
    )
    monkeypatch.setattr(
        "workspace.modules.fake_data.fake_product.product_generator.generate_product_data",
        lambda: (ResultCode.PRODUCT_GEN_FAIL, None)
    )
    code, info = generate_and_save_testdata()
    assert code == ResultCode.PRODUCT_GEN_FAIL
    assert "商品資料產生失敗" in info["msg"]

def test_controller_uuid_fail(monkeypatch):
    monkeypatch.setattr(
        "workspace.modules.fake_data.fake_user.user_generator.generate_user_data",
        lambda: (ResultCode.SUCCESS, {"user": 1})
    )
    monkeypatch.setattr(
        "workspace.modules.fake_data.fake_product.product_generator.generate_product_data",
        lambda: (ResultCode.SUCCESS, {"product": 2})
    )
    monkeypatch.setattr(
        "workspace.utils.uuid.uuid_generator.generate_batch_uuid_with_code",
        lambda: (ResultCode.UUID_GEN_FAIL, None)
    )
    code, info = generate_and_save_testdata()
    assert code == ResultCode.UUID_GEN_FAIL
    assert "UUID 產生失敗" in info["msg"]

def test_controller_ensure_dir_fail(monkeypatch):
    # 目錄建立失敗
    def raise_io_error(path): raise IOError("mock dir fail")
    monkeypatch.setattr(
        "workspace.utils.file.file_helper.ensure_dir", raise_io_error
    )
    code, info = generate_and_save_testdata()
    assert code == ResultCode.USER_WRITE_FAIL
    assert "建立資料夾失敗" in info["msg"]

def test_controller_user_write_fail(monkeypatch):
    monkeypatch.setattr(
        "workspace.modules.fake_data.fake_user.user_generator.generate_user_data",
        lambda: (ResultCode.SUCCESS, {"user": 1})
    )
    monkeypatch.setattr(
        "workspace.modules.fake_data.fake_product.product_generator.generate_product_data",
        lambda: (ResultCode.SUCCESS, {"product": 2})
    )
    monkeypatch.setattr(
        "workspace.utils.uuid.uuid_generator.generate_batch_uuid_with_code",
        lambda: (ResultCode.SUCCESS, "testuuid")
    )
    monkeypatch.setattr(
        "workspace.utils.data.data_enricher.enrich_with_uuid",
        lambda data, uuid: {**data, "uuid": uuid}
    )
    # save_json 寫入 user 檔失敗
    def raise_io_error(data, path): raise IOError("mock user write fail")
    monkeypatch.setattr(
        "workspace.utils.data.data_loader.save_json", raise_io_error
    )
    code, info = generate_and_save_testdata()
    assert code == ResultCode.USER_WRITE_FAIL
    assert "帳號資料寫入失敗" in info["msg"]

def test_controller_product_write_fail(monkeypatch):
    # patch 前面步驟全都成功
    monkeypatch.setattr(
        "workspace.modules.fake_data.fake_user.user_generator.generate_user_data",
        lambda: (ResultCode.SUCCESS, {"user": 1})
    )
    monkeypatch.setattr(
        "workspace.modules.fake_data.fake_product.product_generator.generate_product_data",
        lambda: (ResultCode.SUCCESS, {"product": 2})
    )
    monkeypatch.setattr(
        "workspace.utils.uuid.uuid_generator.generate_batch_uuid_with_code",
        lambda: (ResultCode.SUCCESS, "testuuid")
    )
    monkeypatch.setattr(
        "workspace.utils.data.data_enricher.enrich_with_uuid",
        lambda data, uuid: {**data, "uuid": uuid}
    )

    # 這裡用 Side Effect 模擬第一次（user）成功，第二次（product）拋異常
    def save_json_side_effect(*args, **kwargs):
        if not hasattr(save_json_side_effect, "called"):
            save_json_side_effect.called = True
            return None  # 第一次呼叫（user）正常
        else:
            raise IOError("mock product write fail")  # 第二次呼叫（product）失敗

    monkeypatch.setattr(
        "workspace.utils.data.data_loader.save_json",
        save_json_side_effect
    )

    code, info = generate_and_save_testdata()
    assert code == ResultCode.PRODUCT_WRITE_FAIL
    assert "商品資料寫入失敗" in info["msg"]

