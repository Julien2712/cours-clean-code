def calculer_prix(duree_minutes, abonne=False, electrique=False):
    if duree_minutes <= 30:
        return 0.00
