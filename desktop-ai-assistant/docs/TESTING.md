# Manual Test Checklist (Integration Testing)

**Owner:** Member C | **When:** 2026-11-12 | **Where:** Windows 10, local machine (not WSL)

Automatic tests (`python -m pytest`) check small pieces of code. This file records the manual integration testing performed on the developer's Windows laptop.

---

## How to run a test round

1. Update and run the automatic tests first:
   ```bash
   git checkout main
   git pull origin main
   source venv/Scripts/activate        # Git Bash (PowerShell: .\venv\Scripts\Activate.ps1)
   pip install -r requirements.txt
   python -m pytest
   ```
2. Start the app: `python main.py` (or test the packaged application/installer when checking the release build).
3. Go through the checklist below. Mark each item **Pass**, **Fail** or **N/A**.
4. Fill one row in the **Test Log** at the bottom.
5. For every **Fail**, open a GitHub Issue (see "Reporting a bug").

---

## Checklist

| ID | Area | Test | What should happen | Result | Notes |
|---|---|---|---|---|---|
| T1 | Setup | Fresh venv + `pip install -r requirements.txt` + `python tests/manual/check_env.py` | No errors, "All good!" | **Pass** | Setup checks completed successfully. |
| T2 | Hotkey | Press the hotkey while **VS Code** is focused | Assistant opens | **Pass** | Worked as expected. |
| T3 | Hotkey | Press the hotkey while **Edge/Chrome** is focused | Assistant opens | **Pass** | Worked as expected. |
| T4 | Hotkey | Press the hotkey while **Notepad** is focused | Assistant opens | **Pass** | Worked as expected. |
| T5 | Hotkey | Press the hotkey 20 times quickly | No crash, no duplicate windows | **Pass** | No issue observed. |
| T6 | Hotkey | Change the hotkey in Settings | New hotkey works, old one does not | **Pass** | Worked as expected. |
| T7 | Selected text | Select text in **VS Code**, press hotkey ("Explain this") | Assistant explains that text | **Pass** | Worked as expected. |
| T8 | Selected text | Select text in a **browser**, press hotkey | Assistant explains that text | **Pass** | Worked as expected. |
| T9 | Selected text | Select nothing, press hotkey | Assistant just opens (no error) | **Pass** | No error observed. |
| T10 | Selected text | Copy "ABC", select other text, press hotkey, then Ctrl+V | "ABC" is pasted (clipboard restored) | **Pass** | Clipboard behavior worked as expected. |
| T11 | Active app | Hotkey from VS Code, then from a browser, then from Notepad | Modes: coding, lecture, general | **Pass** | Worked as expected. |
| T12 | Screenshot | Click "Explain my screen" | Answer describes what was on screen | **Pass** | Worked as expected. |
| T13 | Screenshot | Same test, look at what the AI described | Our assistant window is **not** in the screenshot | **Pass** | Worked as expected. |
| T14 | Screenshot | Use a **second monitor** | App and screenshot work, window stays on screen | **Pass** | No issue observed during testing. |
| T15 | AI | Save a **wrong API key**, ask something | Friendly error message, no crash | **Pass** | Error handled without an application crash. |
| T16 | AI | Turn **Wi-Fi off**, ask something | Friendly "no internet" message, no freeze | **Pass** | Offline network error handled without a freeze. |
| T17 | AI | Ask a long question | Answer appears word by word, window never freezes | **Pass** | Worked as expected. |
| T18 | AI | Ask for code | Code block is formatted, Copy button works | **Pass** | Worked as expected. |
| T19 | History | Chat, close the app, open it again | Old chat is still in History | **Pass** | History persisted after restart. |
| T20 | History | New chat, delete a chat | Works, no crash | **Pass** | Worked as expected. |
| T21 | Ollama | Switch to Ollama, Wi-Fi **off**, ask something | Local model answers | **N/A** | Ollama was not installed/configured or tested in this test round. Ollama functionality remains unverified. |
| T22 | Tray | Right click tray icon: Open, Settings, Quit | All three work, Quit really closes the app | **Pass** | Worked as expected. |
| T23 | Settings | Save API key, close, reopen app | Key is remembered (no key shown in plain text) | **Pass** | Worked as expected. |
| T24 | Auto-start | Enable "Start with Windows", sign out and sign in | App starts by itself | **Pass** | Worked as expected. |
| T25 | Auto-start | Disable it, sign out and sign in | App does not start | **Pass** | Worked as expected. |
| T26 | Installer | Install on a PC **without Python** | App installs and starts (Week 4) | **Pass*** | Installer was built, installed, and the application launched successfully on the developer's laptop. A separate clean-PC test with no Python installation is still recommended. |
| T27 | Installer | Uninstall | App and auto-start entry are removed (Week 4) | **Pass** | Uninstall test completed successfully. |

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

One manual test round was recorded on the developer's laptop.

| Date | Tester | Windows | Python | Branch / commit | Passed | Failed | N/A | Issues opened |
|---|---|---|---|---|---:|---:|---:|---|
| 2026-11-12 | Member C | Windows 10 | 3.14.7 | Not recorded | 26* | 0 | 1 | None reported |

\*T26 passed on the developer's laptop, but the specific "without Python" condition has not yet been independently verified. For strict checklist counting, treat T26 as **N/A / pending clean-PC verification** until it is tested on a machine without Python. Therefore, the strict verified count is **25 Pass, 0 Fail, 2 N/A/pending**.

### Details of the latest round

| ID | Result (Pass / Fail / N/A) | Notes / issue number |
|---|---|---|
| T1 | Pass | Environment setup/check completed successfully. |
| T2 | Pass | Hotkey opened assistant from VS Code. |
| T3 | Pass | Hotkey opened assistant from browser. |
| T4 | Pass | Hotkey opened assistant from Notepad. |
| T5 | Pass | Repeated hotkey presses caused no observed crash or duplicate windows. |
| T6 | Pass | Updated hotkey behavior worked as expected. |
| T7 | Pass | Selected text from VS Code was explained. |
| T8 | Pass | Selected text from browser was explained. |
| T9 | Pass | Assistant opened normally when no text was selected. |
| T10 | Pass | Clipboard was restored as expected. |
| T11 | Pass | Active-app modes behaved as expected. |
| T12 | Pass | Screen explanation worked. |
| T13 | Pass | Assistant window was excluded from the captured screenshot. |
| T14 | Pass | Second-monitor behavior worked during testing. |
| T15 | Pass | Wrong API key produced a handled error; app did not crash. |
| T16 | Pass | No-internet condition was handled without freezing. |
| T17 | Pass | Long-answer streaming worked without freezing. |
| T18 | Pass | Code formatting and Copy button worked. |
| T19 | Pass | Chat history remained after restarting the app. |
| T20 | Pass | New chat and delete-chat actions worked. |
| T21 | N/A | Ollama was not tested. Local-model/offline Ollama behavior is not verified. |
| T22 | Pass | Tray Open, Settings, and Quit actions worked. |
| T23 | Pass | API key persistence worked; no plain-text display was observed. |
| T24 | Pass | Start with Windows worked. |
| T25 | Pass | Disabling Start with Windows worked. |
| T26 | Pass* | Installer successfully installed and launched the app on the developer's laptop. Clean-PC/no-Python condition still needs a separate test. |
| T27 | Pass | Uninstall completed successfully. |

---

## Overall result

The application passed the manual tests performed on the developer's Windows 10 laptop, with no failures reported.

**Not tested:** T21 (Ollama).

**Recommended additional verification:** T26 should be repeated on a clean Windows PC that does not have Python installed, to confirm the installer works independently of the developer's Python environment.

No GitHub issues were reported for this test round.
