import math


def calculer_prix(duree_minutes, abonne=False, electrique=False):
    prix = 0
    if duree_minutes <= 30:
        prix = 0.00
    else:
        nb_demi_heures = math.ceil((duree_minutes - 30) / 30)
        prix = 1.5 * nb_demi_heures

    nb_tranches_24h = math.ceil(duree_minutes / 1440)
    plafond = 18.0 * nb_tranches_24h
    prix = min(prix, plafond)

    return prix
