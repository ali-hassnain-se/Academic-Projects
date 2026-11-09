"""Paths that work both from source and from the packaged .exe."""
import sys
from pathlib import Path

from platformdirs import user_config_dir

from assistant.config import APP_NAME


def resource_path(relative: str) -> str:
    """Path of a bundled file such as 'assets/icon.ico'.

    From source: relative to the project folder.
    From the PyInstaller .exe: relative to the unpacked bundle folder."""
    base = getattr(sys, "_MEIPASS", None)
    root = Path(base) if base else Path(__file__).resolve().parents[1]
    return str(root / relative)


def settings_file() -> Path:
    """settings.json inside the user's config folder (always writable)."""
    folder = Path(user_config_dir(APP_NAME, appauthor=False))
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "settings.json"