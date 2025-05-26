# tests/test_account_generator.py

import pytest
from workspace.controller.account_generator_controller import run_generate_account

class TestAccountGenerator:

    def test_generate_account_success(self):
        result = run_generate_account()

        assert result["success"] is True
        assert "data" in result

        account = result["data"]

        if isinstance(account, dict):
            assert "username" in account
            assert "password" in account
        elif isinstance(account, list):
            assert len(account) > 0
            for item in account:
                assert "username" in item
                assert "password" in item
        else:
            pytest.fail("回傳格式錯誤，應為 dict 或 list")
