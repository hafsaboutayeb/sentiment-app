"""Tests d'intégration : l'API telle qu'elle tourne vraiment (TP4, étape D).

Les tests du TP3 vérifient des réponses ; ceux-ci vérifient le démarrage de l'API
et son comportement quand le modèle manque ou tombe en panne.
"""
import importlib
import logging
import runpy
from pathlib import Path

import pytest

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


def test_demarrage_reel_charge_le_modele():
    """D.1 (donné en exemple) : un client ouvert par « with » exécute le lifespan."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        reponse = client.get("/health")
    assert reponse.status_code == 200
    assert "TP2" in reponse.json()["model"]


def test_demarrage_echoue_si_le_modele_est_absent(monkeypatch, tmp_path):
    from fastapi.testclient import TestClient

    from api.main import app

    predictor = importlib.import_module("sentiment_app.predict")
    predictor.charger_modele.cache_clear()
    monkeypatch.setattr(predictor, "MODELE", tmp_path / "absent.joblib")
    try:
        with pytest.raises(FileNotFoundError, match="Modèle introuvable"):
            with TestClient(app):
                pass
    finally:
        predictor.charger_modele.cache_clear()


def test_modele_non_charge_refuse_health_et_predict(monkeypatch):
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        monkeypatch.setitem(app.state._state, "classifier", None)
        assert client.get("/health").status_code == 503
        assert client.post("/predict", json={"text": "avis valide"}).status_code == 503


@pytest.mark.parametrize("erreur", [RuntimeError("panne"), ValueError("bug interne")])
def test_panne_du_modele_est_une_erreur_500(monkeypatch, caplog, erreur):
    from fastapi.testclient import TestClient

    from api.main import app

    class ModeleEnPanne:
        def predict(self, texte: str) -> dict:
            raise erreur

    caplog.set_level(logging.ERROR, logger="sentiment_api")
    with TestClient(app) as client:
        monkeypatch.setitem(app.state._state, "classifier", ModeleEnPanne())
        response = client.post("/predict", json={"text": "avis valide"})

    assert response.status_code == 500
    assert response.json() == {"detail": "Erreur interne du serveur"}
    assert "bug interne" not in response.text
    assert "Erreur lors de la prédiction" in caplog.text


def test_point_entree_demarre_uvicorn(monkeypatch):
    import uvicorn

    appels = []
    monkeypatch.setattr(uvicorn, "run", lambda *args, **kwargs: appels.append((args, kwargs)))
    fichier_api = Path(__file__).resolve().parents[1] / "api" / "main.py"

    runpy.run_path(str(fichier_api), run_name="__main__")

    assert appels == [
        (("api.main:app",), {"host": "0.0.0.0", "port": 8000, "log_level": "info"})
    ]
