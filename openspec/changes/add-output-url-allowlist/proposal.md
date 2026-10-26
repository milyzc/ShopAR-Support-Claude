# Proposal

## Why

The model can return links that do not belong to ShopAR, for example a phishing page asking the customer to "verify the card" (OWASP LLM05). Nothing checks URLs in replies today: the `out-phishing-url` case in `evals/attacks.yaml` passes through. llm-guard's `MaliciousURLs` scanner cannot be used because the model it depends on was removed from Hugging Face.

## What Changes

- Replies that contain a URL outside an allowlist of ShopAR domains are blocked.
- The allowlist is configurable without code changes.
- The attack corpus gains a blocked phishing link and an allowed official link.

## Capabilities

### New Capabilities

### Modified Capabilities
- `guardrails`: adds a requirement that replies may only link to allowed domains.

## Impact

- Output guard pipeline (new output scanner, blocking).
- Configuration: new environment variable for the allowed domains.
- `evals/attacks.yaml`: new cases; `out-phishing-url` becomes a pass.
