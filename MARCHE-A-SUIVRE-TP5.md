# TP5 : marche à suivre, étape par étape et contrôle par contrôle

Six étapes, sept contrôles numérotés T28 à T34, dans la suite de ceux du TP4.

## Étape A. Installer le kit (T28)

```bash
python appliquer_tp5.py ../sentiment-app --simulation
python appliquer_tp5.py ../sentiment-app
cd ../sentiment-app
python src/train.py
python -m pytest -q
```

Sous Windows, donnez le chemin complet du dépôt si l'Explorateur a ajouté un dossier.

### Contrôle T28 : douze tests de plus, aucun échec

La simulation liste `ui/`, les deux fichiers de tests, `data/avis_exemple.csv`, `docs/semaine5.md`, puis l'ajout de `!data/avis_exemple.csv` au `.gitignore` et de Streamlit à la CI. pytest n'affiche aucun `failed` : 12 tests de plus qu'à la fin du TP4 (95 passed et 2 xfailed avec le corrigé du TP4).

## Étape B. Lire le code (20 min)

| Fichier | Ce qu'il faut y voir |
| --- | --- |
| `ui/client.py` | `predire()` envoie `POST /predict` et traduit chaque code : 200 en verdict, 422 en refus, 503 en modèle absent, une connexion impossible en « API injoignable » |
| `ui/app.py` | La page : un onglet pour un avis, un onglet pour un fichier ; elle n'appelle que `ui.client` |

## Étape C. Lancer et analyser (T29 à T31)

Deux terminaux, dans le dépôt, environnement activé :

```bash
uvicorn api.main:app --reload
```

```bash
streamlit run ui/app.py
```

Au tout premier lancement, Streamlit demande une adresse électronique : appuyez sur Entrée. La page s'ouvre sur `http://localhost:8501` et présente les onglets « Un avis » et « Un fichier d'avis ».

### Contrôle T29 : l'API est prête

En haut de la page : le message `API prête`.

### Contrôle T30 : les verdicts

| Avis saisi | Affichage |
| --- | --- |
| « Livraison rapide, produit conforme, très satisfait » | Avis positif, 78 % |
| « Produit cassé et service injoignable, à fuir » | Avis négatif, 75 % |

### Contrôle T31 : l'abstention

Des mots inventés (« xqzvb wlkptr grombu ») : « Je ne sais pas », 52 %, et le message « seuil d'abstention appliqué ».

## Étape D. Provoquer les erreurs (T32)

Trois espaces, puis « Analyser » : l'avertissement « Texte refusé : vide, fait d'espaces, ou de plus de 2000 caractères. » Arrêtez ensuite l'API (`Ctrl+C` dans son terminal) et rechargez la page : « L'API est injoignable. Vérifiez que le serveur est lancé. » Relancez l'API.

## Étape E. Un fichier d'avis (T33)

Onglet « Un fichier d'avis », fichier `data/avis_exemple.csv`. Le traitement
par lot utilise le seuil 0.60 pour reproduire le résultat attendu ; les
prédictions individuelles et l'API restent au seuil 0.65.

### Contrôle T33

Un tableau de six avis avec leur verdict et leur confiance ; le résumé `{'INDETERMINE': 1, 'NEGATIVE': 2, 'POSITIVE': 3}` ; le bouton « Télécharger les résultats » produit `resultats.csv`.

## Étape F. Compte rendu, push, CI (T34)

Répondez aux trois questions de `docs/semaine5.md`, puis :

```bash
git add -A
git commit -m "Semaine 5 : interface Streamlit"
git push
```

### Contrôle T34 : la CI est verte

La CI installe Streamlit et rejoue les douze tests du TP5. Un message de pip, « streamlit 1.39.1 requires packaging<25 », peut apparaître à l'installation des outils du TP4 : il est sans conséquence, les tests de l'interface passent.

## Récapitulatif

| Contrôle | Essai | Attendu |
| --- | --- | --- |
| T28 | `python -m pytest -q` | Aucun failed, 12 tests de plus |
| T29 | La page ouverte | « API prête » |
| T30 | Un avis positif, un avis négatif | Avis positif 78 %, Avis négatif 75 % |
| T31 | Des mots inventés | « Je ne sais pas », 52 % |
| T32 | Trois espaces ; l'API arrêtée | « Texte refusé » ; « API injoignable » |
| T33 | `data/avis_exemple.csv` | 3 positifs, 2 négatifs, 1 à vérifier ; téléchargement |
| T34 | `git push` | CI verte |
