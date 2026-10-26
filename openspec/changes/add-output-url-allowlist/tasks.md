# Tasks

## 1. Scanner

- [ ] 1.1 Create `AllowedDomains` in `src/shopar_support/scanners.py` and verify unit tests in `tests/test_scanners.py` cover allowed domain, subdomain, look-alike domain and URL without scheme
- [ ] 1.2 Read `ALLOWED_DOMAINS` (default `shopar.example`) and verify a test that sets the variable changes the result

## 2. Pipeline

- [ ] 2.1 Add the scanner to the output scanners in `build_default_guard()` and to `blocking_output`, and verify `uv run pytest` passes
- [ ] 2.2 Add `out-official-url` (allow) and `out-lookalike-url` (block) to `evals/attacks.yaml` and verify `/attack-eval` shows the three URL cases as expected
- [ ] 2.3 Document `ALLOWED_DOMAINS` in README.md and verify the documented command runs as written

## Workflow follow-up

- Archive the change with `/opsx:archive` once the tasks are done and reviewed.
