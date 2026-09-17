from inventaire import calculer_valeur_stock, recuperer_article_en_alerte


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
