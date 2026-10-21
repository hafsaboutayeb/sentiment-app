import sys
from pathlib import Path

import streamlit as st

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))
from ui import client  # noqa: E402

st.set_page_config(page_title="Analyse de sentiments", layout="centered")
st.caption("API prête · Modèle entraîné en TP2 · interface de démonstration · fil rouge du cours")
st.title("Analyse de sentiments d'avis clients")

session = client.creer_session()
etat_sante = client.sante(session)
if not etat_sante.ok:
    st.error(client.INJOIGNABLE)
    st.stop()

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
            st.metric(label="Avis positif", value=f"{int(resultat.score * 100)} %")
        elif resultat.label == "NEGATIVE":
            st.metric(label="Avis négatif", value=f"{int(resultat.score * 100)} %")
        else:
            st.metric(label="Je ne sais pas", value=f"{int(resultat.score * 100)} %")
            st.info("seuil d'abstention appliqué")