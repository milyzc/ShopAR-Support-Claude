# Design

## Context

Output scanners follow llm-guard's protocol `scan(prompt, output) -> (text, is_valid, risk)` and are listed in `build_default_guard()`. Only scanners named in `blocking_output` stop a reply.

## Goals / Non-Goals

**Goals:**
- Deterministic check with no model download.

**Non-Goals:**
- Judging whether an unknown site is malicious (reputation, ML classification).
- Rewriting or removing the link instead of blocking.

## Decisions

- **Allowlist instead of a blocklist or classifier.** The support assistant only needs to link to ShopAR. An allowlist fails closed, while a blocklist misses every new phishing domain. `MaliciousURLs` was the classifier alternative, but its model is no longer available.
- **Own scanner class (`AllowedDomains`) in `src/shopar_support/scanners.py`.** It follows the same protocol so it plugs into `scan_output` like any llm-guard scanner.
- **Host matching on the parsed URL**, not substring matching: `shopar.example.evil.example` must fail even though it contains `shopar.example`.
- **Configuration through `ALLOWED_DOMAINS`** (comma-separated), defaulting to `shopar.example`.

## Risks / Trade-offs

- [URLs without a scheme ("shopar-verificacion.example/login") are missed by a scheme-based regex] → also match bare domains with a path, and cover it with a test case.
- [False positives when the model cites a legitimate external site] → acceptable for a support bot; the domain can be added to the allowlist.
