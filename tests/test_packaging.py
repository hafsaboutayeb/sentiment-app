"""Contrôles du paquet et de la commande installable du TP6."""
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_version_et_commande(capsys):
    from sentiment_app import __version__
    from sentiment_app.cli import main

    assert __version__ == "0.6.0"
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])
    assert exc_info.value.code == 0
    assert capsys.readouterr().out.strip() == "sentiment-app 0.6.0"


def test_chemin_modele_par_defaut():
    from sentiment_app import predict

    assert predict.MODELE == ROOT / "models" / "sentiment.joblib"


def test_chemin_modele_configurable(monkeypatch):
    from sentiment_app.predict import chemin_modele

    target = ROOT / "modele-externe.joblib"
    monkeypatch.setenv("SENTIMENT_MODELE", str(target))
    assert chemin_modele() == target


def test_ancien_import_predit_le_meme_module():
    script = (
        "import predict; import sentiment_app.predict; "
        "assert predict is sentiment_app.predict"
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join([str(ROOT / "src"), str(ROOT)])
    subprocess.run([sys.executable, "-c", script], cwd=ROOT, env=env, check=True)


def test_api_n_insere_pas_de_chemin_python():
    source = (ROOT / "api" / "model.py").read_text(encoding="utf-8")
    assert "sys.path" not in source


def test_cli_predict_outputs_api_result(capsys, monkeypatch):
    from api import model
    from sentiment_app.cli import main

    class FauxClassifier:
        def predict(self, text):
            return {"label": "POSITIVE", "score": 0.777, "text": text[:100]}

    monkeypatch.setattr(model, "load_model", lambda: FauxClassifier())
    assert main(["predict", "Très", "bien"]) == 0
    assert capsys.readouterr().out.strip() == (
        '{"label": "POSITIVE", "score": 0.777, "text": "Très bien"}'
    )
