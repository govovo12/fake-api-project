# tests/unit/test_random_factory.py

import pytest
from workspace.utils.random_factory import simple_random_string

class TestRandomFactory:

    def test_generate_string_default_length(self):
        result = simple_random_string()
        assert isinstance(result, str)
        assert len(result) == 8

    def test_generate_string_custom_length(self):
        result = simple_random_string(length=12)
        assert isinstance(result, str)
        assert len(result) == 12

    def test_generate_string_with_prefix(self):
        result = simple_random_string(length=5, prefix="abc")
        assert result.startswith("abc")
        assert len(result) == 8  # 3 prefix + 5 generated
