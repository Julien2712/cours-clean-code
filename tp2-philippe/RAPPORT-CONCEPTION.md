# Rapport de Conception - TP2

## Partie 1 : Les cinq violations

| Principe | Fichier et ligne | Le symptôme observable | La conséquence concrète |
|---|---|---|---|
| **DIP** | `facture.py`, ligne 24 | La classe `EmetteurDeFactures` instancie directement `ClientSMTP`. | Impossible de changer le moyen d'envoi sans modifier le code métier et impossible de tester sans le réseau. |
| **ISP** | `passerelles.py`, ligne 28 | `ClientSMTP` implémente `envoyer_sms` et `envoyer_notification_push` en levant `NotImplementedError`. | Le client dépend d'une interface beaucoup trop large par rapport à son seul besoin (envoyer un courriel). |
| **SRP** | `facture.py`, ligne 29 | La méthode `emettre` calcule les montants, formate le texte en chaîne de caractères, et envoie le courriel. | Modifier la présentation visuelle de la facture oblige à rouvrir la fonction qui gère les calculs et le réseau. |
| **LSP** | `abonnements.py`, ligne 44 | `AbonnementAnnuel.resilier` lève `ResiliationImpossible` brisant la docstring du parent. | Une fonction cliente qui manipule des `Abonnement` de manière polymorphique plantera sur ce sous-type. |
| **OCP** | `tarifs.py`, ligne 33 | `appliquer_code_promo` énumère les codes avec des conditions `if` en dur. | Ajouter un nouveau code promo oblige à rouvrir et modifier une fonction existante déjà couverte par des tests. |

## Partie 2 : Le coût des trois demandes

| Demande | Fichiers à rouvrir | Fonctions à modifier | Tests existants à rejouer |
|---|---|---|---|
| **D1. Formule découverte (4€)** | `tarifs.py`, `abonnements.py`, `test_facturation.py` | `prix_par_poste` | `test_chaque_formule_a_son_prix_par_poste` |
| **D2. Code RENTREE (-10%)** | `tarifs.py`, `test_facturation.py` | `appliquer_code_promo` | `test_un_code_promo_inconnu_est_refuse` |
| **D3. Palier 30% (200 postes)** | `tarifs.py`, `test_facturation.py` | `taux_de_remise_volume` | `test_la_remise_volume_suit_les_paliers` |

## Partie 3 : Le graphe des dépendances

*   **`abonnements.py`** : n'importe aucune dépendance externe.
*   **`tarifs.py`** : importe `abonnements.py`.
*   **`passerelles.py`** : n'importe que l'outil de base `abc`.
*   **`facture.py`** : importe `abonnements.py`, `tarifs.py` et `ClientSMTP` depuis `passerelles.py`.

**Le candidat à l'inversion :**
La dépendance de `facture.py` vers `ClientSMTP` de `passerelles.py`. Le module métier qui gère les factures dépend directement d'un module technique de réseau.