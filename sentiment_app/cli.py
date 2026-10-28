"""Interface en ligne de commande du paquet sentiment-app."""
import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Sequence

from sentiment_app import __version__


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sentiment", description="Application d'analyse de sentiments.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"sentiment-app {__version__}",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    predict = commands.add_parser("predict", help="analyser un avis")
    predict.add_argument("text", nargs="+", help="texte de l'avis")

    serve = commands.add_parser("serve", help="lancer l'API FastAPI")
    serve.add_argument("--host", default="127.0.0.1", help="adresse d'écoute (défaut : 127.0.0.1)")
    serve.add_argument("--port", type=int, default=8000, help="port d'écoute (défaut : 8000)")

    commands.add_parser("ui", help="lancer l'interface Streamlit")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)

    if args.command == "predict":
        from api.model import load_model

        text = " ".join(args.text)
        try:
            result = load_model().predict(text)
        except FileNotFoundError as error:
            print(error, file=sys.stderr)
            return 1
        except ValueError as error:
            print(f"Texte refusé : {error}", file=sys.stderr)
            return 2
        print(json.dumps(result, ensure_ascii=False))
        return 0

    if args.command == "serve":
        import uvicorn

        uvicorn.run("api.main:app", host=args.host, port=args.port)
        return 0

    if args.command == "ui":
        if importlib.util.find_spec("streamlit") is None:
            print("Streamlit absent : installez sentiment-app avec l'extra [ui].", file=sys.stderr)
            return 1
        app_path = Path(__file__).resolve().parents[1] / "ui" / "app.py"
        return subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(app_path)],
            check=False,
        ).returncode

    return 2
