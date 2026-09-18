from facturation.tarifs import appliquer_code_promo, prix_par_poste
import facturation.nouvelles_regles

def test_formule_decouverte_est_a_4e():
    assert prix_par_poste("decouverte") == 4.0

def test_promo_rentree_moins_10_pourcent():
    assert appliquer_code_promo(100.0, "RENTREE", False) == 90.0
    assert appliquer_code_promo(100.0, "RENTREE", True) == 90.0