# Semaine 4 : tests approfondis et qualité

## 1. Couverture et intégration

Les tests d'intégration vérifient les erreurs de démarrage, l'indisponibilité
du modèle, les entrées invalides et les erreurs internes. Une entrée invalide
est une erreur du client (HTTP 422) ; une panne inattendue du modèle est une
erreur du serveur (HTTP 500).

Lors de la reprise du 28 octobre 2026, la couverture de l'API est de 100 %,
au-dessus du seuil demandé de 95 %. La suite complète compte 108 tests réussis
et un test `xfailed` attendu.

## 2. Défauts trouvés

| Symptôme | Outil ou test | Correction |
| --- | --- | --- |
| Noms de variables ambigus | Ruff, règle E741 | Noms explicites dans les tests et `ui/helpers.py`. |
| `zip()` sans contrôle de longueur | Ruff, règle B905 | Ajout de `strict=True` dans `src/evaluate.py`. |
| Exceptions non chaînées | Ruff, règle B904 | Chaînage explicite avec `from e` ou `from None` dans `api/main.py`. |
| Un texte constitué d'espaces n'était pas validé au niveau du schéma | Tests de limites et Hypothesis | Validateur Pydantic qui rejette les chaînes vides après suppression des espaces. |
| Une erreur `ValueError` inattendue était confondue avec une erreur client | Tests d'intégration | Les erreurs internes suivent le traitement générique HTTP 500. |

Les tests de propriétés couvrent les limites de longueur, les chaînes vides ou
blanches et la forme des réponses. Les contrôles `tests/test_limites.py` ont
été relancés trois fois : 10 tests réussis à chaque exécution.

## 3. Seuil d'abstention

Le seuil retenu est 0.65. Sur les 58 avis du jeu d'évaluation, 41 sont classés
et 17 (29 %) sont orientés vers un humain. L'exactitude des avis classés est
de 0.976, avec une erreur. Un texte inventé (« xqzvb wlkptr grombu ») est
renvoyé comme `INDETERMINE` avec un score de 0.5162.

L'abstention évite de forcer une classe lorsque le modèle est trop incertain.
Le seuil de prédiction par lot CSV utilisé au TP5 est distinct (0.60) afin de
reproduire les résultats attendus pour le fichier d'exemple ; le seuil API et
la prédiction individuelle restent à 0.65.

## 4. Jeu d'or

Sur 20 avis, le bilan relancé est de 6 prédictions correctes, 13 abstentions
et 1 erreur franche déclarée. Le test de l'erreur connue est conservé comme
`xfailed` attendu : il rend visible une limite du modèle sans masquer le
résultat.

## 5. Outils statiques et validation

Ruff et mypy passent lors de la reprise. La validation finale est :

```text
ruff check . : All checks passed!
mypy api : Success: no issues found in 4 source files
pytest : 108 passed, 1 xfailed
Couverture API : 100 %
```

Le contrôle de couverture est exécuté avec `--cov-fail-under=95`. Le test
`xfailed` est une erreur connue et attendue, pas un échec non traité.
