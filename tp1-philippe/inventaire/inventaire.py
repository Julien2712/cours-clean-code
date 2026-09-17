import datetime
import json
import math

TVA = 0.2
FACTEUR_DE_REAPPROVISIONNEMENT = 3
REMISE_REAPPROVISIONNEMENT = 0.1
QUANTITE_REAPPROVISIONNEMENT = 100
JOURS_PERIODE_VENTES = 30
MOUVEMENT_SORTIE = "out"
MOUVEMENT_ENTREE = "in"
CATEGORIES_CONNUES = ("outil", "consommable", "piece")

JOURNAL = []
DERNIER = 0


def calculer_valeur_stock(articles):
    valeur_stock = 0
    for article in articles:
        if article["q"] > 0:
            valeur_stock += article["q"] * article["pu"]
    return round(valeur_stock, 2)


def recuperer_article_en_alerte(articles):
    reference_alerte = []
    for article in articles:
        if article["q"] < article["seuil"]:
            reference_alerte.append(article["ref"])
    return reference_alerte


def enregistrer_mouvement_stock(article, quantite, type_mouvement=MOUVEMENT_SORTIE, forcer=False):
    global DERNIER

    if quantite <= 0:
        return False

    if type_mouvement == MOUVEMENT_SORTIE:
        article["q"] -= quantite
        if article["q"] < 0 and not forcer:
            return False
    elif type_mouvement == MOUVEMENT_ENTREE:
        article["q"] += quantite
    else:
        return False

    DERNIER += 1
    JOURNAL.append(
        {
            "id": DERNIER,
            "ref": article["ref"],
            "q": quantite,
            "t": type_mouvement,
        }
    )
    return True


def calculer_cout_reapprovisionnement(article):
    if article["q"] >= article["seuil"]:
        return 0

    quantite_a_commander = article["seuil"] * FACTEUR_DE_REAPPROVISIONNEMENT - article["q"]
    cout_total = quantite_a_commander * article["pu"]

    if quantite_a_commander > QUANTITE_REAPPROVISIONNEMENT:
        cout_total -= cout_total * REMISE_REAPPROVISIONNEMENT

    return round(cout_total, 2)


def trier_articles_par_valeur(articles):
    return sorted(
        articles,
        key=lambda article: article["q"] * article["pu"],
        reverse=True,
    )


def calculer_rotation_stock(article, ventes_periode):
    try:
        return math.floor(article["q"] / (ventes_periode / JOURS_PERIODE_VENTES))
    except ZeroDivisionError:
        return 0


def regrouper_valeur_par_categorie(articles):
    valeurs = {}
    for article in articles:
        categorie = article["cat"] if article["cat"] in CATEGORIES_CONNUES else "autre"
        valeurs[categorie] = valeurs.get(categorie, 0) + article["q"] * article["pu"]
    return {categorie: round(valeur, 2) for categorie, valeur in valeurs.items()}


def filtrer_articles_valides(articles, cat=None, seuil_min=None):
    return [
        article
        for article in articles
        if (cat is None or article["cat"] == cat)
        and (seuil_min is None or article["q"] >= seuil_min)
        and article["q"] > 0
        and article["pu"] > 0
    ]


def calculer_synthese_stock(articles):
    valeur_totale = round(sum(article["q"] * article["pu"] for article in articles), 2)
    alertes = [article["ref"] for article in articles if article["q"] < article["seuil"]]
    return {
        "valeur": valeur_totale,
        "nb": len(articles),
        "alertes": alertes,
        "ttc": round(valeur_totale * (1 + TVA), 2),
    }


def afficher_alertes(alertes):
    for reference in alertes:
        print(f"ALERTE {reference}")


def rapport(articles, cat=None, seuil_min=None, verbose=True):
    articles_valides = filtrer_articles_valides(articles, cat, seuil_min)
    synthese = calculer_synthese_stock(articles_valides)
    synthese["date"] = str(datetime.datetime.now())
    if verbose:
        afficher_alertes(synthese["alertes"])
    return synthese


def export_json(res, chemin="/tmp/inv.json", hist=None):
    if hist is None:
        hist = []
    hist.append(res)
    with open(chemin, "w", encoding="utf-8") as fichier:
        fichier.write(json.dumps(hist))
    return hist