import os

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="mini-ask")


class Domanda(BaseModel):
    testo: str


class Risposta(BaseModel):
    risposta: str
    modalita: str


def rispondi_finto(testo: str) -> str:
    return f"Risposta finta a: {testo}"


@app.get("/healthz")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask")
def ask(domanda: Domanda) -> Risposta:
    modalita = os.environ.get("MODALITA", "finta")
    return Risposta(risposta=rispondi_finto(domanda.testo), modalita=modalita)