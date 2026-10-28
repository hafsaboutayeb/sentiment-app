# Compte rendu - Semaine 6 : paquet installable

## 1. Pourquoi séparer le paquet du modèle ?

La roue contient le code Python (`sentiment_app`, `api` et `ui`), mais pas
les jeux de données ni le modèle entraîné. Le modèle est un artefact propre à
l'entraînement et à la version de scikit-learn qui l'a produit. La variable
`SENTIMENT_MODELE` permet donc de lui donner un chemin au déploiement, sans
embarquer de données ou de modèle volumineux dans la roue.

## 2. Comment le code trouve-t-il le modèle hors du dépôt ?

`sentiment_app.predict.chemin_modele()` utilise `SENTIMENT_MODELE` lorsqu'elle
est définie. Sinon, le projet cherche le fichier `models/sentiment.joblib`
relativement à sa racine. Une installation de la roue sans variable configurée
signale explicitement que le modèle manque ; elle n'invente pas de résultat.

## 3. Pourquoi épingler scikit-learn et ne plus modifier `sys.path` dans l'API ?

Le format Joblib sérialise des objets scikit-learn : relire un modèle avec une
version incompatible peut échouer. La dépendance du paquet et l'environnement
de CI limitent donc scikit-learn à la série 1.5, la même que celle utilisée
pour entraîner le modèle de démonstration. L'API importe directement
`sentiment_app.predict`, ce qui rend l'import identique depuis le dépôt et
depuis le paquet installé. `src/predict.py` reste uniquement comme couche de
compatibilité pour les anciens outils du TP2 et du TP4.

## 4. Contrôles de packaging

- `python -m build --wheel` construit `sentiment_app-0.6.0-py3-none-any.whl`.
- `sentiment --version` affiche `sentiment-app 0.6.0`.
- La CI installe la roue dans un environnement distinct du dépôt puis lance
  une prédiction avec `SENTIMENT_MODELE` pointant vers le modèle entraîné.
