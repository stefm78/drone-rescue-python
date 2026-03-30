# =============================================================================
# EXERCICE 05 — Dictionnaires avancés et sets
# Module correspondant : cours/05_dictionnaires_avances.md
# =============================================================================
# Objectifs :
#   - Créer des dictionnaires représentant des entités du jeu
#   - Manipuler des dicts de dicts
#   - Utiliser des sets de tuples pour stocker des positions
#   - Écrire des fonctions factory
# =============================================================================


# -----------------------------------------------------------------------------
# EXERCICE 1 — Créer un drone (fonction factory)
# -----------------------------------------------------------------------------
# Dans Drone Rescue, un drone est représenté par un dictionnaire.
# Écris la fonction creer_drone(identifiant, col, lig, batterie_max=20, batterie_init=10)
# qui retourne un dictionnaire avec les clés :
#   id, col, lig, batterie, batterie_max, survivant, bloque, hors_service
#
# Contraintes :
#   - col et lig sont des entiers (index 0-basé)
#   - survivant vaut None par défaut
#   - bloque vaut 0 par défaut
#   - hors_service vaut False par défaut
# -----------------------------------------------------------------------------

def creer_drone(identifiant, col, lig, batterie_max=20, batterie_init=10):
    """
    Retourne un dictionnaire représentant un drone.
    col, lig : entiers 0-basés.
    """
    # TODO
    pass


# Tests exercice 1
if __name__ == "__main__":
    d = creer_drone("D1", 0, 5)
    print(d["id"])           # D1
    print(d["batterie"])     # 10
    print(d["batterie_max"]) # 20
    print(d["survivant"])    # None
    print(d["hors_service"]) # False

    d2 = creer_drone("D2", 3, 7, batterie_max=15, batterie_init=8)
    print(d2["batterie"])    # 8
    print(d2["batterie_max"])# 15


# -----------------------------------------------------------------------------
# EXERCICE 2 — Dict de dicts : l'état global
# -----------------------------------------------------------------------------
# L'état du jeu est un dict qui contient tous les drones dans un dict de dicts :
#   etat["drones"]["D1"]["batterie"]
#
# Écris initialiser_drones(nb=6, batterie_max=20, batterie_init=10)
# qui retourne un dict de dicts :
#   {"D1": creer_drone(...), "D2": creer_drone(...), ...}
# Positionne les drones sur la ligne 0, colonnes 0 à nb-1.
# -----------------------------------------------------------------------------

def initialiser_drones(nb=6, batterie_max=20, batterie_init=10):
    """
    Retourne un dict de dicts {"D1": {...}, "D2": {...}, ...}.
    """
    # TODO
    # Pense à utiliser creer_drone() et une boucle
    pass


# Tests exercice 2
if __name__ == "__main__":
    drones = initialiser_drones(3)
    print(list(drones.keys()))       # ['D1', 'D2', 'D3']
    print(drones["D2"]["col"])       # 1
    print(drones["D3"]["batterie"])  # 10

    # Modifier la batterie de D1
    drones["D1"]["batterie"] -= 1
    print(drones["D1"]["batterie"])  # 9


# -----------------------------------------------------------------------------
# EXERCICE 3 — Sets de tuples pour les positions
# -----------------------------------------------------------------------------
# Les zones dangereuses X sont stockées dans un set de tuples (col, lig).
# Un set garantit l'unicité et teste l'appartenance en O(1).
#
# Écris les fonctions :
#   ajouter_zone_x(zones_x, col, lig) — ajoute (col, lig) au set
#   retirer_zone_x(zones_x, col, lig) — retire (col, lig) si présent (discard)
#   est_zone_x(zones_x, col, lig)     — retourne True si (col, lig) dans le set
# -----------------------------------------------------------------------------

def ajouter_zone_x(zones_x, col, lig):
    # TODO
    pass


def retirer_zone_x(zones_x, col, lig):
    # TODO
    pass


def est_zone_x(zones_x, col, lig):
    # TODO
    pass


# Tests exercice 3
if __name__ == "__main__":
    zones = set()
    ajouter_zone_x(zones, 3, 5)
    ajouter_zone_x(zones, 7, 2)
    ajouter_zone_x(zones, 3, 5)   # doublon — ne doit pas créer de duplication
    print(len(zones))             # 2
    print(est_zone_x(zones, 3, 5))  # True
    print(est_zone_x(zones, 0, 0))  # False
    retirer_zone_x(zones, 3, 5)
    print(est_zone_x(zones, 3, 5))  # False
    retirer_zone_x(zones, 9, 9)     # ne plante pas (discard)


# -----------------------------------------------------------------------------
# EXERCICE 4 — Accéder et modifier un dict de dicts
# -----------------------------------------------------------------------------
# Écris les fonctions suivantes qui opèrent sur etat["drones"] :
#
#   drone_par_id(drones, identifiant)
#     → retourne le dict du drone ou None si introuvable
#
#   drones_actifs(drones)
#     → retourne la liste des dicts de drones dont hors_service == False
#
#   consommer_batterie(drone, cout=1)
#     → diminue la batterie du drone de cout (min 0)
#     → met hors_service à True si batterie tombe à 0
# -----------------------------------------------------------------------------

def drone_par_id(drones, identifiant):
    # TODO
    pass


def drones_actifs(drones):
    # TODO
    pass


def consommer_batterie(drone, cout=1):
    # TODO
    pass


# Tests exercice 4
if __name__ == "__main__":
    drones = initialiser_drones(4)

    d = drone_par_id(drones, "D2")
    print(d["id"])   # D2
    print(drone_par_id(drones, "D9"))  # None

    print(len(drones_actifs(drones)))  # 4
    drones["D3"]["hors_service"] = True
    print(len(drones_actifs(drones)))  # 3

    drone = drones["D1"]
    for _ in range(10):
        consommer_batterie(drone)
    print(drone["batterie"])     # 0
    print(drone["hors_service"]) # True


# -----------------------------------------------------------------------------
# EXERCICE 5 — Résumé tableau de bord
# -----------------------------------------------------------------------------
# Écris : afficher_tableau_drones(drones)
# Affiche un tableau aligné pour tous les drones :
#
#   ID    Col  Lig  Bat    Surv
#   D1    0    5    9/20   —
#   D2    1    0    10/20  —
#   D3    2    0    0/20   —  HS
#
# Utilise f-strings avec :<N et :>N pour l'alignement.
# Ajoute " HS" à la fin si le drone est hors service.
# -----------------------------------------------------------------------------

def afficher_tableau_drones(drones):
    """
    Affiche le tableau de bord des drones avec colonnes alignées.
    """
    # TODO
    pass


# Tests exercice 5
if __name__ == "__main__":
    drones = initialiser_drones(3)
    drones["D1"]["batterie"] = 9
    drones["D3"]["batterie"] = 0
    drones["D3"]["hors_service"] = True
    drones["D2"]["survivant"] = "S2"
    afficher_tableau_drones(drones)
    # ID    Col  Lig  Bat    Surv
    # D1    0    0    9/20   —
    # D2    1    0    10/20  S2
    # D3    2    0    0/20   —  HS
