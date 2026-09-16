def calculer_prix(duree_minutes, abonne=False, electrique=False):
    prix = 0
    if duree_minutes <= 30:
        prix = 0.00
    else:
        nb_heures = (duree_minutes - 30 + 29) // 30
        prix = 1.5 * nb_heures
    return prix
