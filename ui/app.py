import sys
from pathlib import Path

import pandas as pd
import streamlit as st

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))
from ui import client  # noqa: E402
from ui.helpers import analyser_fichier, charger_predicteur  # noqa: E402

st.set_page_config(page_title="Analyse de sentiments", layout="centered")
st.caption("API prête · Modèle entraîné en TP2 · interface de démonstration · fil rouge du cours")
st.title("Analyse de sentiments d'avis clients")

session = client.creer_session()
etat_sante = client.sante(session)
if not etat_sante.ok:
    st.error(client.INJOIGNABLE)
    st.stop()

onglet_avis, onglet_fichier = st.tabs(["Un avis", "Un fichier d'avis"])

with onglet_avis:
    texte = st.text_area("Saisissez un avis :", height=150)

    if st.button("Analyser"):
        resultat = client.predire(session, texte)

        if not resultat.ok:
            if resultat.message == client.REFUS:
                st.warning(resultat.message)
            else:
                st.error(resultat.message)
        else:
            if resultat.label == "POSITIVE":
                st.metric(label="Avis positif", value=f"{round(resultat.score * 100)} %")
            elif resultat.label == "NEGATIVE":
                st.metric(label="Avis négatif", value=f"{round(resultat.score * 100)} %")
            else:
                st.metric(label="Je ne sais pas", value=f"{round(resultat.score * 100)} %")
                st.info("seuil d'abstention appliqué")

with onglet_fichier:
    fichier = st.file_uploader("Choisir un fichier CSV", type=["csv"])
    if fichier is not None:
        try:
            avis = pd.read_csv(fichier)
        except pd.errors.EmptyDataError:
            st.error("Le fichier CSV est vide ou ne contient pas d'en-tête.")
        except pd.errors.ParserError as erreur:
            st.error(f"Le fichier CSV est invalide : {erreur}")
        except UnicodeDecodeError:
            st.error("Le fichier CSV doit être encodé en UTF-8.")
        else:
            try:
                resultats, resume = analyser_fichier(avis, charger_predicteur())
            except KeyError as erreur:
                st.error(f"Colonne requise absente : {erreur}")
            except ValueError as erreur:
                st.error(f"Impossible d'analyser le fichier : {erreur}")
            else:
                st.dataframe(resultats, use_container_width=True)
                st.write("Résumé des prédictions")
                st.json(resume)
                st.download_button(
                    "Télécharger les résultats",
                    data=resultats.to_csv(index=False).encode("utf-8-sig"),
                    file_name="resultats.csv",
                    mime="text/csv",
                )