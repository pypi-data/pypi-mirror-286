import platform

from conf.Platform import Platform


def test_system():
    assert Platform().system == platform.system().lower()
