import time

from assistant.system.capture import get_active_app, take_screenshot

print("Switch to VS Code or a browser. Checking in 4 seconds...")
time.sleep(4)
print("Active app:", get_active_app())

png = take_screenshot()
with open("test_screenshot.png", "wb") as f:
    f.write(png)
print("Saved test_screenshot.png  (size:", len(png), "bytes)")
print("PNG header OK:", png[:8] == b"\x89PNG\r\n\x1a\n")