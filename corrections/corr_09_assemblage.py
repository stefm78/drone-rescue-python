# =============================================================================
# CORRECTION 09 — Assemblage final
# =============================================================================
# Chaque solution inclut des assert exécutables.
# Lance avec : python corr_09_assemblage.py
# =============================================================================


LETTRES = list("ABCDEFGHIJ")
GRILLE_TAILLE    = 5
COUT_TRANSPORT   = 2
COUT_ZONE_X      = 2
RECHARGE_HOPITAL = 3
NB_TOURS_MAX     = 10


# ---------------------------------------------------------------------------
# Fonctions de création (reprises de l'exercice)
# ---------------------------------------------------------------------------

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
    """Crée un état de jeu minimal 5x5 pour les tests."""
    hopital    = (4, 4)
    drones     = {
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


def distance_chebyshev(c1, l1, c2, l2):
    """Distance de Chebyshev entre deux cases."""
    return max(abs(c2 - c1), abs(l2 - l1))


def case_valide(pos):
    """True si (col, lig) est dans la grille."""
    col, lig = pos
    return 0 <= col < GRILLE_TAILLE and 0 <= lig < GRILLE_TAILLE


def pos_str(col, lig):
    """Convertit (col, lig) 0-based en notation affichage 'B3'."""
    return f"{LETTRES[col]}{lig + 1}"


# ---------------------------------------------------------------------------
# A1 — Reconstruction de la grille
# ---------------------------------------------------------------------------

def reconstruire_grille(etat):
    """Reconstruit la grille depuis l'état courant."""
    g = etat["grille"]
    # Remettre toutes les cases à '.'
    for lig in range(GRILLE_TAILLE):
        for col in range(GRILLE_TAILLE):
            g[lig][col] = "."
    # Zones X
    for pos in etat["zones_x"]:
        g[pos[1]][pos[0]] = "X"
    # Survivants en attente
    for s in etat["survivants"].values():
        if s["etat"] == "en_attente":
            g[s["lig"]][s["col"]] = "S"
    # Drones actifs
    for d in etat["drones"].values():
        if not d["hors_service"]:
            g[d["lig"]][d["col"]] = "D"
    # Hôpital (prioritaire sur les entités)
    hcol, hlig = etat["hopital"]
    g[hlig][hcol] = "H"
    # Bâtiments (priorité maximale)
    for pos in etat["batiments"]:
        g[pos[1]][pos[0]] = "B"


assert_etat = initialiser_etat_simple()
reconstruire_grille(assert_etat)
assert assert_etat["grille"][0][0] == "D"
assert assert_etat["grille"][1][2] == "D"
assert assert_etat["grille"][2][1] == "S"
assert assert_etat["grille"][3][3] == "X"
assert assert_etat["grille"][4][4] == "H"
print("A1 OK")


# ---------------------------------------------------------------------------
# B1 — Afficher la grille
# ---------------------------------------------------------------------------

def afficher_grille_simple(etat):
    """Affiche la grille avec en-tête de colonnes et numéros de lignes."""
    taille = len(etat["grille"])
    print("      " + "  ".join(LETTRES[:taille]))
    print("    " + "---" * taille)
    for lig_idx, ligne in enumerate(etat["grille"]):
        num   = str(lig_idx + 1).rjust(2)
        cases = "  ".join(ligne)
        print(f"{num} |  {cases}")


assert_etat2 = initialiser_etat_simple()
reconstruire_grille(assert_etat2)
afficher_grille_simple(assert_etat2)  # affichage visuel
print("B1 OK")


# ---------------------------------------------------------------------------
# B2 — Ligne de statut d'un drone
# ---------------------------------------------------------------------------

def statut_drone(drone):
    """Retourne la ligne de statut d'un drone."""
    pos_affichage = pos_str(drone["col"], drone["lig"])
    bat    = f"{drone['batterie']}/{drone['batterie_max']}"
    surv   = drone["survivant"] if drone["survivant"] else "--"
    etat_d = "HS" if drone["hors_service"] else "OK"
    # Choix d'alignement : id(4), pos(6), bat(7), surv(6), état
    return f"{drone['id']:<4} {pos_affichage:<6} {bat:<7} {surv:<6} {etat_d}"


d_test = creer_drone("D1", 0, 0)
ligne_test = statut_drone(d_test)
assert "D1" in ligne_test
assert "10/20" in ligne_test
assert "OK" in ligne_test
print("B2 OK")


# ---------------------------------------------------------------------------
# C1 — Calcul du coût de déplacement
# ---------------------------------------------------------------------------

def calculer_cout(drone, cible, zones_x, hopital):
    """
    Retourne le delta batterie net d'un déplacement.
    Négatif = perte de batterie, positif = gain.
    """
    # Coût de base
    cout = COUT_TRANSPORT if drone["survivant"] else 1
    # Supplément zone X
    if cible in zones_x:
        cout += COUT_ZONE_X
    delta = -cout
    # Recharge si arrivée à l'hôpital
    if cible == hopital:
        delta += RECHARGE_HOPITAL
    return delta


d_c1 = creer_drone("D1", 0, 0)
zones_c1 = {(2, 2)}
hop_c1   = (4, 4)
assert calculer_cout(d_c1, (1, 1), zones_c1, hop_c1) == -1
assert calculer_cout(d_c1, (2, 2), zones_c1, hop_c1) == -3
d_c1["survivant"] = "S1"
assert calculer_cout(d_c1, (1, 1), zones_c1, hop_c1) == -2
assert calculer_cout(d_c1, (2, 2), zones_c1, hop_c1) == -4
d_c1["survivant"] = None
assert calculer_cout(d_c1, (4, 4), zones_c1, hop_c1) == +2  # -1 + 3
print("C1 OK")


# ---------------------------------------------------------------------------
# Helpers D1
# ---------------------------------------------------------------------------

def survivant_sur_case(etat, pos):
    """Retourne le dict du survivant en attente sur la case, ou None."""
    for s in etat["survivants"].values():
        if s["etat"] == "en_attente" and (s["col"], s["lig"]) == pos:
            return s
    return None


# ---------------------------------------------------------------------------
# D1 — Flux d'un tour complet
# ---------------------------------------------------------------------------

def jouer_un_tour(etat, mouvements_j1):
    """
    Joue un tour avec la liste de mouvements J1.
    mouvements_j1 : [(drone_id, (col_cible, lig_cible)), ...]
    """
    hopital = etat["hopital"]

    for did, cible in mouvements_j1:
        drone = etat["drones"].get(did)
        if drone is None or drone["hors_service"]:
            continue

        # Validation minimale
        if distance_chebyshev(drone["col"], drone["lig"], cible[0], cible[1]) > 1:
            etat["historique"].append(f"T{etat['tour']:02d}  {did}  REFUSÉ (trop loin)")
            continue
        if drone["batterie"] <= 0:
            etat["historique"].append(f"T{etat['tour']:02d}  {did}  REFUSÉ (batterie vide)")
            continue

        depart = (drone["col"], drone["lig"])
        bat_avant = drone["batterie"]
        evenement = ""

        # Appliquer le coût
        delta = calculer_cout(drone, cible, etat["zones_x"], hopital)
        drone["batterie"] = max(0, drone["batterie"] + delta)
        drone["col"], drone["lig"] = cible

        # Livraison à l'hôpital
        if cible == hopital and drone["survivant"]:
            s = etat["survivants"][drone["survivant"]]
            s["etat"] = "sauve"
            etat["score"] += 1
            evenement = f"LIVRAISON {s['id']} +1pt"
            drone["survivant"] = None
        else:
            # Prise d'un survivant
            s = survivant_sur_case(etat, cible)
            if s and drone["survivant"] is None:
                drone["survivant"] = s["id"]
                s["etat"] = "embarque"
                evenement = f"PRISE {s['id']}"

        # Hors service ?
        if drone["batterie"] <= 0:
            drone["hors_service"] = True
            evenement = "HS"

        # Log
        ligne = (
            f"T{etat['tour']:02d}  {did}  "
            f"{pos_str(*depart)}→{pos_str(*cible)}  "
            f"bat:{bat_avant}→{drone['batterie']}"
        )
        if evenement:
            ligne += f"  {evenement}"
        etat["historique"].append(ligne)

    etat["tour"] += 1
    return etat


etat_d1 = initialiser_etat_simple()
mouvements = [("D1", (1, 1)), ("D2", (1, 2))]
etat_d1 = jouer_un_tour(etat_d1, mouvements)
assert etat_d1["drones"]["D1"]["col"] == 1
assert etat_d1["drones"]["D1"]["lig"] == 1
assert etat_d1["drones"]["D2"]["survivant"] == "S1"
assert etat_d1["survivants"]["S1"]["etat"] == "embarque"
assert etat_d1["tour"] == 2
print("D1 OK")


# ---------------------------------------------------------------------------
# E1 — Vérification de fin de partie
# ---------------------------------------------------------------------------

def verifier_fin_partie(etat):
    """Retourne (termine, issue) : issue = 'victoire', 'defaite' ou None."""
    # Victoire : tous les survivants sauvés
    if all(s["etat"] == "sauve" for s in etat["survivants"].values()):
        return True, "victoire"
    # Défaite : tous les drones HS ou tours épuisés
    if etat["tour"] > NB_TOURS_MAX:
        return True, "defaite"
    if all(d["hors_service"] for d in etat["drones"].values()):
        return True, "defaite"
    return False, None


etat_e1 = initialiser_etat_simple()
assert verifier_fin_partie(etat_e1) == (False, None)
etat_e1["survivants"]["S1"]["etat"] = "sauve"
assert verifier_fin_partie(etat_e1) == (True, "victoire")

etat_e2 = initialiser_etat_simple()
etat_e2["tour"] = NB_TOURS_MAX + 1
assert verifier_fin_partie(etat_e2) == (True, "defaite")

etat_e3 = initialiser_etat_simple()
for d in etat_e3["drones"].values():
    d["hors_service"] = True
assert verifier_fin_partie(etat_e3) == (True, "defaite")
print("E1 OK")

print()
print("=== Tous les tests corr_09 passent ===")
