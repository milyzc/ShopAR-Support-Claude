"""HTTP API. The only path to the model is chat(), which wraps it with the guard."""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field

from . import llm
from .guard import Guard, build_default_guard

app = FastAPI(title="ShopAR Support API")

BLOCKED_REPLY = "No puedo procesar ese mensaje. Si necesitás ayuda con un pedido, escribime de nuevo."


class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=20_000)


class ChatOut(BaseModel):
    reply: str
    blocked: bool
    engine: str | None = None
    input_flags: list[str] = []
    output_flags: list[str] = []


@lru_cache
def get_guard() -> Guard:
    return build_default_guard()


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/chat", response_model=ChatOut)
def chat(body: ChatIn, guard: Annotated[Guard, Depends(get_guard)]) -> ChatOut:
    with guard.lock:
        guard.reset_vault()
        checked_in = guard.check_input(body.message)
        if checked_in.blocked:
            # Never echo the original message back: it may contain what was just redacted
            return ChatOut(reply=BLOCKED_REPLY, blocked=True, input_flags=checked_in.failed)

        reply, engine = llm.complete(checked_in.text)
        checked_out = guard.check_output(checked_in.text, reply)
        guard.reset_vault()

    if checked_out.blocked:
        return ChatOut(
            reply=BLOCKED_REPLY,
            blocked=True,
            engine=engine,
            input_flags=checked_in.failed,
            output_flags=checked_out.failed,
        )
    return ChatOut(
        reply=checked_out.text,
        blocked=False,
        engine=engine,
        input_flags=checked_in.failed,
        output_flags=checked_out.failed,
    )
