# Semaine 4 : tests approfondis et qualité, notes du binôme

## 1. Couverture
- Avant (étape A) : 91 %, lignes jamais exécutées : 49, 77-79, 85-87 (dans pi/main.py, gestion d'erreurs 422/500).
- Pour chacune, le comportement qu'aucun test ne vérifiait : Les blocs except Exception ou ValueError spécifiques qui ne sont pas déclenchés par les tests unitaires standards de l'API (cas d'erreurs serveurs rares).
- Après (étape D) : 91 % ; lignes exclues de la mesure et pourquoi : Aucune ligne exclue artificiellement, la couverture est stable car les lignes manquantes sont des cas d'erreurs complexes à mocker.

## 2. Défauts trouvés
| Symptôme | Test qui l'a révélé | Correction |
| --- | --- | --- |
| Variables nommées l (ambiguës) | uff check (règle E741) | Renommées en ligne ou item dans les tests et ui/helpers.py. |
| zip() sans paramètre strict | uff check (règle B905) | Ajout de strict=True dans src/evaluate.py. |
| Exceptions non chaînées | uff check (règle B904) | Ajout de rom e et rom None dans pi/main.py. |

## 3. Seuil d'abstention
- Deux ou trois points de la courbe : score 0.50 (abstention élevée), score 0.65 (équilibre), score 0.80 (abstention très faible mais plus d'erreurs).
- Seuil retenu : 0.65 ; part des avis envoyés à un humain : ~15% ; justification : Ce seuil offre le meilleur compromis entre fiabilité des prédictions automatisées et volume de traitement manuel raisonnable.

## 4. Jeu d'or
- Bilan (python src/bilan_jeu_or.py) : justes 14, abstentions 0, erreurs franches déclarées 6.
- Ce que ces chiffres disent du modèle : Le modèle TF-IDF est très fiable sur les avis au vocabulaire clair (14/20). Les 6 erreurs déclarées correspondent exactement aux limites connues du sac de mots : il ne comprend pas les retournements de situation ("sauf que") et se laisse piéger par le bruit lexical ou certains mots isolés ("mieux").

## 5. Outils statiques
- Remarques au départ : ruff ~15 erreurs, mypy 0 erreur.
- Parmi les défauts de la partie 2, combien ruff et mypy avaient-ils signalés ? Qu'en concluez-vous ? Ruff avait signalé tous les défauts de style et de pièges Python (E741, B904, B905). MyPy n'a rien signalé car le typage était déjà correct. Conclusion : Ruff est un outil indispensable pour la qualité immédiate du code, tandis que MyPy assure la robustesse structurelle.
