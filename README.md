# Academic Projects | BS Software Engineering

A central repository for the software engineering projects, system designs, UI/UX prototypes and lab work I develop during my undergraduate studies. Each project lives in its own folder with its own README, documentation and source files.

![Status](https://img.shields.io/badge/status-actively%20maintained-brightgreen)
![Degree](https://img.shields.io/badge/BS-Software%20Engineering-blue)

---

## Table of Contents

- [Projects at a Glance](#projects-at-a-glance)
- [Featured Projects](#featured-projects)
- [Repository Structure](#repository-structure)
- [Tech Stack and Tools](#tech-stack-and-tools)
- [Getting Started](#getting-started)
- [Conventions](#conventions)
- [About the Author](#about-the-author)

---

## Projects at a Glance

| # | Project | Course | Domain | Status |
|---|---|---|---|---|
| 1 | [Campus Emergency Assistance (CEA)](Campus-Emergency-Assistance-CEA/) | Human-Computer Interaction | UI/UX design and low-fidelity prototyping | Prototype |
| 2 | [Desktop AI Assistant](desktop-ai-assistant/) | Artificial Intelligence | Desktop application, LLM integration | In development (team project) |

---

## Featured Projects

### 1. Campus Emergency Assistance (CEA)

A mobile-first emergency assistance application that connects campus students with medical, fire, security and administrative services quickly and efficiently.

| | |
|---|---|
| **Course** | Human-Computer Interaction (HCI) |
| **Domain** | UI/UX design and low-fidelity prototyping |
| **Deliverables** | Interactive prototype, UI flow diagrams, HCI report |
| **Tools** | Figma, Draw.io, Markdown, LaTeX |

Open the project folder: [Campus-Emergency-Assistance-CEA](Campus-Emergency-Assistance-CEA/)

---

### 2. Desktop AI Assistant

A floating AI assistant for Windows that stays on top of whatever you are doing. Press a hotkey in VS Code, a browser lecture or a coding-practice site, and a small chat window opens, so you can ask about selected text or your whole screen without switching tabs.

| | |
|---|---|
| **Course** | Artificial Intelligence |
| **Domain** | Desktop application, LLM integration, context-aware prompting |
| **Team** | 3 members (GUI, backend, system integration) |
| **Key features** | Global hotkey, explain selected text, explain my screen, active-app detection, Gemini and offline Ollama models, chat history, start with Windows |
| **Tools** | Python, PySide6, Google Gemini API, Ollama, SQLite, pynput, pytest, PyInstaller |
| **Status** | In development, first release (v1.0.0) planned for mid-November 2026 |

Open the project folder: [desktop-ai-assistant](desktop-ai-assistant/)

---

## Repository Structure

```text
Academic-Projects/
│
├── Campus-Emergency-Assistance-CEA/
│   ├── README.md               # Project details and prototype showcase
│   ├── assets/                 # PNG screenshots and UI flow diagrams
│   ├── design/                 # Figma source files (.fig)
│   └── docs/                   # HCI reports and documentation
│
├── desktop-ai-assistant/
│   ├── README.md               # Features, installation, usage, team
│   ├── main.py                 # Application entry point
│   ├── requirements.txt        # Python dependencies
│   ├── assistant/              # Source code (ui, ai, storage, system)
│   ├── tests/                  # Automatic and manual tests
│   ├── docs/                   # Architecture, testing checklist, guides
│   └── assets/                 # Icons and images
│
├── .github/                    # Issue and pull request templates
│
└── [Future-Projects]/          # Other semester projects and labs
```

---

## Tech Stack and Tools

| Area | Technologies |
|---|---|
| Programming | Python, C++, SQL / MySQL |
| UI/UX and prototyping | Figma, Draw.io, Justinmind |
| Desktop and AI | PySide6, Google Gemini API, Ollama |
| Testing | pytest |
| Documentation and reports | Markdown, LaTeX, MS Word, Mermaid diagrams |
| Version control and collaboration | Git, GitHub (issues, pull requests, project boards) |

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/ali-hassnain-se/Academic-Projects.git
cd Academic-Projects
```

Then open the folder of the project you are interested in and follow the instructions in its own `README.md`. For example, to run the Desktop AI Assistant (Windows):

```bash
cd desktop-ai-assistant
python -m venv venv
source venv/Scripts/activate        # PowerShell: venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

---

## Conventions

- **One folder per project**, each with its own `README.md`.
- **Branches:** `feature/<name>`, `fix/<name>`, `docs/<name>`. Work is merged into `main` through Pull Requests.
- **Commit messages:** `type(area): message`, for example `feat(system): add global hotkey listener`.
- **Secrets** (API keys, passwords) are never committed.

---

## About the Author

**Rana Ali Hassnain**: BS Software Engineering student (2024 to 2028) at Superior College, affiliated with GCUF. Interested in data structures and algorithms, backend development, and open source (KDE contributor).

GitHub: [@ali-hassnain-se](https://github.com/ali-hassnain-se)

---

<sub>These projects are created for academic purposes.</sub>
