import os

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from fastapi.responses import RedirectResponse

app = FastAPI(title="mini-ask")


class Domanda(BaseModel):
    testo: str = Field(min_length=1, max_length=500)


class Risposta(BaseModel):
    risposta: str
    modalita: str


def rispondi_finto(testo: str) -> str:
    return f"Risposta finta a: {testo}"


def controlla_chiave(chiave: str | None) -> None:
    attesa = os.environ.get("API_KEY")
    if attesa is None or chiave != attesa:
        raise HTTPException(status_code=401, detail="Chiave API mancante o sbagliata")

@app.get("/", include_in_schema=False)
def home() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get("/healthz")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/ask",
    responses={
        400: {"description": "Corpo della richiesta non leggibile"},
        401: {"description": "Chiave API mancante o sbagliata"},
    },
)
def ask(domanda: Domanda, x_api_key: str | None = Header(default=None)) -> Risposta:
    controlla_chiave(x_api_key)
    modalita = os.environ.get("MODALITA", "finta")
    return Risposta(risposta=rispondi_finto(domanda.testo), modalita=modalita)
