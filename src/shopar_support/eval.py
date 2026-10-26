"""Run the attack corpus against the real guard and print a Markdown report.

Usage: uv run python -m shopar_support.eval [evals/attacks.yaml]
Exit code 1 if any case does not get the expected result.
"""

import sys
from pathlib import Path

import yaml

from .guard import Guard, GuardResult, build_default_guard


def run_case(guard: Guard, case: dict) -> tuple[GuardResult, str]:
    text = case["text"] * case.get("repeat", 1)
    guard.reset_vault()
    if case["kind"] == "input":
        result = guard.check_input(text)
    else:
        result = guard.check_output("", text)
    got = "block" if result.blocked else "redact" if result.text != text else "allow"
    return result, got


def passed(case: dict, result: GuardResult, got: str) -> bool:
    if case["expect"] == "redact":
        return got == "redact" and not any(s in result.text for s in case.get("must_not_contain", []))
    return got == case["expect"]


def main(argv: list[str] | None = None) -> int:
    path = Path(argv[0] if argv else "evals/attacks.yaml")
    cases = yaml.safe_load(path.read_text(encoding="utf-8"))
    guard = build_default_guard()

    print("| Case | OWASP | Expected | Got | Scanners flagged | |\n|---|---|---|---|---|---|")
    failures = []
    for case in cases:
        result, got = run_case(guard, case)
        ok = passed(case, result, got)
        if not ok:
            failures.append((case, got))
        print(
            f"| {case['id']} | {case['owasp']} | {case['expect']} | {got} | {', '.join(result.failed) or '-'} | {'✅' if ok else '❌'} |"
        )

    false_positives = [c for c, got in failures if c["expect"] == "allow"]
    print(
        f"\n{len(cases) - len(failures)}/{len(cases)} as expected · "
        f"{len(false_positives)} false positive(s) · {len(failures) - len(false_positives)} miss(es)"
    )
    for case, got in failures:
        print(f"- {case['id']}: expected {case['expect']}, got {got}. {case.get('note', '')}".rstrip())
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
