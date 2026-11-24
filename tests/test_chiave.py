import pytest
from fastapi import HTTPException

from app.main import controlla_chiave


def test_chiave_giusta_passa(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_KEY", "segreta")
    controlla_chiave("segreta")


def test_chiave_sbagliata_da_401(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_KEY", "segreta")
    with pytest.raises(HTTPException) as errore:
        controlla_chiave("sbagliata")
    assert errore.value.status_code == 401
    assert errore.value.detail == "Chiave API mancante o sbagliata"


def test_chiave_mancante_da_401(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_KEY", "segreta")
    with pytest.raises(HTTPException) as errore:
        controlla_chiave(None)
    assert errore.value.status_code == 401
    assert errore.value.detail == "Chiave API mancante o sbagliata"


def test_server_senza_api_key_da_401(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("API_KEY", raising=False)
    with pytest.raises(HTTPException) as errore:
        controlla_chiave(None)
    assert errore.value.status_code == 401
    assert errore.value.detail == "Chiave API mancante o sbagliata"
