# Architecture

This page shows how the Desktop AI Assistant is built. GitHub draws the diagrams below automatically (they are written in Mermaid).

## 1. Big picture

```mermaid
flowchart LR
    U(["User"]) -->|"Ctrl+Space or bubble click"| HK["Hotkey listener<br/>assistant/system/hotkey.py<br/>(Member C)"]
    HK -->|"Qt signal"| GUI["GUI window<br/>assistant/ui/<br/>(Member A)"]

    GUI -->|"before showing the window"| CAP["Capture<br/>assistant/system/capture.py<br/>(Member C)"]
    CAP -.->|"selected text, screenshot, active app"| GUI

    GUI -->|"ask(prompt, image, mode)"| AI["AI client<br/>assistant/ai/client.py<br/>(Member B)"]
    AI --> P{"Provider"}
    P -->|"online"| GEM["Google Gemini API"]
    P -->|"offline"| OLL["Ollama<br/>local model"]
    GEM -->|"streamed text"| AI
    OLL -->|"streamed text"| AI
    AI -->|"text chunks"| GUI
    GUI -->|"answer, word by word"| U

    AI --> DB[("SQLite history<br/>assistant/storage/")]
    GUI -->|"New chat, History"| DB
    SET["Settings and API key<br/>keyring + config"] --> AI
    GUI --> SET
    AUTO["Auto-start<br/>assistant/system/autostart.py<br/>(Member C)"] -.->|"starts the app at login"| GUI
```

## 2. What happens when the user presses the hotkey

```mermaid
sequenceDiagram
    actor U as User
    participant HK as Hotkey (C)
    participant CAP as Capture (C)
    participant GUI as GUI (A)
    participant AI as AI client (B)
    participant LLM as Gemini / Ollama
    participant DB as History (B)

    U->>HK: presses Ctrl+Space
    HK->>GUI: callback on a background thread, sends a Qt signal
    GUI->>CAP: get_active_app() and get_selected_text()
    CAP-->>GUI: "vscode" and the selected text
    GUI->>GUI: show the overlay window
    GUI->>AI: ask(prompt, image, mode) in a worker thread
    AI->>LLM: system prompt + last messages + question
    LLM-->>AI: answer in small chunks
    AI-->>GUI: chunks arrive as signals
    GUI-->>U: text appears word by word
    AI->>DB: save question and answer
```

Why `get_active_app()` and `get_selected_text()` are called **before** the window is shown: once our window opens it takes the focus, and the active app would always be "other".

## 3. Explain my screen

```mermaid
sequenceDiagram
    actor U as User
    participant GUI as GUI (A)
    participant CAP as Capture (C)
    participant AI as AI client (B)

    U->>GUI: clicks "Explain my screen"
    GUI->>GUI: hide the window, wait about 200 ms
    GUI->>CAP: take_screenshot()
    CAP-->>GUI: PNG bytes (resized to 1600 px wide)
    GUI->>GUI: show the window again
    GUI->>AI: ask("Explain my screen", image=png, mode="screen")
    AI-->>GUI: streamed explanation
    GUI-->>U: answer
```

The window is hidden first so it does not appear in its own screenshot.

## 4. Threads

| Thread | What runs there | Rule |
|---|---|---|
| Main (GUI) thread | All windows, buttons and text | Only this thread may change widgets |
| Hotkey thread (created by `pynput`) | The hotkey callback | Must only send a Qt signal, never touch widgets |
| Worker thread | `ask()` (network call, streaming) | Sends each chunk back to the GUI as a signal |

## 5. Layers and ownership

| Layer | Folder | Owner | Talks to |
|---|---|---|---|
| GUI | `assistant/ui/` | Member A | System, AI client, history |
| AI and data | `assistant/ai/`, `assistant/storage/` | Member B | Gemini, Ollama, SQLite, keyring |
| System | `assistant/system/` | Member C | Windows (keyboard, clipboard, screen, registry) |

The layers only talk to each other through the agreed functions: `ask()`, `get_api_key()`, the history functions, `get_selected_text()`, `take_screenshot()`, `get_active_app()`, `register_hotkey()` and `enable_autostart()`.

## 6. Exporting a picture (for slides)

1. Open https://mermaid.live
2. Paste the code of one diagram (the part between the three backticks, without the word `mermaid`).
3. Click **Actions > PNG** and save it into `docs/images/`.