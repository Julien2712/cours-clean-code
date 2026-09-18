from facturation.tarifs import Prix_Formule, REGLES_PROMO

# D1 : Nouvelle formule
Prix_Formule["decouverte"] = 4.0

# D2 : Nouveau code promo
def promo_rentree(montant: float, premiere_facture: bool) -> float:
    return montant * 0.9

REGLES_PROMO["RENTREE"] = promo_rentree