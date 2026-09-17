from inventaire import MOUVEMENT_SORTIE,calculer_cout_reapprovisionnement ,calculer_valeur_stock, recuperer_article_en_alerte, enregistrer_mouvement_stock


def test_calculer_valeur_stock_standard():
    articles = [
        {"ref": "A1", "q": 10, "pu": 5.0, "seuil": 2},
        {"ref": "A2", "q": 2, "pu": 10.0, "seuil": 5},
    ]
    assert calculer_valeur_stock(articles) == 70.0

def test_recuperer_article_en_alerte():
    articles = [
        {"ref": "A1", "q": 1, "seuil": 2},
        {"ref": "A2", "q": 2, "seuil": 2},
        {"ref": "A3", "q": 5, "seuil": 2},
    ]
    assert recuperer_article_en_alerte(articles) == ["A1"]

def test_enregistrer_mouvement_stock():
    articles = [{"ref": "A1", "q": 10, "seuil": 2}]
    assert enregistrer_mouvement_stock(articles[0], 5) == True
    assert enregistrer_mouvement_stock(articles[0], -2) == False
    assert enregistrer_mouvement_stock(articles[0], 15, MOUVEMENT_SORTIE, forcer=True) == True

def test_calculer_cout_reapprovisionnement():
    art_ok = {"q": 10, "seuil": 5, "pu": 2.0}
    assert calculer_cout_reapprovisionnement(art_ok) == 0
    art_alerte = {"q": 2, "seuil": 5, "pu": 2.0}
    assert calculer_cout_reapprovisionnement(art_alerte) == 26.0
    art_remise = {"q": 50, "seuil": 100, "pu": 10.0}
    assert calculer_cout_reapprovisionnement(art_remise) == 2250.0
