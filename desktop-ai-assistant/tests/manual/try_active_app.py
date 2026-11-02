import time
from assistant.system.capture import get_active_app, _active_process_name

print("Switch between apps (VS Code, Chrome, Notepad...). Prints for 20 seconds.\n")
for i in range(20):
    time.sleep(1)
    try:
        raw = _active_process_name()
    except Exception as e:
        raw = f"error: {e}"
    print(f"{i+1:2d}s  raw={raw:<20}  ->  {get_active_app()}")