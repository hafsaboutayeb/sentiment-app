import httpx

BASE_URL = "http://127.0.0.1:8000"
REFUS = "Texte refusé : vide, fait d'espaces, ou de plus de 2000 caractères."
INJOIGNABLE = "L'API est injoignable. Vérifiez que le serveur est lancé."
SANS_MODELE = "Le modèle n'est pas chargé côté serveur."

def creer_session():
    return httpx.Client(base_url=BASE_URL, timeout=5.0)

def sante(session):
    try:
        r = session.get("/health")
        class Reponse:
            ok = r.status_code == 200
            message = r.json().get("model", "") if r.status_code == 200 else ""
        return Reponse()
    except httpx.RequestError:
        class Reponse:
            ok = False
            message = ""
        return Reponse()

def predire(session, texte):
    if not texte or not str(texte).strip() or len(str(texte)) > 2000:
        class Reponse:
            ok = False
            label = ""
            score = 0.0
            message = REFUS
        return Reponse()
    try:
        r = session.post("/predict", json={"text": texte})
        if r.status_code in (500, 503):
            class Reponse:
                ok = False
                label = ""
                score = 0.0
                message = SANS_MODELE
            return Reponse()
        class Reponse:
            ok = r.status_code == 200
            label = r.json().get("label", "") if r.status_code == 200 else ""
            score = r.json().get("score", 0.0) if r.status_code == 200 else 0.0
            message = "" if r.status_code == 200 else f"Erreur {r.status_code}"
        return Reponse()
    except httpx.RequestError:
        class Reponse:
            ok = False
            label = ""
            score = 0.0
            message = INJOIGNABLE
        return Reponse()

def predire_lot(session, textes):
    return [predire(session, t) for t in textes]

def resumer(reponses):
    compte = {"POSITIVE": 0, "NEGATIVE": 0, "REFUS OU ERREUR": 0}
    for r in reponses:
        if not r.ok:
            compte["REFUS OU ERREUR"] += 1
        elif r.label in compte:
            compte[r.label] += 1
        else:
            compte["REFUS OU ERREUR"] += 1
    return compte
