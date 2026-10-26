---
paths:
  - "src/**/*.py"
---
- Never call `llm.complete()` or the Ollama API outside `api.chat()`: every model call goes through the guard.
- Never log, print or return the customer's original message or the model's raw reply. Log scanner names and scores only.
- A new scanner goes in `build_default_guard()`. Decide explicitly whether it blocks or sanitizes, and say why in a comment.
- Every new scanner adds at least one attack case and one benign case to `evals/attacks.yaml`.
- Prefer deterministic checks (allowlists, parsing) over ML classifiers when both solve the problem.
