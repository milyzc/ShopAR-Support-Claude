def main() -> None:
    import os

    import uvicorn

    # Local only: this is a training project
    uvicorn.run("shopar_support.api:app", host="127.0.0.1", port=int(os.environ.get("PORT", "8000")))
