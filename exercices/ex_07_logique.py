# =============================================================================
# EXERCICE 07 — Logique de jeu
# Module correspondant : cours/07_logique_de_jeu.md
# =============================================================================
# Objectifs :
#   - Valider et exécuter les déplacements avec les règles officielles
#   - Gérer la collecte et la livraison des survivants
#   - Implanter la propagation des zones X
#   - Vérifier les conditions de fin de partie avec all()
# =============================================================================
# Toutes les entités sont des dictionnaires — pas de classes.
# =============================================================================

import random


# -----------------------------------------------------------------------------
# EXERCICE 1 — Valider un mouvement de drone
# -----------------------------------------------------------------------------
# Règles officielles à vérifier dans l'ordre :
#   1. Distance de Chebyshev entre départ et arrivée == 1
#   2. Drone non HS (hors_service == False)
#   3. Drone non bloqué (bloque == 0)
#   4. Case cible non occupée par un bâtiment (col_c, lig_c) pas dans batiments
#   5. Déplacements restants ce tour > 0
#
# Écris : valider_mouvement(drone, col_c, lig_c, etat, depl_restants)
#   drone : dict avec clés col, lig, hors_service, bloque
#   etat  : dict avec clé "batiments" (liste de tuples (col, lig))
#   → retourne (True, "") si valide
#   → retourne (False, "message d'erreur") sinon
# -----------------------------------------------------------------------------

def distance_chebyshev(col1, lig1, col2, lig2):
    return max(abs(col2 - col1), abs(lig2 - lig1))


def valider_mouvement(drone, col_c, lig_c, etat, depl_restants):
    """
    Valide le mouvement du drone vers (col_c, lig_c).
    Retourne (bool, message).
    """
    # TODO
    pass


# Tests exercice 1
if __name__ == "__main__":
    etat_test = {"batiments": [(2, 3), (5, 1)]}
    drone = {"id": "D1", "col": 1, "lig": 2,
             "batterie": 8, "hors_service": False, "bloque": 0}

    ok, msg = valider_mouvement(drone, 2, 2, etat_test, 3)
    print(ok, msg)    # True ""

    ok, msg = valider_mouvement(drone, 2, 3, etat_test, 3)
    print(ok, msg)    # False  "bâtiment"

    ok, msg = valider_mouvement(drone, 5, 5, etat_test, 3)
    print(ok, msg)    # False  "distance > 1"

    ok, msg = valider_mouvement(drone, 2, 2, etat_test, 0)
    print(ok, msg)    # False  "plus de déplacements"

    drone_hs = dict(drone)
    drone_hs["hors_service"] = True
    ok, msg = valider_mouvement(drone_hs, 2, 2, etat_test, 3)
    print(ok, msg)    # False  "hors service"


# -----------------------------------------------------------------------------
# EXERCICE 2 — Calculer le coût batterie
# -----------------------------------------------------------------------------
# Règles officielles :
#   - Déplacement seul       : -1
#   - Avec survivant embarqué : -2
#   - En zone X              : -2 supplémentaire
#   - À l'hôpital           : +3 (et livraison si survivant)
#   La batterie ne peut pas descendre sous 0.
#
# Écris : calculer_cout(drone, col_c, lig_c, etat)
#   etat : dict avec "hopital" (col, lig), "zones_x" (set de tuples)
#   → retourne l'entier (peut être négatif = recharge)
# -----------------------------------------------------------------------------

def calculer_cout(drone, col_c, lig_c, etat):
    """
    Retourne le coût batterie du mouvement (négatif = recharge).
    """
    # TODO
    # 1. Base : -1
    # 2. Si survivant embarqué : -1 supplémentaire
    # 3. Si cible dans zones_x : -2 supplémentaire
    # 4. Si cible == hopital : +3 (recharge)
    pass


# Tests exercice 2
if __name__ == "__main__":
    etat2 = {
        "hopital": (0, 7),
        "zones_x": {(4, 4)},
    }
    drone_libre = {"survivant": None}
    drone_charge = {"survivant": "S1"}

    print(calculer_cout(drone_libre, 1, 0, etat2))   # -1  (dépl simple)
    print(calculer_cout(drone_charge, 1, 0, etat2))  # -2  (avec survivant)
    print(calculer_cout(drone_libre, 4, 4, etat2))   # -3  (zone X)
    print(calculer_cout(drone_charge, 4, 4, etat2))  # -4  (survivant + zone X)
    print(calculer_cout(drone_charge, 0, 7, etat2))  # +1  (-2 + 3 recharge)


# -----------------------------------------------------------------------------
# EXERCICE 3 — Propager les zones X
# -----------------------------------------------------------------------------
# Règles :
#   - Se propage sur les 4 cases orthogonales (pas de diagonal)
#   - Ne se propage pas sur bâtiment, hôpital, survivant
#   - Probabilité de propagation : random.random() < proba
#   - Se déclenche tous les 3 tours
#
# Écris : propager_zones_x(etat, proba=0.3)
#   etat : dict avec "zones_x" (set), "batiments", "hopital", "survivants",
#          "grille" (pour la taille)
#   → modifie etat["zones_x"] en place
#   → retourne la liste des nouvelles positions ajoutées
# -----------------------------------------------------------------------------

def propager_zones_x(etat, proba=0.3):
    """
    Propage les zones X de façon orthogonale.
    Modifie etat["zones_x"] et retourne les nouvelles positions.
    """
    # TODO
    # 1. Parcourir list(etat["zones_x"]) (copie pour éviter RuntimeError)
    # 2. Pour chaque zone, calculer les 4 voisins orthogonaux
    # 3. Filtrer : dans grille, pas batiment, pas hopital, pas survivant
    # 4. Pour chaque candidat : random.random() < proba → ajouter au set
    pass


# Tests exercice 3
if __name__ == "__main__":
    random.seed(42)
    etat3 = {
        "zones_x"   : {(4, 4)},
        "batiments" : [(4, 3)],
        "hopital"   : (0, 7),
        "survivants": {"S1": {"col": 4, "lig": 5, "etat": "en_attente"}},
        "grille"    : [['.'] * 8 for _ in range(8)],
    }
    nouvelles = propager_zones_x(etat3, proba=1.0)   # proba=1 = toujours
    # Voisins de (4,4) : (3,4), (5,4), (4,3)=batiment, (4,5)=survivant
    # Attendu : (3,4) et (5,4) seulement
    print(sorted(nouvelles))  # [(3, 4), (5, 4)]
    print(sorted(etat3["zones_x"]))  # [(3, 4), (4, 4), (5, 4)]


# -----------------------------------------------------------------------------
# EXERCICE 4 — Vérifier la fin de partie
# -----------------------------------------------------------------------------
# VICTOIRE : all(s["etat"] == "sauve" for s in etat["survivants"].values())
# DÉFAITE tours : etat["tour"] > etat["tour_max"]
# DÉFAITE drones : all(d["hors_service"] for d in etat["drones"].values())
#
# Écris : verifier_fin_partie(etat)
#   → retourne "VICTOIRE", "DEFAITE_TOURS", "DEFAITE_DRONES", ou "EN_COURS"
# Note : utiliser all() et les dict
# -----------------------------------------------------------------------------

def verifier_fin_partie(etat):
    """
    Retourne l'état de la partie : "VICTOIRE", "DEFAITE_TOURS",
    "DEFAITE_DRONES", ou "EN_COURS".
    """
    # TODO
    # Conseil : tester la victoire en premier
    pass


# Tests exercice 4
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
    print(verifier_fin_partie(etat4))   # EN_COURS

    etat4["survivants"]["S2"]["etat"] = "sauve"
    print(verifier_fin_partie(etat4))   # VICTOIRE

    etat4["survivants"]["S2"]["etat"] = "en_attente"
    etat4["tour"] = 21
    print(verifier_fin_partie(etat4))   # DEFAITE_TOURS

    etat4["tour"] = 5
    etat4["drones"]["D1"]["hors_service"] = True
    etat4["drones"]["D2"]["hors_service"] = True
    print(verifier_fin_partie(etat4))   # DEFAITE_DRONES
