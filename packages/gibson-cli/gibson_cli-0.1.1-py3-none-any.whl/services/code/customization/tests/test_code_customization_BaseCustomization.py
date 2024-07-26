import pytest

from core.Configuration import Configuration
from services.code.customization.BaseCustomization import BaseCustomization


def test_preserve_exception():
    with pytest.raises(NotImplementedError):
        BaseCustomization(Configuration()).preserve()


def test_restore_exception():
    with pytest.raises(NotImplementedError):
        BaseCustomization(Configuration()).restore()
