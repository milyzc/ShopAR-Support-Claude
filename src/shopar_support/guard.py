"""Guardrail pipeline: every call to the model goes through check_input and check_output.

Scanners follow llm-guard's protocol: scan(text) -> (sanitized, is_valid, risk_score)
for input, scan(prompt, output) -> (...) for output. Some scanners only sanitize
(the request continues with the cleaned text); the ones in `blocking` stop it.
"""

import os
import threading
from dataclasses import dataclass, field

from llm_guard import scan_output, scan_prompt
from llm_guard.vault import Vault


@dataclass
class GuardResult:
    text: str
    blocked: bool
    failed: list[str] = field(default_factory=list)  # scanners that flagged the text
    scores: dict[str, float] = field(default_factory=dict)


class Guard:
    def __init__(
        self, input_scanners, output_scanners, *, vault: Vault | None = None, blocking_input=(), blocking_output=()
    ):
        self.input_scanners = input_scanners
        self.output_scanners = output_scanners
        self.vault = vault
        self.blocking_input = set(blocking_input)
        self.blocking_output = set(blocking_output)
        # The vault maps placeholders to real values and is shared by Anonymize and
        # Deanonymize, so requests are serialized and the vault is emptied between them.
        # Otherwise one customer's data could be restored into another customer's reply.
        self.lock = threading.Lock()

    def reset_vault(self) -> None:
        if self.vault is not None:
            for item in list(self.vault.get()):
                self.vault.remove(item)

    def check_input(self, prompt: str) -> GuardResult:
        text, valid, scores = scan_prompt(self.input_scanners, prompt)
        return self._result(text, valid, scores, self.blocking_input)

    def check_output(self, prompt: str, output: str) -> GuardResult:
        text, valid, scores = scan_output(self.output_scanners, prompt, output)
        return self._result(text, valid, scores, self.blocking_output)

    @staticmethod
    def _result(text, valid, scores, blocking) -> GuardResult:
        failed = [name for name, ok in valid.items() if not ok]
        return GuardResult(text, any(name in blocking for name in failed), failed, scores)


def build_default_guard(token_limit: int = 1000) -> Guard:
    """Real llm-guard scanners. The first call downloads the models (several GB)."""
    from llm_guard.input_scanners import Anonymize, PromptInjection, Secrets, TokenLimit
    from llm_guard.input_scanners.anonymize import DEFAULT_ENTITY_TYPES
    from llm_guard.input_scanners.anonymize_helpers.regex_patterns import DEFAULT_REGEX_PATTERNS
    from llm_guard.output_scanners import Deanonymize, Sensitive
    from llm_guard.util import configure_logger

    from .patterns import AR_ENTITY_TYPES, AR_PATTERNS

    # llm-guard logs to stdout at DEBUG by default; keep scanned text out of the logs
    configure_logger(log_level=os.environ.get("LLM_GUARD_LOG_LEVEL", "ERROR"))

    vault = Vault()
    return Guard(
        input_scanners=[
            TokenLimit(limit=token_limit),  # LLM10: cheap check first
            PromptInjection(),  # LLM01. English-only model: false positives on Spanish (see evals)
            Secrets(),  # LLM02: redacts credentials before they reach the provider
            Anonymize(
                vault,
                regex_patterns=DEFAULT_REGEX_PATTERNS + AR_PATTERNS,
                entity_types=DEFAULT_ENTITY_TYPES + AR_ENTITY_TYPES,
            ),  # LLM02
        ],
        output_scanners=[
            # Sensitive runs before Deanonymize: it redacts PII the model produced on its
            # own, then Deanonymize restores only this customer's own placeholders.
            Sensitive(redact=True),  # LLM02
            Deanonymize(vault),
        ],
        vault=vault,
        blocking_input={"TokenLimit", "PromptInjection"},
        blocking_output=set(),
    )
