# Manual Test Checklist (Integration Testing)

**Owner:** Member C | **When:** every week (and before every milestone) | **Where:** Windows 10/11, not WSL

Automatic tests (`python -m pytest`) check small pieces of code. This file checks that **the whole app works together** the way a real user will use it.

---

## How to run a test round

1. Update and run the automatic tests first:
   ```bash
   git checkout main
   git pull origin main
   source venv/Scripts/activate        # Git Bash   (PowerShell: venv\Scripts\Activate.ps1)
   pip install -r requirements.txt
   python -m pytest
   ```
2. Start the app: `python main.py`
3. Go through the checklist below. Mark each item **Pass**, **Fail** or **N/A** (feature not built yet).
4. Fill one row in the **Test Log** at the bottom.
5. For every **Fail**, open a GitHub Issue (see "Reporting a bug").

---

## Checklist

| ID | Area | Test | What should happen |
|---|---|---|---|
| T1 | Setup | Fresh venv + `pip install -r requirements.txt` + `python tests/manual/check_env.py` | No errors, "All good!" |
| T2 | Hotkey | Press the hotkey while **VS Code** is focused | Assistant opens |
| T3 | Hotkey | Press the hotkey while **Edge/Chrome** is focused | Assistant opens |
| T4 | Hotkey | Press the hotkey while **Notepad** is focused | Assistant opens |
| T5 | Hotkey | Press the hotkey 20 times quickly | No crash, no duplicate windows |
| T6 | Hotkey | Change the hotkey in Settings | New hotkey works, old one does not |
| T7 | Selected text | Select text in **VS Code**, press hotkey ("Explain this") | Assistant explains that text |
| T8 | Selected text | Select text in a **browser**, press hotkey | Assistant explains that text |
| T9 | Selected text | Select nothing, press hotkey | Assistant just opens (no error) |
| T10 | Selected text | Copy "ABC", select other text, press hotkey, then Ctrl+V | "ABC" is pasted (clipboard restored) |
| T11 | Active app | Hotkey from VS Code, then from a browser, then from Notepad | Modes: coding, lecture, general |
| T12 | Screenshot | Click "Explain my screen" | Answer describes what was on screen |
| T13 | Screenshot | Same test, look at what the AI described | Our assistant window is **not** in the screenshot |
| T14 | Screenshot | Use a **second monitor** | App and screenshot work, window stays on screen |
| T15 | AI | Save a **wrong API key**, ask something | Friendly error message, no crash |
| T16 | AI | Turn **Wi-Fi off**, ask something | Friendly "no internet" message, no freeze |
| T17 | AI | Ask a long question | Answer appears word by word, window never freezes |
| T18 | AI | Ask for code | Code block is formatted, Copy button works |
| T19 | History | Chat, close the app, open it again | Old chat is still in History |
| T20 | History | New chat, delete a chat | Works, no crash |
| T21 | Ollama | Switch to Ollama, Wi-Fi **off**, ask something | Local model answers |
| T22 | Tray | Right click tray icon: Open, Settings, Quit | All three work, Quit really closes the app |
| T23 | Settings | Save API key, close, reopen app | Key is remembered (no key shown in plain text) |
| T24 | Auto-start | Enable "Start with Windows", sign out and sign in | App starts by itself |
| T25 | Auto-start | Disable it, sign out and sign in | App does not start |
| T26 | Installer | Install on a PC **without Python** | App installs and starts (Week 4) |
| T27 | Installer | Uninstall | App and auto-start entry are removed (Week 4) |

---

## Reporting a bug

Create a GitHub Issue (**Issues > New issue > Bug report**). The template asks for these parts:

1. **Title:** short and clear, e.g. `Hotkey does not open assistant in Notepad`
2. **Steps to reproduce:** numbered, exact steps
3. **Expected result**
4. **Actual result**
5. **Environment:** Windows version, Python version, branch / commit
6. **Screenshot or error text:** paste the screenshot into the issue (drag and drop or Ctrl+V)
7. **Labels and assignee:** label `bug` (+ `ui`, `ai` or `system`) and assign the owner of that part:

| Problem is in | Assign to |
|---|---|
| Window, buttons, tray, settings, theme, installer | Member A |
| AI answer, streaming, history, API key, Ollama, errors | Member B |
| Hotkey, selected text, screenshot, active app, auto-start | Member C |

### Severity (write it in the issue title or a comment)

| Level | Meaning | Example |
|---|---|---|
| **High** | App crashes or main feature does not work | Hotkey never opens the app |
| **Medium** | Feature works but wrongly | Wrong mode chosen in a browser |
| **Low** | Small visual or wording problem | Button text cut off |

---

## Test Log

Copy one row per test round.

| Date | Tester | Windows | Python | Branch / commit | Passed | Failed | N/A | Issues opened |
|---|---|---|---|---|---|---|---|---|
| 2026-11-__ | | | | main @ ______ | | | | #__, #__ |

### Details of the latest round

| ID | Result (Pass / Fail / N/A) | Notes / issue number |
|---|---|---|
| T1 | | |
| T2 | | |
| T3 | | |
| T4 | | |
| T5 | | |
| T6 | | |
| T7 | | |
| T8 | | |
| T9 | | |
| T10 | | |
| T11 | | |
| T12 | | |
| T13 | | |
| T14 | | |
| T15 | | |
| T16 | | |
| T17 | | |
| T18 | | |
| T19 | | |
| T20 | | |
| T21 | | |
| T22 | | |
| T23 | | |
| T24 | | |
| T25 | | |
| T26 | | |
| T27 | | |