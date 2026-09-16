# Rapport qualité, module inventaire

Nom :
Date :
Empreinte du commit de départ :

---

## 1. Tableau de bord initial

Mesures relevées avant toute modification.

### Complexité par fonction

| Fonction | Ligne | Complexité cyclomatique | Rang |
|---|---|---|---|
| rapport | 122 | 22 | D |
| par_cat | 94 | 10 | B |
| mouv | 37 | 9 | B |
| classer | 74 | 5 | A |
| val | 19 | 3 | A |
| alerte | 29 | 3 | A |
| cout | 62 | 3 | A |
| rot | 87 | 2 | A |
| maj_prix | 175 | 1 | A |
| export_json | 185 | 1 | A |

Commande utilisée :

```bash
radon cc inventaire.py -s -a
```

### Synthèse du fichier

### Synthèse du fichier

| Mesure | Valeur | Commande |
|---|---|---|
| Lignes de code réelles | 159 (SLOC) | `radon raw inventaire.py` |
| Complexité moyenne | B (5,9) | `radon cc inventaire.py -s -a` |
| Indice de maintenabilité | A (36,80) | `radon mi inventaire.py -s` |
| Score pylint | 7.76/10 | `pylint inventaire.py` |
| Problèmes ruff | 14    | `ruff check inventaire.py` |
| Entrées vulture | 14 trouvés dont 2 100%, 12 60% | `vulture inventaire.py` |
| Couverture de branches | 0% | `pytest --cov=inventaire --cov-branch --cov-report=term-missing` |
| Barrière xenon | Echec code exit 1, rapport rang D, moyenne des fichiers rang B |`xenon --max-absolute B --max-modules B --max-average A inventaire.py`|

---

## 2. Catalogue des odeurs

Douze entrées minimum. Trois au moins doivent être invisibles pour les outils.
La colonne conséquence décrit ce qui arrive à la personne qui devra modifier ce
fichier dans six mois.

| # | Ligne | Odeur ou défaut | Détecté par | Conséquence concrète |
|---|---|---|---|---|
| 1 | 37 | Argument par défaut mutable `j=[]` | ruff (B006) + pylint (W0102) | La liste est partagée entre tous les appels : elle s'accumule silencieusement d'un appel à l'autre. |
| 2 | 185 | Argument par défaut mutable `hist=[]` | ruff (B006) + pylint (W0102) | Même bug sur `export_json` : l'historique grossit indéfiniment entre appels sans lien. |
| 3 | 90 | `except:` nu | ruff (E722) + pylint (W0702) | Toute erreur (même une vraie panne) est avalée et transformée en `0`. |
| 4 | 46 | `if force == False:` | pylint (C0121) | Illisible ; si `force` change de type un jour, le comportement change silencieusement. |
| 5 | 122 | `rapport()` : 7 paramètres, 21 branches, CC=22 (rang D) | pylint (R0913, R0912, R1702) + radon/xenon | Impossible à tester sans capturer stdout ; tout changement a un impact énorme. |
| 6 | 94 | `par_cat` duplique un bloc if/elif par catégorie | pylint (R0912) | Ajouter une catégorie oblige à copier-coller un bloc de plus. |
| 7 | 169, 187 | `open()` sans `with` ni `encoding=` | ruff (SIM115) + pylint (R1732, W1514) | Fuite de fichier si erreur avant `close()` ; encodage imprévisible selon l'OS. |
| 8 | 78 | Variable `i` jamais utilisée dans le tri | pylint (W0612) + vulture (60%) | Signe d'une boucle redondante : le tri est deux fois plus lent que nécessaire. |
| 9 | 175 | Paramètres `ref`, `p` inutilisés dans `maj_prix` | pylint (W0613) + vulture (100%) | La fonction ne fait rien : l'appeler ne met aucun prix à jour. |
| 10 | 15 | Variable globale `STOCK` jamais utilisée | vulture (60%) | Risque qu'un dev y écrive du code que personne ne relira jamais. |
| 11 | 124 | `datetime.now()` sans fuseau horaire | ruff (DTZ005) | Dates incohérentes si le serveur change de fuseau. |
| 12 | 1, 19-185 | Aucune docstring (module + 9 fonctions) | pylint (C0114, C0116) | Impossible de savoir ce que fait une fonction sans lire tout son code. |
| 13 | 37 | Paramètres booléens `force`/`log` | lecture manuelle | Appel illisible ; deux booléens inversés passent inaperçus. |
| 14 | 11-13 | Constantes cryptiques `S`, `R`, `Q` | lecture manuelle | `S` dans `cout()` est incompréhensible sans deviner son sens métier. |
| 15 | 4 | Commentaire "NE PAS TOUCHER À mouv()" | lecture manuelle | Preuve que la peur remplace les tests comme protection. |
| 16 | 74-84 | Tri à bulles réécrit à la main | lecture manuelle | Lent sur un gros inventaire ; un simple `sorted()` suffisait. |
| 17 | 168 | Nom de fichier aléatoire dans `/tmp/` codé en dur | lecture manuelle | Collision possible ; `/tmp` n'existe pas sous Windows. |

---

## 3. Faut-il tout réécrire

Une demi-page. Chiffres de la partie 1, au moins un exemple historique vu en cours,
et un ordre d'intervention justifié.

---

Au vu des résultats obtenus par les différents tests — score pylint de
7,76/10, indice de maintenabilité A (36,80), complexité moyenne B (5,9),
14 problèmes remontés par vulture, 0 % de couverture de branches et un
échec à la barrière xenon — on pourrait croire, en s'arrêtant aux deux
premiers chiffres, que le fichier va plutôt bien.

Pourtant ces deux chiffres flatteurs sont une moyenne calculée sur tout le
fichier : ils diluent la seule fonction réellement problématique
(`rapport`, CC=22, rang D) dans neuf autres fonctions triviales (rang A).
Le chiffre qui ne ment pas, c'est xenon : échec formel dès qu'on fixe un
seuil raisonnable. Et aucun de ces indicateurs ne remplace ce qui manque
vraiment : 0 % de couverture de tests, donc aucune preuve qu'une
modification ne casse rien.

Dans le cours nous avions l'exemple de Netscape : en 1997, l'équipe a
choisi de jeter et réécrire son moteur de rendu après avoir perdu la
compréhension de son propre code. Résultat, deux ans sans version
compétitive pendant qu'Internet Explorer passait de 20 % à plus de 80 %
du marché, et l'équipe a fini dissoute (p.12).

Le fichier `inventaire.py` n'est pas dans l'état de Netscape avant sa
catastrophe : il est en général plutôt sain, avec quelques problèmes de
lisibilité et de maintenabilité concentrés sur une seule fonction, rien
de critique à l'échelle du fichier. On peut donc, au lieu de tout
réécrire, simplement corriger les erreurs.

**Ordre d'intervention** : d'abord des tests de caractérisation sur
`mouv` et `rapport` (les fonctions les plus risquées) pour avoir un
filet ; ensuite les corrections rapides déjà repérées par les outils
(arguments par défaut mutables, `except` nu) ; enfin, seulement une fois
protégée par les tests, la décomposition de `rapport()`.

## 4. Écarts constatés entre le code et les règles métier

Rempli pendant la mission 3, sans rien corriger.

| Règle | Ligne | Ce que le code fait | Ce que la règle dit |
|---|---|---|---|
|  |  |  |  |

---

## 5. Tableau de bord après refactoring

Mêmes mesures, mêmes commandes qu'en partie 1.

| Mesure | Avant | Après | Écart |
|---|---|---|---|
|  |  |  |  |

Ce que ce delta prouve, en trois phrases maximum :

---

## 6. Bugs prouvés puis corrigés

| Règle violée | Ligne d'origine | Commit red | Commit fix | Conséquence métier |
|---|---|---|---|---|
|  |  |  |  |  |

Pour au moins un de ces bugs, la conséquence est chiffrée en euros ou en ruptures de stock.
