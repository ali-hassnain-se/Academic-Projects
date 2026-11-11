# Multi-Laptop Test Report (Release Candidate)

**Owner:** Member C | **Installer under test:** `DesktopAIAssistant-Setup.exe` (from Member A) | **Version / commit:** ______

Goal: prove that the installed app works on computers that are **not** the developers' laptops, especially one **without Python**.

---

## 1. Laptops

| ID | Owner | Windows version (`Win+R` > `winver`) | Edition (Home / Pro) | 64-bit? | Python installed? | Antivirus | Screen scaling (100/125/150%) | Monitors |
|---|---|---|---|---|---|---|---|---|
| L1 | Member C (Developer Laptop) | Windows 10 (exact version pending) | To be recorded | Yes | Yes | To be recorded | To be recorded | To be recorded |
| L2 | Pending | Pending | Pending | Pending | Yes / No | Pending | Pending | Pending |
| L3 | Pending (Clean Laptop) | Pending | Pending | Pending | No | Pending | Pending | Pending |

**L1 Status:** Application successfully tested on the developer laptop.
All performed tests passed without application errors.

**L2 and L3:** Testing pending.

At least one laptop must have no Python installed.

---

## 2. Preparation (before testing)

- [ ] Ask Member A for a **pre-release installer**. Best way: GitHub > Releases > Draft a new release > tag `v1.0.0-rc1` > tick **Set as a pre-release** > attach the installer. Testers then download it exactly like a real user.
- [ ] Each tester has their **own Gemini API key** (https://aistudio.google.com/apikey). Never share keys in the group chat.
- [ ] Keep a screen recorder or `Win+Shift+S` ready for screenshots of problems.
- [ ] Ask Member A to make the app write a **log file** (for example `%LOCALAPPDATA%\DesktopAIAssistant\logs\app.log`). Without it, errors on a friend's laptop are almost impossible to diagnose.

---

## 3. Test steps (run on every laptop)

Mark **Pass / Fail / N/A** in the results table (section 4). Write the Issue number for every Fail.

| Step | Test | Expected result |
|---|---|---|
| S1 | Download the installer from the GitHub release page | Download completes |
| S2 | Run it. If Windows shows **"Windows protected your PC"**: click **More info > Run anyway** (the app is not code-signed) | Setup wizard opens |
| S3 | Finish the installation | Installs without error; Start menu shortcut exists |
| S4 | Start the app | Bubble or tray icon appears within a few seconds; no console window; no crash |
| S5 | First-run API key flow: paste the key in Settings, save | Key accepted; no key shown in plain text afterwards |
| S6 | Ask a short question | Answer streams in word by word; window does not freeze |
| S7 | Press the hotkey in **Notepad** | Assistant opens |
| S8 | Press the hotkey in **Edge/Chrome** | Assistant opens |
| S9 | Press the hotkey in **VS Code** (if installed) | Assistant opens |
| S10 | Select text in a browser, press the hotkey ("Explain this") | Assistant explains the selected text |
| S11 | Select nothing, press the hotkey | Assistant just opens, no error |
| S12 | Click **Explain my screen** | Answer describes the screen; assistant window is not in the screenshot |
| S13 | Ask 2 questions, close the app completely (tray > Quit), start it again | Old chats are in History |
| S14 | Tray icon menu: Open, Settings, Quit | All work; Quit really ends the app (check Task Manager) |
| S15 | Switch theme (dark/light) and restart | Theme is remembered |
| S16 | Turn **Wi-Fi off**, ask something | Friendly "no internet" message; no freeze or crash |
| S17 | Wrong API key, ask something | Friendly "invalid key" message; then correct key works again |
| S18 | Enable **Start with Windows**, **restart the laptop**, log in | App starts by itself (Task Manager > Startup shows the entry) |
| S19 | Disable it, restart, log in | App does not start |
| S20 | If a second monitor or 125%/150% scaling is available | Windows stay on screen, text is not cut off |
| S21 | Check resource use (Task Manager > Details) while idle | Reasonable (write the RAM number in the notes) |
| S22 | **Uninstall:** Settings > Apps > Installed apps > Desktop AI Assistant > Uninstall | App removed; no entry left in Task Manager > Startup; shortcut gone |
| S23 | (Only on a laptop with Ollama) Wi-Fi off, switch to Ollama, ask something | Local model answers |

---

## 4. Results

Legend:
- PASS = Test completed successfully
- FAIL = Test failed
- N/A = Not applicable
- PENDING = Not tested yet

| Step | L1 | L2 | L3 | Issue # |
|---|---|---|---|---|
| S1 | PENDING | PENDING | PENDING | - |
| S2 | PASS | PENDING | PENDING | - |
| S3 | PASS | PENDING | PENDING | - |
| S4 | PASS | PENDING | PENDING | - |
| S5 | PASS | PENDING | PENDING | - |
| S6 | PASS | PENDING | PENDING | - |
| S7 | PASS | PENDING | PENDING | - |
| S8 | PASS | PENDING | PENDING | - |
| S9 | PASS | PENDING | PENDING | - |
| S10 | PASS | PENDING | PENDING | - |
| S11 | PASS | PENDING | PENDING | - |
| S12 | PASS | PENDING | PENDING | - |
| S13 | PASS | PENDING | PENDING | - |
| S14 | PASS | PENDING | PENDING | - |
| S15 | PASS | PENDING | PENDING | - |
| S16 | PASS | PENDING | PENDING | - |
| S17 | PASS | PENDING | PENDING | - |
| S18 | PASS | PENDING | PENDING | - |
| S19 | PASS | PENDING | PENDING | - |
| S20 | PASS | PENDING | PENDING | - |
| S21 | PASS | PENDING | PENDING | - |
| S22 | PASS | PENDING | PENDING | - |
| S23 | N/A (if Ollama not installed) | PENDING | PENDING | - |

**L1 Summary:**
- Application tested successfully on the developer laptop.
- All performed applicable tests passed.
- No application errors encountered.
- GitHub Release download test (S1) is pending.
- No release-blocking issue reported so far.

**L2 and L3 Summary:**
- Testing has not started yet.

---

## 5. Notes per laptop

### L1: Developer Laptop (Member C)

- Windows version: Windows 10 (exact build to be recorded using `winver`)
- Python installed: Yes
- Source code available: Yes
- Installer tested: Yes
- Application status: PASS
- Windows warnings during installation: None reported
- Time from double-click to a usable app: Not recorded
- RAM used when idle: Not recorded
- Problems found: No application errors encountered during performed tests
- Screenshots: To be added if needed
- Overall result: PASS for performed applicable tests

### L2: (Owner / Date)

- Windows version:
- Python installed:
- Windows warnings during installation:
- Time from double-click to a usable app:
- RAM used when idle:
- Problems found:
- Screenshots:

### L3: Clean Laptop (Owner / Date)

- Windows version:
- Python installed: No
- Source code available: No
- Git installed: No
- VS Code installed: No
- Windows warnings during installation:
- Time from double-click to a usable app:
- RAM used when idle:
- Problems found:
- Screenshots:

---

## 6. Bugs found

| Issue | Laptop | Step | Severity (High / Medium / Low) | Assigned to | Fixed in | Retested |
|---|---|---|---|---|---|---|
| #__ | | | | | rc2 / commit | Yes / No |

For every bug open a GitHub Issue (**Bug report** template) with: steps, expected, actual, Windows version, laptop ID, the log file and a screenshot. Label `bug`, add `ui` / `ai` / `system`, and assign the owner.

---

## 7. Sign-off

Release can go ahead when:

- [ ] All **High** bugs are fixed and retested on the laptop where they appeared
- [ ] At least one laptop **without Python** passed S1 to S6, S18 and S22
- [ ] Remaining Medium / Low bugs are written in the README under "Known limitations"
- [ ] The installer used for the final test is the same file that goes to the GitHub Release

Tested by: ____________  Date: ____________