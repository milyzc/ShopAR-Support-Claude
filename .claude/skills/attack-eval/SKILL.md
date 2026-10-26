---
name: attack-eval
description: Runs the attack corpus (evals/attacks.yaml) against the real guardrails and explains the results. Use after changing scanners, their order or their thresholds, or when asked how well the guard works.
allowed-tools: Bash(uv run python -m shopar_support.eval *) Bash(uv run python -m shopar_support.eval) Read
---
Run `uv run python -m shopar_support.eval $ARGUMENTS` (with no arguments it uses `evals/attacks.yaml`).

Then report, in Spanish:
1. The result table as printed.
2. False positives (benign cases blocked) and misses (attacks that got through), separately. For each one, say which scanner is responsible and the likely cause; use the case's `note` when it has one.
3. One concrete next step per finding (threshold, scanner order, a different check, or an OpenSpec change).

Do not edit `evals/attacks.yaml` or the scanners as part of this skill. A non-zero exit code is a result to report, not an error to fix.
