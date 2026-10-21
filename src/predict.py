#!/usr/bin/env python
import sys
from functools import lru_cache
from pathlib import Path

import joblib

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"

@lru_cache(maxsize=1)
def charger_modele():
    if not MODELE.exists():
        raise FileNotFoundError("models/sentiment.joblib absent : lancez python src/train.py")
    return joblib.load(MODELE)

def predict(texte: str) -> dict:
    if not isinstance(texte, str) or not texte.strip():
        raise ValueError("texte vide")
    pipeline = charger_modele()
    probas = pipeline.predict_proba([texte])[0]
    score = float(max(probas))
    if score < 0.65:
        etiquette = "indetermine"
    else:
        etiquette = "positive" if probas[1] > 0.5 else "negative"
    return {"label": etiquette, "score": round(score, 4)}

def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    resultat = predict(" ".join(sys.argv[1:]))
    print(f"{resultat['label']} (confiance {resultat['score']:.0%})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())