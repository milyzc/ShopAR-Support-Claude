"""Model client: local Ollama, with a deterministic mock when it is not available."""

import os

import httpx

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")

SYSTEM_PROMPT = (
    "Sos el asistente de soporte de ShopAR (tienda online argentina). "
    "Respondé breve, en español rioplatense. Solo ayudás con pedidos, envíos y reclamos."
)


def mock_reply(prompt: str) -> str:
    """Naive fake model, predictable for class. It repeats placeholders it receives."""
    p = prompt.lower()
    if "pago" in p or "tarjeta" in p:
        # Phishing link the model "learned" somewhere: no output scanner catches it yet
        return "Para confirmar el pago, verificá tu tarjeta en http://shopar-verificacion.example/login"
    if "pedido" in p:
        names = [w for w in prompt.split() if w.startswith("[REDACTED_PERSON")]
        hello = f"Hola {' '.join(names)}! " if names else ""
        return hello + "Tu pedido #1001 está en camino y llega el jueves."
    return "Hola, soy el asistente de ShopAR. ¿En qué te ayudo con tu pedido?"


def complete(prompt: str) -> tuple[str, str]:
    """Return (reply, engine)."""
    if os.environ.get("FORCE_MOCK") != "1":
        try:
            r = httpx.post(
                f"{OLLAMA_URL}/api/chat",
                timeout=90,
                json={
                    "model": MODEL,
                    "stream": False,
                    "options": {"temperature": 0.2},
                    "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
                },
            )
            r.raise_for_status()
            return r.json()["message"]["content"], f"ollama:{MODEL}"
        except httpx.HTTPError:
            pass
    return mock_reply(prompt), "mock"
