"""Calcul du montant d'une facture d'abonnement."""

from facturation.abonnements import (
    FORMULE_ENTREPRISE,
    FORMULE_ESSENTIEL,
    FORMULE_PRO,
    Abonnement,
)

TAUX_TVA = 0.20


class FormuleInconnue(ValueError):
    """La formule demandee n'existe pas au catalogue."""


class CodePromoInconnu(ValueError):
    """Le code promotionnel n'existe pas."""

# --- Points d'ouverture pour l'OCP ---

Prix_Formule = {
    FORMULE_ESSENTIEL: 9.0,
    FORMULE_PRO: 19.0,
    FORMULE_ENTREPRISE: 39.0,
}

Remise_Volume = [
    (50, 0.20),
    (10, 0.10),
]

def _promo_bienvenue(montant: float, premiere_facture: bool) -> float:
    if premiere_facture:
        return max(0.0, montant - 5.0)
    return montant

def _promo_noel(montant: float, premiere_facture: bool) -> float:
    return montant * 0.85

REGLES_PROMO = {
    "BIENVENUE": _promo_bienvenue,
    "NOEL": _promo_noel,
}

# --- Fonctions de calcul ---

def prix_par_poste(formule: str) -> float:
    if formule not in Prix_Formule:
        raise FormuleInconnue(formule)
    return Prix_Formule[formule]


def taux_de_remise_volume(nombre_de_postes: int) -> float:
    for seuil, taux in sorted(Remise_Volume, reverse=True):
        if nombre_de_postes >= seuil:
            return taux
    return 0.0


def appliquer_code_promo(montant: float, code: str | None, premiere_facture: bool) -> float:
    if code is None:
        return montant
    if code not in REGLES_PROMO:
        raise CodePromoInconnu(code)
    
    fonction_de_calcul = REGLES_PROMO[code]
    return fonction_de_calcul(montant, premiere_facture)


def montant_hors_taxe(
    abonnement: Abonnement,
    code_promo: str | None = None,
    premiere_facture: bool = False,
) -> float:
    base = prix_par_poste(abonnement.formule) * abonnement.nombre_de_postes
    apres_volume = base * (1 - taux_de_remise_volume(abonnement.nombre_de_postes))
    return round(appliquer_code_promo(apres_volume, code_promo, premiere_facture), 2)


def montant_toutes_taxes(
    abonnement: Abonnement,
    code_promo: str | None = None,
    premiere_facture: bool = False,
) -> float:
    return round(montant_hors_taxe(abonnement, code_promo, premiere_facture) * (1 + TAUX_TVA), 2)