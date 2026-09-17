import inventaire
from inventaire import (
    MOUVEMENT_ENTREE,
    MOUVEMENT_SORTIE,
    calculer_cout_reapprovisionnement,
    calculer_rotation_stock,
    calculer_synthese_stock,
    calculer_valeur_stock,
    enregistrer_mouvement_stock,
    export_json,
    filtrer_articles_valides,
    rapport,
    recuperer_article_en_alerte,
    regrouper_valeur_par_categorie,
    trier_articles_par_valeur,
)


def test_valeur_stock_standard():
    articles = [
        {"ref": "A1", "q": 10, "pu": 5.0},
        {"ref": "A2", "q": 2, "pu": 10.0},
    ]
    assert calculer_valeur_stock(articles) == 70.0


def test_valeur_stock_ignore_les_quantites_negatives_ou_nulles():
    articles = [
        {"ref": "A1", "q": -5, "pu": 10.0},
        {"ref": "A2", "q": 0, "pu": 10.0},
        {"ref": "A3", "q": 3, "pu": 10.0},
    ]
    assert calculer_valeur_stock(articles) == 30.0


def test_valeur_stock_est_arrondie_au_centime():
    articles = [{"ref": "A1", "q": 3, "pu": 0.333}]
    assert calculer_valeur_stock(articles) == 1.0


def test_valeur_stock_liste_vide():
    assert calculer_valeur_stock([]) == 0


def test_article_strictement_sous_le_seuil_est_en_alerte():
    articles = [{"ref": "A1", "q": 1, "seuil": 2}]
    assert recuperer_article_en_alerte(articles) == ["A1"]


def test_article_exactement_au_seuil_n_est_PAS_en_alerte_ECART_M2():
    articles = [{"ref": "A1", "q": 2, "seuil": 2}]
    assert recuperer_article_en_alerte(articles) == []


def test_article_au_dessus_du_seuil_n_est_pas_en_alerte():
    articles = [{"ref": "A1", "q": 5, "seuil": 2}]
    assert recuperer_article_en_alerte(articles) == []


def test_mouvement_sortie_valide_diminue_le_stock():
    article = {"ref": "A1", "q": 10}
    assert enregistrer_mouvement_stock(article, 5) is True
    assert article["q"] == 5


def test_mouvement_entree_augmente_le_stock():
    article = {"ref": "A1", "q": 10}
    assert enregistrer_mouvement_stock(article, 5, MOUVEMENT_ENTREE) is True
    assert article["q"] == 15


def test_mouvement_quantite_nulle_est_refuse_M4():
    article = {"ref": "A1", "q": 10}
    assert enregistrer_mouvement_stock(article, 0) is False
    assert article["q"] == 10


def test_mouvement_quantite_negative_est_refuse_M4():
    article = {"ref": "A1", "q": 10}
    assert enregistrer_mouvement_stock(article, -3) is False
    assert article["q"] == 10


def test_mouvement_sortie_superieure_au_stock_est_refuse():
    article = {"ref": "A1", "q": 5}
    assert enregistrer_mouvement_stock(article, 10) is False


def test_mouvement_sortie_refusee_MODIFIE_QUAND_MEME_LE_STOCK_ECART_M3():
    article = {"ref": "A1", "q": 5}
    enregistrer_mouvement_stock(article, 10)
    assert article["q"] == -5


def test_mouvement_sortie_forcee_autorise_le_stock_negatif():
    article = {"ref": "A1", "q": 5}
    assert enregistrer_mouvement_stock(article, 10, MOUVEMENT_SORTIE, forcer=True) is True
    assert article["q"] == -5


def test_mouvement_type_inconnu_est_refuse():
    article = {"ref": "A1", "q": 10}
    assert enregistrer_mouvement_stock(article, 5, "transfert") is False


def test_mouvement_incremente_dernier_et_alimente_le_journal():
    article = {"ref": "A1", "q": 10}
    avant = inventaire.DERNIER
    enregistrer_mouvement_stock(article, 3)
    assert inventaire.DERNIER == avant + 1
    assert inventaire.JOURNAL[-1]["ref"] == "A1"
    assert inventaire.JOURNAL[-1]["q"] == 3


def test_cout_article_pas_en_alerte_est_nul():
    article = {"q": 10, "seuil": 5, "pu": 2.0}
    assert calculer_cout_reapprovisionnement(article) == 0


def test_cout_article_exactement_au_seuil_est_nul():
    article = {"q": 5, "seuil": 5, "pu": 2.0}
    assert calculer_cout_reapprovisionnement(article) == 0


def test_cout_article_en_alerte_sans_remise():
    article = {"q": 2, "seuil": 5, "pu": 2.0}
    assert calculer_cout_reapprovisionnement(article) == 26.0


def test_cout_article_en_alerte_avec_remise_au_dela_de_100():
    article = {"q": 50, "seuil": 100, "pu": 10.0}
    assert calculer_cout_reapprovisionnement(article) == 2250.0


def test_cout_a_exactement_100_unites_N_A_PAS_la_remise_ECART_M5():
    article = {"q": 5, "seuil": 35, "pu": 10.0}
    assert calculer_cout_reapprovisionnement(article) == 1000.0


def test_tri_par_valeur_decroissante():
    articles = [
        {"ref": "A1", "q": 2, "pu": 10.0},
        {"ref": "A2", "q": 10, "pu": 5.0},
        {"ref": "A3", "q": 1, "pu": 5.0},
    ]
    resultat = trier_articles_par_valeur(articles)
    assert [a["ref"] for a in resultat] == ["A2", "A1", "A3"]


def test_tri_ne_modifie_pas_la_liste_d_origine():
    articles = [{"ref": "A1", "q": 1, "pu": 1.0}, {"ref": "A2", "q": 2, "pu": 1.0}]
    ordre_avant = [a["ref"] for a in articles]
    trier_articles_par_valeur(articles)
    assert [a["ref"] for a in articles] == ordre_avant


def test_tri_liste_vide():
    assert trier_articles_par_valeur([]) == []


def test_rotation_calcul_standard():
    article = {"q": 60}
    assert calculer_rotation_stock(article, 30) == 60


def test_rotation_aucune_vente_NE_LEVE_PAS_D_ERREUR_ECART_M7():
    article = {"q": 60}
    assert calculer_rotation_stock(article, 0) == 0


def test_filtrer_articles_valides_exclut_quantite_et_prix_nuls():
    articles = [
        {"ref": "A1", "q": 0, "pu": 5.0, "seuil": 2, "cat": "outil"},
        {"ref": "A2", "q": 5, "pu": 0, "seuil": 2, "cat": "outil"},
        {"ref": "A3", "q": 5, "pu": 5.0, "seuil": 2, "cat": "outil"},
    ]
    resultat = filtrer_articles_valides(articles)
    assert [a["ref"] for a in resultat] == ["A3"]


def test_calculer_synthese_stock():
    articles = [{"ref": "A1", "q": 10, "pu": 5.0, "seuil": 2}]
    synthese = calculer_synthese_stock(articles)
    assert synthese["valeur"] == 50.0
    assert synthese["ttc"] == 60.0
    assert synthese["nb"] == 1
    assert synthese["alertes"] == []


def test_rapport_calcule_la_valeur_et_le_ttc():
    articles = [{"ref": "A1", "q": 10, "pu": 5.0, "seuil": 2, "cat": "outil"}]
    res = rapport(articles, verbose=False)
    assert res["valeur"] == 50.0
    assert res["ttc"] == 60.0
    assert res["nb"] == 1
    assert res["alertes"] == []


def test_rapport_signale_les_alertes():
    articles = [{"ref": "A1", "q": 1, "pu": 5.0, "seuil": 2, "cat": "outil"}]
    res = rapport(articles, verbose=False)
    assert res["alertes"] == ["A1"]


def test_rapport_filtre_par_categorie():
    articles = [
        {"ref": "A1", "q": 1, "pu": 5.0, "seuil": 2, "cat": "outil"},
        {"ref": "A2", "q": 1, "pu": 5.0, "seuil": 2, "cat": "piece"},
    ]
    res = rapport(articles, cat="outil", verbose=False)
    assert res["nb"] == 1


def test_rapport_ECRIT_SUR_LA_CONSOLE_PAR_DEFAUT_ECART_M8(capsys):
    articles = [{"ref": "A1", "q": 1, "pu": 5.0, "seuil": 2, "cat": "outil"}]
    rapport(articles)
    capture = capsys.readouterr()
    assert "ALERTE A1" in capture.out


def test_par_categorie_regroupe_les_valeurs():
    articles = [
        {"cat": "outil", "q": 2, "pu": 5.0},
        {"cat": "outil", "q": 1, "pu": 5.0},
        {"cat": "piece", "q": 1, "pu": 10.0},
    ]
    assert regrouper_valeur_par_categorie(articles) == {"outil": 15.0, "piece": 10.0}


def test_par_categorie_inconnue_tombe_dans_autre():
    articles = [{"cat": "gadget", "q": 1, "pu": 3.0}]
    assert regrouper_valeur_par_categorie(articles) == {"autre": 3.0}


def test_export_json_ecrit_le_fichier_et_retourne_l_historique(tmp_path):
    chemin = tmp_path / "inv.json"
    resultat = export_json({"valeur": 10}, chemin=str(chemin))
    assert chemin.exists()
    assert resultat == [{"valeur": 10}]


def test_export_json_ne_partage_plus_l_historique_entre_appels_FIX_ARGUMENT_MUTABLE(tmp_path):
    chemin_a = tmp_path / "inv_a.json"
    chemin_b = tmp_path / "inv_b.json"
    premier = export_json({"valeur": 1}, chemin=str(chemin_a))
    deuxieme = export_json({"valeur": 2}, chemin=str(chemin_b))
    assert premier is not deuxieme
    assert len(deuxieme) == 1