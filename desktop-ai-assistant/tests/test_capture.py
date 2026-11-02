from assistant.system.capture import classify_app


def test_vscode():
    assert classify_app("Code.exe") == "vscode"
    assert classify_app("code - insiders.exe") == "vscode"


def test_browsers():
    for name in ("chrome.exe", "msedge.exe", "firefox.exe", "brave.exe"):
        assert classify_app(name) == "browser"


def test_case_is_ignored():
    assert classify_app("CHROME.EXE") == "browser"


def test_other_apps():
    assert classify_app("notepad.exe") == "other"
    assert classify_app("") == "other"