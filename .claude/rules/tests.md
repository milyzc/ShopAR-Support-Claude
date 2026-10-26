---
paths:
  - "tests/**"
  - "evals/**"
---
- Fictitious data only. Credentials must be documented examples (e.g. `AKIAIOSFODNN7EXAMPLE`) or obviously fake; never anything with a real provider format that could trip secret scanning.
- Unit tests use fake scanners from `tests/test_guard.py`; they must not download models.
- Each case in `evals/attacks.yaml` declares its OWASP risk (or `-` for benign cases) and its expected result.
- Never change an `expect` value to make the eval pass. A failing case is a finding: report it.
