import os


def test_os_mode():
    assert os.getenv("MODE") == "TEST"
