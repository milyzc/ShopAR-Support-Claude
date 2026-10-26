# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is
ShopAR Support API: a FastAPI service where every call to the model goes through an llm-guard pipeline. It is a training project for a course on secure AI use; the labs `../labllm` and `../labllm2` show the attacks, this repo shows the defenses in real code. All data is fictitious. The server binds to `127.0.0.1`.

Reply in Spanish (rioplatense). Code, comments, commits, specs and docs in English.

## Commands
- `uv run pytest` — unit tests with fake scanners (fast, no model download). One test: `uv run pytest tests/test_guard.py::test_blocking_scanner_blocks`
- `uv run ruff check .` / `uv run ruff format .`
- `uv run python -m shopar_support.eval` — runs `evals/attacks.yaml` against the real scanners and prints a report. Exit code 1 means some case did not get the expected result; that is a finding, not a broken build.
- `uv run shopar-support` — API on http://127.0.0.1:8000 (`POST /chat {"message": "..."}`). Uses Ollama (`OLLAMA_URL`, `OLLAMA_MODEL`) or a deterministic mock when it is down or `FORCE_MOCK=1`.

The first run of the real guard downloads several GB of Hugging Face models.

## Architecture
- `guard.py` — `Guard` runs input scanners before the model and output scanners after it. A scanner either sanitizes (the request continues with the cleaned text) or, if its class name is in `blocking_input`/`blocking_output`, blocks. `build_default_guard()` is the single place where scanners and their order are defined.
- The Anonymize/Deanonymize vault is shared state: `api.chat()` holds `guard.lock` and empties the vault before and after each request so one customer's data can never be restored into another's reply.
- `api.py` — the only route to the model. Tests swap the guard with `app.dependency_overrides[get_guard]`.
- `patterns.py` — Argentine identifiers (DNI, CBU) added as regex patterns, because Anonymize's NER only supports English and Chinese.
- `llm.py` — Ollama client plus `mock_reply()`.

## Known limitations (keep them visible, do not hide them)
- llm-guard is archived (no longer maintained) and `MaliciousURLs` fails because its model was removed from Hugging Face.
- `PromptInjection` uses an English-only model: it blocks benign Spanish messages. The eval shows these false positives on purpose.

## Workflow
Behavior changes go through OpenSpec: `/opsx:propose` → `/opsx:apply` → `/opsx:archive`. The current specs live in `openspec/specs/`, and open changes in `openspec/changes/`. Any change to what the guard blocks must also update `evals/attacks.yaml`.
