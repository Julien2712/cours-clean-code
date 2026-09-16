from parking import calculer_prix


def test_stationnement_30_minutes_ou_moins_est_gratuit():
    assert calculer_prix(0) == 0.00
    assert calculer_prix(15) == 0.00
    assert calculer_prix(30) == 0.00

def test_au_dela_de_30_minutes_le_tarif_est_1_5_par_demi_heure_supp():
    assert calculer_prix(31) == 1.5
    assert calculer_prix(60) == 1.5
    assert calculer_prix(61) == 3.0
    assert calculer_prix(120)==4.5
