import sys

import pytest

from assistant.system import autostart


def test_command_for_packaged_exe(monkeypatch):
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", r"C:\Apps\DesktopAIAssistant.exe")
    assert autostart._command() == '"C:\\Apps\\DesktopAIAssistant.exe"'


def test_command_from_source_points_to_main_py(monkeypatch):
    monkeypatch.delattr(sys, "frozen", raising=False)
    cmd = autostart._command()
    assert cmd.startswith('"')
    assert cmd.endswith('main.py"')


def test_registry_roundtrip_on_windows(monkeypatch):
    """Real registry test (skipped automatically on Linux/WSL).
    Uses a different value name so the real auto-start entry is never touched."""
    pytest.importorskip("winreg")
    monkeypatch.setattr(autostart, "_NAME", "DesktopAIAssistantTest")

    try:
        autostart.enable_autostart()
        assert autostart.is_autostart_enabled() is True
        autostart.disable_autostart()
        assert autostart.is_autostart_enabled() is False
        autostart.disable_autostart()   # second call must not raise
    finally:
        autostart.disable_autostart()