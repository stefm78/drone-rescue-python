# =============================================================================
# EXERCICE 09 — Assemblage final
# Module correspondant : cours/09_assemblage_final.md
# =============================================================================
# Objectifs :
#   - Comprendre les dépendances entre les modules du projet
#   - Intégrer logique.py, affichage.py, logger.py dans une mini boucle
#   - Vérifier que le flux d'un tour complet fonctionne de bout en bout
#   - Identifier et corriger les erreurs d'import circulaire
# =============================================================================
# Cet exercice est AUTOPORTANT : il ne dépend PAS des fichiers jeu/.
# Toutes les fonctions nécessaires sont re-définies ici en version simplifiée.
# =============================================================================


LETTRES = list("ABCDEFGHIJ")
GRILLE_TAILLE   = 5
COUT_TRANSPORT   = 2
COUT_ZONE_X      = 2
RECHARGE_HOPITAL = 3
NB_TOURS_MAX     = 10


# =============================================================================
# PARTIE A — Fonctions de création (logique)
# =============================================================================

def creer_drone(identifiant, col, lig, batterie_max=20):
    """Retourne un dictionnaire représentant un drone."""
    return {
        "id"          : identifiant,
        "col"         : col,
        "lig"         : lig,
        "batterie"    : batterie_max // 2,
        "batterie_max": batterie_max,
        "survivant"   : None,
        "bloque"      : 0,
        "hors_service": False,
    }


def creer_survivant(identifiant, col, lig):
    """Retourne un dictionnaire représentant un survivant."""
    return {"id": identifiant, "col": col, "lig": lig, "etat": "en_attente"}


def initialiser_etat_simple():
    """
    Crée un état de jeu minimal (grille 5x5) pour les tests.
    Hôpital en (4,4), 2 drones, 1 survivant, 1 zone X.
    """
    hopital   = (4, 4)
    drones    = {
        "D1": creer_drone("D1", 0, 0),
        "D2": creer_drone("D2", 2, 1),
    }
    survivants = {"S1": creer_survivant("S1", 1, 2)}
    zones_x    = {(3, 3)}
    grille     = [["." for _ in range(GRILLE_TAILLE)] for _ in range(GRILLE_TAILLE)]
    return {
        "tour"        : 1,
        "score"       : 0,
        "partie_finie": False,
        "victoire"    : False,
        "grille"      : grille,
        "hopital"     : hopital,
        "batiments"   : [],
        "drones"      : drones,
        "tempetes"    : {},
        "survivants"  : survivants,
        "zones_x"     : zones_x,
        "historique"  : [],
    }


# -----------------------------------------------------------------------------
# EXERCICE A1 — Reconstruction de la grille
# -----------------------------------------------------------------------------
# Écris `reconstruire_grille(etat)` qui met à jour `etat["grille"]` depuis
# l'état courant (drones, survivants, zones_x, hopital, batiments).
# Ordre de priorité (du moins au plus prioritaire) :
#   '.', 'X', 'S', 'D', 'H', 'B'
# -----------------------------------------------------------------------------

def reconstruire_grille(etat):
    """Reconstruit la grille depuis l'état courant."""
    # TODO
    pass


# Tests A1
if __name__ == "__main__":
    etat = initialiser_etat_simple()
    reconstruire_grille(etat)
    assert etat["grille"][0][0] == "D"   # D1 en col=0, lig=0
    assert etat["grille"][1][2] == "D"   # D2 en col=2, lig=1
    assert etat["grille"][2][1] == "S"   # S1 en col=1, lig=2
    assert etat["grille"][3][3] == "X"   # zone X en (3,3)
    assert etat["grille"][4][4] == "H"   # hôpital en (4,4)
    print("A1 OK")


# =============================================================================
# PARTIE B — Affichage (affichage)
# =============================================================================

def pos_str(col, lig):
    """Convertit (col, lig) 0-based en notation affichage 'B3'."""
    return f"{LETTRES[col]}{lig + 1}"


# -----------------------------------------------------------------------------
# EXERCICE B1 — Afficher la grille
# -----------------------------------------------------------------------------
# Écris `afficher_grille_simple(etat)` qui imprime la grille avec
# l'en-tête de colonnes (A B C ...) et les numéros de lignes (1 à N).
# Format :
#   "      A  B  C  D  E"
#   "    ---------------"
#   " 1 |  D  .  .  .  ."
#   " 2 |  .  .  D  .  ."
#   ...
# -----------------------------------------------------------------------------

def afficher_grille_simple(etat):
    """Affiche la grille avec coordonnées."""
    # TODO
    pass


# Tests B1
if __name__ == "__main__":
    etat = initialiser_etat_simple()
    reconstruire_grille(etat)
    afficher_grille_simple(etat)  # doit afficher sans erreur
    print("B1 OK")


# -----------------------------------------------------------------------------
# EXERCICE B2 — Ligne de statut d'un drone
# -----------------------------------------------------------------------------
# Écris `statut_drone(drone)` qui retourne une chaîne :
#   "D1  A1    10/20  --    OK"
#   "D2  C2    0/20   S1    HS"
# Format : id (4), pos (6), batterie (7), survivant (6), état
# -----------------------------------------------------------------------------

def statut_drone(drone):
    """Retourne la ligne de statut d'un drone."""
    # TODO
    pass


# Tests B2
if __name__ == "__main__":
    d = creer_drone("D1", 0, 0)
    ligne = statut_drone(d)
    assert "D1" in ligne
    assert "10/20" in ligne
    print("B2 OK")


# =============================================================================
# PARTIE C — Logique (règles du jeu)
# =============================================================================

def distance_chebyshev(c1, l1, c2, l2):
    """Distance de Chebyshev entre deux cases."""
    return max(abs(c2 - c1), abs(l2 - l1))


def case_valide(pos):
    """True si (col, lig) est dans la grille."""
    col, lig = pos
    return 0 <= col < GRILLE_TAILLE and 0 <= lig < GRILLE_TAILLE


# -----------------------------------------------------------------------------
# EXERCICE C1 — Calcul du coût de déplacement
# -----------------------------------------------------------------------------
# Règles officielles :
#   - déplacement normal          : -1
#   - transport d'un survivant    : -2
#   - entrée zone X (supplément)  : -2
#   - arrivée à l'hôpital         : +RECHARGE_HOPITAL (après coût)
# Écris `calculer_cout(drone, cible, zones_x, hopital)` qui retourne
# le delta batterie NET (peut être positif si hôpital + pas transport).
# -----------------------------------------------------------------------------

def calculer_cout(drone, cible, zones_x, hopital):
    """
    Retourne le delta batterie net d'un déplacement.
    Valeur négative = perte, valeur positive = gain.
    """
    # TODO
    pass


# Tests C1
if __name__ == "__main__":
    d = creer_drone("D1", 0, 0)
    zones = {(2, 2)}
    hop   = (4, 4)
    assert calculer_cout(d, (1, 1), zones, hop)  == -1   # dépl. normal
    assert calculer_cout(d, (2, 2), zones, hop)  == -3   # normal + zone X
    d["survivant"] = "S1"
    assert calculer_cout(d, (1, 1), zones, hop)  == -2   # transport
    assert calculer_cout(d, (2, 2), zones, hop)  == -4   # transport + zone X
    d["survivant"] = None
    assert calculer_cout(d, (4, 4), zones, hop)  == +2   # hôpital : -1 + 3
    print("C1 OK")


# =============================================================================
# PARTIE D — Mini boucle de jeu (assemblage)
# =============================================================================

# -----------------------------------------------------------------------------
# EXERCICE D1 — Flux d'un tour complet
# -----------------------------------------------------------------------------
# Écris `jouer_un_tour(etat, mouvements_j1)` qui :
#   1. Pour chaque (drone_id, cible) dans mouvements_j1 :
#      a. Valide le mouvement (distance ≤ 1, batterie > 0, hors_service=False)
#      b. Applique le coût de batterie
#      c. Si survivant sur la cible → l'embarquer (etat pour drone, 'embarque' pour survivant)
#      d. Si cible == hôpital et drone porte un survivant → livrer (+1 score,
#         etat survivant='sauve', drone['survivant']=None) + recharger
#      e. Ajoute une ligne dans etat["historique"]
#   2. Incrémente etat["tour"]
#   3. Retourne etat
#
# Pas besoin de gérer les tempêtes ni la propagation zones X ici.
# -----------------------------------------------------------------------------

def survivant_sur_case(etat, pos):
    """Retourne le dict du survivant en attente sur la case, ou None."""
    for s in etat["survivants"].values():
        if s["etat"] == "en_attente" and (s["col"], s["lig"]) == pos:
            return s
    return None


def jouer_un_tour(etat, mouvements_j1):
    """
    Joue un tour avec la liste de mouvements J1.
    mouvements_j1 : [(drone_id, (col_cible, lig_cible)), ...]
    Retourne etat mis à jour.
    """
    # TODO
    # Pour chaque (did, cible) :
    #   - vérifier distance_chebyshev <= 1
    #   - vérifier batterie > 0 et hors_service == False
    #   - appliquer calculer_cout
    #   - gérer prise et livraison survivant
    #   - ajouter ligne historique
    # Incrémenter tour
    pass


# Tests D1
if __name__ == "__main__":
    etat = initialiser_etat_simple()
    # D1 se déplace de (0,0) vers (1,1)
    # D2 se déplace de (2,1) vers (1,2) → prend S1
    mouvements = [("D1", (1, 1)), ("D2", (1, 2))]
    etat = jouer_un_tour(etat, mouvements)
    assert etat["drones"]["D1"]["col"] == 1
    assert etat["drones"]["D1"]["lig"] == 1
    assert etat["drones"]["D2"]["survivant"] == "S1"
    assert etat["survivants"]["S1"]["etat"] == "embarque"
    assert etat["tour"] == 2
    print("D1 OK")


# =============================================================================
# PARTIE E — Vérification de fin de partie
# =============================================================================

# -----------------------------------------------------------------------------
# EXERCICE E1 — verifier_fin_partie
# -----------------------------------------------------------------------------
# Écris `verifier_fin_partie(etat)` qui :
#   - retourne (True, "victoire") si tous les survivants sont 'sauve'
#   - retourne (True, "defaite")  si tous les drones sont hors_service
#                                  OU etat["tour"] > NB_TOURS_MAX
#   - retourne (False, None)      sinon
# -----------------------------------------------------------------------------

def verifier_fin_partie(etat):
    """Retourne (termine, issue) où issue est 'victoire', 'defaite' ou None."""
    # TODO
    pass


# Tests E1
if __name__ == "__main__":
    etat = initialiser_etat_simple()
    assert verifier_fin_partie(etat) == (False, None)   # partie en cours

    etat["survivants"]["S1"]["etat"] = "sauve"
    assert verifier_fin_partie(etat) == (True, "victoire")

    etat2 = initialiser_etat_simple()
    etat2["tour"] = NB_TOURS_MAX + 1
    assert verifier_fin_partie(etat2) == (True, "defaite")

    etat3 = initialiser_etat_simple()
    for d in etat3["drones"].values():
        d["hors_service"] = True
    assert verifier_fin_partie(etat3) == (True, "defaite")
    print("E1 OK")
