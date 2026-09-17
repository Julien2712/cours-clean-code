from inventaire import calculer_valeur_stock


def test_calculer_valeur_stock_standard():
    articles = [
        {"ref": "A1", "q": 10, "pu": 5.0, "seuil": 2},
        {"ref": "A2", "q": 2, "pu": 10.0, "seuil": 5},
    ]
    assert calculer_valeur_stock(articles) == 70.0

