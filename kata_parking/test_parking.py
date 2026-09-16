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

def test_le_montant_est_plafonne_a_18_euros_par_tranche_de_24h():
    assert calculer_prix(8 * 60) == 18.00
    assert calculer_prix(24 * 60) == 18.00
    assert calculer_prix(25 * 60) == 36.00


def test_camion_abonne_paie_60_pourcent_du_montant():
    assert calculer_prix(31, abonne=True) == 0.90
    assert calculer_prix(8 * 60, abonne=True) == 10.80
