# Captures et preuves du journal TP1-TP6

## Synthèses des contrôles

Les fichiers `reprise-tp*.png` sont des images de synthèse produites à partir
des sorties de commandes réellement relancées sur le poste partagé du binôme
le 28 octobre 2026. Elles ne sont pas des photos du terminal et ne prouvent
pas les états intermédiaires des séances.

## Captures réelles du navigateur

- `tp3-fastapi-docs-2026-10-28.png` : documentation Swagger de l'API FastAPI.
- `tp5-streamlit-ready-2026-10-28.png` : page Streamlit avec l'API prête.
- `tp5-streamlit-avis-positif-2026-10-28.png` et
  `tp5-streamlit-avis-negatif-2026-10-28.png` : prédictions affichées.
- `tp5-streamlit-abstention-2026-10-28.png` : abstention sur un texte inventé.
- `tp5-streamlit-texte-vide-2026-10-28.png` : refus d'un avis composé d'espaces.
- `tp5-streamlit-api-indisponible-2026-10-28.png` : message après arrêt de l'API.
- `tp5-streamlit-resultats-csv-2026-10-28.png` et
  `tp5-streamlit-resultats-csv-suite-2026-10-28.png` : première partie puis fin
  du tableau des six avis.
- `tp5-streamlit-resultats-resume-2026-10-28.png` : résumé des prédictions et
  bouton de téléchargement.

Le CSV `data/avis_exemple.csv` a été téléversé dans la page. L'interface affiche
le tableau, le résumé `{'INDETERMINE': 1, 'NEGATIVE': 2, 'POSITIVE': 3}` et le
bouton qui télécharge `resultats.csv`.
Le seuil d'une prédiction individuelle et de l'API est 0.65 ; le traitement
par lot CSV utilise 0.60 pour obtenir le résumé attendu du fichier d'exemple.
Les images `reprise-tp4` et `reprise-tp5` ont été actualisées après la dernière
validation (108 tests réussis, 1 `xfailed`, couverture API à 100 %).

Les captures originales des séances et des étapes intermédiaires ne figuraient
pas dans le dépôt. Elles ne peuvent pas être recréées à partir de l'état final.
Les membres ont indiqué avoir travaillé ensemble sur le même ordinateur ; le
diagnostic actuel montre les deux auteurs Git, mais le nom Git global configuré
sur ce poste est celui de Hafsa. Aucune session Windows distincte d'Aya n'a été
vérifiée. Ne présentez pas une réexécution comme une capture historique.

Avant de partager une capture, masquez les mots de passe, jetons et fichiers
`.env`.
