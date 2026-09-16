from parking import calculer_prix


def test_stationnement_30_minutes_ou_moins_est_gratuit():
    assert calculer_prix(0) == 0.00
    assert calculer_prix(15) == 0.00
    assert calculer_prix(30) == 0.00
