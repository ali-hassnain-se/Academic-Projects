"""Manual helper for auto-start.

Usage (Windows, from the project folder):
    python -m tests.manual.try_autostart on       # enable
    python -m tests.manual.try_autostart off      # disable
    python -m tests.manual.try_autostart          # only show status
"""
import sys

from assistant.system import autostart

action = sys.argv[1] if len(sys.argv) > 1 else "status"

if action == "on":
    autostart.enable_autostart()
elif action == "off":
    autostart.disable_autostart()

print("Enabled:", autostart.is_autostart_enabled())
print("Command:", autostart._command())