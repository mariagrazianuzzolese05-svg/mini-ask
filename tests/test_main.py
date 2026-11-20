from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthz_risponde_ok() -> None:
    risposta = client.get("/healthz")
    assert risposta.status_code == 200
    assert risposta.json() == {"status": "ok"}


def test_ask_modalita_finta() -> None:
    risposta = client.post("/ask", json={"testo": "ciao"})
    assert risposta.status_code == 200
    assert risposta.json() == {
        "risposta": "Risposta finta a: ciao",
        "modalita": "finta",
    }

def test_ask_senza_testo_da_422() -> None:
    risposta = client.post("/ask", json={})
    assert risposta.status_code == 422    