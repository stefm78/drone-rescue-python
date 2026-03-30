# =============================================================================
# CORRECTION 07 — Logique de jeu
# =============================================================================
# Toutes les entités sont des dictionnaires. Pas de classes.
# =============================================================================

import random


# --- utilitaire partagé ----------------------------------------------------- #

def distance_chebyshev(col1, lig1, col2, lig2):
    return max(abs(col2 - col1), abs(lig2 - lig1))


# -----------------------------------------------------------------------------
# EXERCICE 1 — Valider un mouvement de drone
# -----------------------------------------------------------------------------

def valider_mouvement(drone, col_c, lig_c, etat, depl_restants):
    """
    Vérifie les 5 règles dans l'ordre.
    Retourne (True, "") ou (False, "message").
    """
    # Règle 1 : distance == 1
    if distance_chebyshev(drone["col"], drone["lig"], col_c, lig_c) != 1:
        return False, "distance > 1"
    # Règle 2 : drone actif
    if drone["hors_service"]:
        return False, "hors service"
    # Règle 3 : drone non bloqué
    if drone["bloque"] > 0:
        return False, f"bloqué ({drone['bloque']} tours)"
    # Règle 4 : pas de bâtiment
    if (col_c, lig_c) in etat["batiments"]:
        return False, "bâtiment"
    # Règle 5 : déplacements restants
    if depl_restants <= 0:
        return False, "plus de déplacements"
    return True, ""


if __name__ == "__main__":
    etat_test = {"batiments": [(2, 3), (5, 1)]}
    drone = {"id": "D1", "col": 1, "lig": 2,
             "batterie": 8, "hors_service": False, "bloque": 0}

    ok, msg = valider_mouvement(drone, 2, 2, etat_test, 3)
    assert ok is True and msg == "", f"attendu True, got {ok} {msg}"

    ok, msg = valider_mouvement(drone, 2, 3, etat_test, 3)
    assert ok is False and "bâtiment" in msg

    ok, msg = valider_mouvement(drone, 5, 5, etat_test, 3)
    assert ok is False and "distance" in msg

    ok, msg = valider_mouvement(drone, 2, 2, etat_test, 0)
    assert ok is False and "déplacements" in msg

    drone_hs = dict(drone)
    drone_hs["hors_service"] = True
    ok, msg = valider_mouvement(drone_hs, 2, 2, etat_test, 3)
    assert ok is False and "service" in msg
    print("Ex1 OK")


# -----------------------------------------------------------------------------
# EXERCICE 2 — Calculer le coût batterie
# -----------------------------------------------------------------------------

def calculer_cout(drone, col_c, lig_c, etat):
    """
    Retourne le coût net (négatif = dépense, positif = recharge).
    """
    cout = -1                                     # base : -1
    if drone["survivant"] is not None:
        cout -= 1                                  # avec survivant : -2 total
    if (col_c, lig_c) in etat["zones_x"]:
        cout -= 2                                  # zone X : -2 supplémentaire
    if (col_c, lig_c) == etat["hopital"]:
        cout += 3                                  # hôpital : +3 recharge
    return cout
    # La batterie ne peut pas descendre sous 0 — appliqué dans executer_mouvement.


if __name__ == "__main__":
    etat2 = {"hopital": (0, 7), "zones_x": {(4, 4)}}
    drone_libre  = {"survivant": None}
    drone_charge = {"survivant": "S1"}

    assert calculer_cout(drone_libre,  1, 0, etat2) == -1
    assert calculer_cout(drone_charge, 1, 0, etat2) == -2
    assert calculer_cout(drone_libre,  4, 4, etat2) == -3
    assert calculer_cout(drone_charge, 4, 4, etat2) == -4
    assert calculer_cout(drone_charge, 0, 7, etat2) == 1   # -2 + 3
    print("Ex2 OK")


# -----------------------------------------------------------------------------
# EXERCICE 3 — Propager les zones X
# -----------------------------------------------------------------------------

def propager_zones_x(etat, proba=0.3):
    """
    Propage orthogonalement les zones X.
    Retourne la liste des nouvelles positions ajoutées.
    """
    taille     = len(etat["grille"])
    batiments  = set(etat["batiments"])  # set pour test O(1)
    hopital    = etat["hopital"]
    # Positions des survivants encore en attente (ne se propagent pas dessus)
    surv_pos   = {(s["col"], s["lig"])
                  for s in etat["survivants"].values()
                  if s["etat"] == "en_attente"}

    nouvelles = []
    for (zc, zl) in list(etat["zones_x"]):  # copie pour éviter RuntimeError
        for dc, dl in ((0, -1), (0, 1), (-1, 0), (1, 0)):  # 4 directions ortho
            nc, nl = zc + dc, zl + dl
            if not (0 <= nc < taille and 0 <= nl < taille):
                continue   # hors grille
            cand = (nc, nl)
            if cand in batiments or cand == hopital or cand in surv_pos:
                continue   # cases protégées
            if cand in etat["zones_x"]:
                continue   # déjà une zone X
            if random.random() < proba:
                etat["zones_x"].add(cand)
                nouvelles.append(cand)
    return nouvelles


if __name__ == "__main__":
    random.seed(42)
    etat3 = {
        "zones_x"   : {(4, 4)},
        "batiments" : [(4, 3)],
        "hopital"   : (0, 7),
        "survivants": {"S1": {"col": 4, "lig": 5, "etat": "en_attente"}},
        "grille"    : [['.'] * 8 for _ in range(8)],
    }
    nouvelles = propager_zones_x(etat3, proba=1.0)
    assert sorted(nouvelles) == [(3, 4), (5, 4)]
    assert sorted(etat3["zones_x"]) == [(3, 4), (4, 4), (5, 4)]
    print("Ex3 OK")


# -----------------------------------------------------------------------------
# EXERCICE 4 — Vérifier la fin de partie
# -----------------------------------------------------------------------------

def verifier_fin_partie(etat):
    """
    Retourne "VICTOIRE", "DEFAITE_TOURS", "DEFAITE_DRONES" ou "EN_COURS".
    all() retourne True si l'itérable est vide — sécurisé ici car
    on ne lance jamais une partie avec 0 survivant ni 0 drone.
    """
    # Victoire d'abord : tous les survivants sont sauvés
    if all(s["etat"] == "sauve" for s in etat["survivants"].values()):
        return "VICTOIRE"
    # Défaite tours : tour dépasse le maximum
    if etat["tour"] > etat["tour_max"]:
        return "DEFAITE_TOURS"
    # Défaite drones : tous hors service
    if all(d["hors_service"] for d in etat["drones"].values()):
        return "DEFAITE_DRONES"
    return "EN_COURS"


if __name__ == "__main__":
    etat4 = {
        "tour"     : 5,
        "tour_max" : 20,
        "survivants": {
            "S1": {"etat": "sauve"},
            "S2": {"etat": "en_attente"},
        },
        "drones": {
            "D1": {"hors_service": False},
            "D2": {"hors_service": False},
        },
    }
    assert verifier_fin_partie(etat4) == "EN_COURS"
    etat4["survivants"]["S2"]["etat"] = "sauve"
    assert verifier_fin_partie(etat4) == "VICTOIRE"
    etat4["survivants"]["S2"]["etat"] = "en_attente"
    etat4["tour"] = 21
    assert verifier_fin_partie(etat4) == "DEFAITE_TOURS"
    etat4["tour"] = 5
    etat4["drones"]["D1"]["hors_service"] = True
    etat4["drones"]["D2"]["hors_service"] = True
    assert verifier_fin_partie(etat4) == "DEFAITE_DRONES"
    print("Ex4 OK")
