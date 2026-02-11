<!--
Guidance for AI coding agents working on this repository.
This file is intentionally concise — follow the steps below before making changes.
-->

# Copilot instructions

Repository snapshot
- Primary files: [README.md](README.md) — currently contains only a project title.
- There are no `src/`, `tests/`, build configs, or CI manifests present.

Agent goals
- Treat this repository as an empty scaffold. Before implementing features, confirm the
  intended language, framework, and build/test tooling with the user.

What to do first (explicit, discoverable steps)
- Inspect [README.md](README.md) for project intent. If README lacks required info (it does), ask the user these 3 questions:
  1. What language/runtime should the project use? (e.g. Node.js, Python, Go)
  2. Do you want a minimal runnable demo, or are we adding to an existing app?
  3. Preferred test runner / CI target (e.g. GitHub Actions, none yet).
- Propose a minimal scaffold (source dir, simple build or run command, a single unit test).
- Create changes in a feature branch and open a pull request with a short description and a runnable example.

Project-specific conventions & patterns
- None are present. Adopt common, minimal conventions until told otherwise:
  - `src/` for sources, `tests/` for tests
  - `README.md` update for any new scaffold or commands
  - Small, focused commits with imperative messages (e.g. "Add Python project scaffold").

Developer workflows (what an agent should recommend or do)
- Before running or adding CI, ask the user for required secrets/credentials.
- When adding a language scaffold, include a short "try it" command in `README.md`.
  Example: for Python include `python -m venv .venv && .venv/bin/pip install -r requirements.txt && pytest`.

Integration points & dependencies
- No external integrations detected. If adding integrations (databases, external APIs), document required env vars and a local test stub.

When uncertain
- Prefer asking concise clarifying questions rather than guessing architecture or tooling.

Files to reference when making changes
- [README.md](README.md) — update with run/build instructions and minimal examples.

If you update this file
- Keep it short and actionable. Add concrete run/test commands you used while validating changes.

Questions for the maintainer
- Which language/runtime do you want for this project?
- Do you want CI added now, or only a local scaffold?
