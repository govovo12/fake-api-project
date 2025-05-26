import pytest
from workspace.utils.random_factory import simple_random_string

class TestRandomFactory:

    def test_generate_string_default_length(self):
        result = simple_random_string(8)
        assert isinstance(result, list)
        assert len(result) == 8

    def test_generate_string_custom_length(self):
        result = simple_random_string(12)
        assert isinstance(result, list)
        assert len(result) == 12

    def test_generate_string_is_alphanumeric(self):
        result = simple_random_string(10)
        for ch in result:
            assert ch.isalnum()
