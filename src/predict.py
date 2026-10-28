#!/usr/bin/env python
"""Compatibilité avec les imports historiques du TP2 et du TP4."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sentiment_app import predict as _module  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(_module.main())

sys.modules[__name__] = _module
