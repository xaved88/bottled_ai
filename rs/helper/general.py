import sys


def can_handle_screenshots() -> bool:
    return sys.platform == "win32"