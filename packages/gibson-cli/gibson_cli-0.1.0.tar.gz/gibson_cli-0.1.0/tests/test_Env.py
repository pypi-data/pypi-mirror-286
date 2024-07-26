import pytest

from core.Configuration import Configuration
from core.Env import Env


def test_verify_language_exception():
    configuration = Configuration()
    configuration.project.code.language = "invalid"

    with pytest.raises(RuntimeError) as e:
        Env().verify(configuration)

    assert str(e.value) == 'unrecognized language "invalid"'
