import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
CHIAVE = {"X-API-Key": "chiave-di-test"}


@pytest.fixture(autouse=True)
def imposta_chiave(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_KEY", "chiave-di-test")


def test_healthz_risponde_ok() -> None:
    risposta = client.get("/healthz")
    assert risposta.status_code == 200
    assert risposta.json() == {"status": "ko"}


def test_ask_modalita_finta() -> None:
    risposta = client.post("/ask", json={"testo": "ciao"}, headers=CHIAVE)
    assert risposta.status_code == 200
    assert risposta.json() == {
        "risposta": "Risposta finta a: ciao",
        "modalita": "finta",
    }


def test_ask_senza_testo_da_422() -> None:
    risposta = client.post("/ask", json={}, headers=CHIAVE)
    assert risposta.status_code == 422


@pytest.mark.parametrize(
    ("lunghezza", "codice"),
    [(0, 422), (1, 200), (500, 200), (501, 422)],
)
def test_ask_limiti_di_lunghezza(lunghezza: int, codice: int) -> None:
    risposta = client.post("/ask", json={"testo": "a" * lunghezza}, headers=CHIAVE)
    assert risposta.status_code == codice


def test_ask_senza_chiave_da_401() -> None:
    risposta = client.post("/ask", json={"testo": "ciao"})
    assert risposta.status_code == 401
    assert risposta.json() == {"detail": "Chiave API mancante o sbagliata"}


def test_ask_chiave_sbagliata_da_401() -> None:
    risposta = client.post(
        "/ask", json={"testo": "ciao"}, headers={"X-API-Key": "sbagliata"}
    )
    assert risposta.status_code == 401


def test_ask_senza_api_key_sul_server_da_401(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("API_KEY")
    risposta = client.post("/ask", json={"testo": "ciao"}, headers=CHIAVE)
    assert risposta.status_code == 401
