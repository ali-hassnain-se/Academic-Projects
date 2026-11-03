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

from assistant.system import capture


def test_get_active_app_vscode(monkeypatch):
    monkeypatch.setattr(capture, "_active_process_name", lambda: "Code.exe")
    assert capture.get_active_app() == "vscode"


def test_get_active_app_never_raises(monkeypatch):
    def boom():
        raise RuntimeError("no window")
    monkeypatch.setattr(capture, "_active_process_name", boom)
    assert capture.get_active_app() == "other"