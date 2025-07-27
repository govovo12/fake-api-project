import pytest
from abc import ABCMeta
from workspace.utils.notifier.base import Notifier

pytestmark = [pytest.mark.unit, pytest.mark.notifier]


def test_notifier_is_abstract_class():
    """✅ 確保 Notifier 是抽象類別"""
    assert isinstance(Notifier, ABCMeta.__class__) or hasattr(Notifier, "__abstractmethods__")


def test_notifier_cannot_be_instantiated():
    """❌ 不能直接實例化 Notifier 抽象類別"""
    with pytest.raises(TypeError):
        Notifier()


def test_subclass_without_send_raises_error():
    """❌ 子類別若未實作 send，仍會因抽象方法報錯"""
    class IncompleteNotifier(Notifier):
        pass

    with pytest.raises(TypeError):
        IncompleteNotifier()


def test_subclass_with_send_can_instantiate():
    """✅ 子類別有實作 send 時，可成功建立實體"""
    class DummyNotifier(Notifier):
        def send(self, message: str) -> bool:
            return True

    instance = DummyNotifier()
    assert instance.send("test") is True
