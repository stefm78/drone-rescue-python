# =============================================================================
# CORRECTION 07 — Logique de jeu
# Module correspondant : cours/07_logique_de_jeu.md
# =============================================================================

import random


# Classe Pos réutilisée depuis l'exercice (simplifiée pour les tests)
class Pos:
    def __init__(self, col, lig):
        self.col = col
        self.lig = lig
    def __str__(self):
        return f"{self.col}{self.lig}"
    def dist(self, autre):
        return max(abs(ord(self.col) - ord(autre.col)), abs(self.lig - autre.lig))
    def __eq__(self, autre):
        return self.col == autre.col and self.lig == autre.lig


# -----------------------------------------------------------------------------
# CORRECTION 1 — Valider un mouvement de drone
# -----------------------------------------------------------------------------
# Ordre des vérifications : déplacements restants → HS → bloqué → distance → bâtiment.
# On retourne (False, motif) dès qu'une règle est violée, (True, "") si tout est OK.
# -----------------------------------------------------------------------------

def valider_mouvement_drone(drone, cible_pos, grille, depl_restants):
    """
    Valide le déplacement du drone vers cible_pos.
    grille : dict {"A1": ".", "B2": "B", ...}
    Retourne (bool, message_erreur).
    """
    if depl_restants <= 0:
        return False, "plus de déplacements ce tour"
    if drone.batterie == 0:
        return False, "drone HS"
    if drone.blocage > 0:
        return False, "drone bloqué"
    if drone.position.dist(cible_pos) != 1:
        return False, "distance > 1"
    cle = f"{cible_pos.col}{cible_pos.lig}"
    if grille.get(cle) == "B":
        return False, "bâtiment"
    return True, ""


# Tests
if __name__ == "__main__":
    class DroneFictif:
        def __init__(self):
            self.position = Pos("B", 3)
            self.batterie = 8
            self.blocage = 0

    grille_test = {"C3": ".", "B4": "B", "C4": "."}
    d = DroneFictif()

    ok, msg = valider_mouvement_drone(d, Pos("C", 3), grille_test, 3)
    print(ok, msg)    # True ""

    ok, msg = valider_mouvement_drone(d, Pos("B", 4), grille_test, 3)
    print(ok, msg)    # False bâtiment

    ok, msg = valider_mouvement_drone(d, Pos("D", 5), grille_test, 3)
    print(ok, msg)    # False distance > 1


# -----------------------------------------------------------------------------
# CORRECTION 2 — Collecter et livrer un survivant
# -----------------------------------------------------------------------------
# Séquence :
#   1. Mettre à jour la position du drone
#   2. Consommer la batterie
#   3. Si la case d'arrivée est "S" et que le drone est libre → COLLECTE
#   4. Si la case d'arrivée est "H" et que le drone porte un survivant → LIVRAISON
#   5. Si la case d'arrivée est "H" sans survivant → RECHARGE (batterie max)
# -----------------------------------------------------------------------------

def executer_mouvement(drone, cible_pos, grille, score):
    """
    Déplace le drone, gère collecte/livraison/recharge.
    Retourne (nouveau_score, evenement_str).
    """
    ancien_pos_key = f"{drone.position.col}{drone.position.lig}"
    nouvelle_pos_key = f"{cible_pos.col}{cible_pos.lig}"

    # Libérer l'ancienne case (si occupée par ce drone uniquement)
    if grille.get(ancien_pos_key, ".").startswith("D"):
        grille[ancien_pos_key] = "."

    # Déplacer le drone
    drone.position = cible_pos
    drone.consommer_batterie()

    evenement = ""
    case_cible = grille.get(nouvelle_pos_key, ".")

    if case_cible == "S" and drone.survivant is None:
        # Collecte d'un survivant
        drone.survivant = "S"  # dans le vrai jeu : identifiant précis
        grille[nouvelle_pos_key] = drone.identifiant if hasattr(drone, 'identifiant') else "D"
        evenement = "COLLECTE"

    elif case_cible == "H":
        if drone.survivant is not None:
            # Livraison à l'hôpital
            score += 1
            drone.survivant = None
            evenement = "LIVRAISON +1pt"
        else:
            # Recharge à l'hôpital
            drone.batterie = drone.batterie_max if hasattr(drone, 'batterie_max') else drone.batterie
            evenement = "RECHARGE"
    else:
        grille[nouvelle_pos_key] = drone.identifiant if hasattr(drone, 'identifiant') else "D"

    return score, evenement


# Tests
if __name__ == "__main__":
    class DroneFictif2:
        identifiant = "D1"
        batterie_max = 20
        def __init__(self):
            self.position = Pos("B", 3)
            self.batterie = 8
            self.survivant = None
        def consommer_batterie(self):
            self.batterie = max(0, self.batterie - 1)

    grille2 = {"C3": "S", "A12": "H"}
    d2 = DroneFictif2()

    score, evt = executer_mouvement(d2, Pos("C", 3), grille2, 0)
    print(score, evt)          # 0 COLLECTE
    print(d2.survivant)        # S
    print(grille2.get("C3"))   # D1 (case maintenant occupée par le drone)


# -----------------------------------------------------------------------------
# CORRECTION 3 — Propagation d'une tempête
# -----------------------------------------------------------------------------
# On calcule les 4 voisins orthogonaux (Δcol ou Δlig = ±1, pas les deux).
# On filtre les cases hors grille et les cases protégées (B, H, S).
# Pour chaque candidat, random.random() < proba décide si la propagation a lieu.
# -----------------------------------------------------------------------------

def propager_tempete(grille, tempete_pos, proba=0.3, taille=12):
    """
    Propage une zone X depuis tempete_pos (4 directions orthogonales).
    Retourne la liste des nouvelles positions X créées.
    """
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # gauche, droite, haut, bas
    nouvelles_zones = []

    col_idx = ord(tempete_pos.col) - ord('A')
    lig_idx = tempete_pos.lig

    for dcol, dlig in directions:
        nc = col_idx + dcol
        nl = lig_idx + dlig
        if not (0 <= nc < taille and 1 <= nl <= taille):
            continue  # hors grille
        cle = f"{chr(65 + nc)}{nl}"
        contenu = grille.get(cle, ".")
        if contenu in ("B", "H", "S"):
            continue  # case protégée
        if random.random() < proba:
            grille[cle] = "X"
            nouvelles_zones.append(cle)

    return nouvelles_zones


# Tests (résultats aléatoires — proba=1.0 pour test déterministe)
if __name__ == "__main__":
    random.seed(42)
    grille3 = {"F6": "X", "E6": ".", "G6": ".", "F5": "B", "F7": "."}
    nouvelles = propager_tempete(grille3, Pos("F", 6), proba=1.0)
    print(sorted(nouvelles))  # ['E6', 'F7', 'G6']  (F5 est un bâtiment)
    print({k: v for k, v in grille3.items() if v == "X"})


# -----------------------------------------------------------------------------
# CORRECTION 4 — Vérifier la fin de partie
# -----------------------------------------------------------------------------
# Ordre de priorité : VICTOIRE (cas le plus favorable) → DEFAITE_DRONES
# → DEFAITE_TOURS → EN_COURS.
# -----------------------------------------------------------------------------

def verifier_fin_partie(tour_actuel, tour_max, drones, nb_survivants_restants):
    """
    Retourne l'état de la partie :
    "VICTOIRE", "DEFAITE_TOURS", "DEFAITE_DRONES", ou "EN_COURS".
    """
    if nb_survivants_restants == 0:
        return "VICTOIRE"
    if tour_actuel >= tour_max:
        return "DEFAITE_TOURS"
    if all(d.batterie == 0 for d in drones):
        return "DEFAITE_DRONES"
    return "EN_COURS"


# Tests
if __name__ == "__main__":
    class DroneSimple:
        def __init__(self, bat): self.batterie = bat

    drones_ok = [DroneSimple(10), DroneSimple(5), DroneSimple(0)]
    print(verifier_fin_partie(5, 20, drones_ok, 3))    # EN_COURS
    print(verifier_fin_partie(5, 20, drones_ok, 0))    # VICTOIRE
    print(verifier_fin_partie(20, 20, drones_ok, 3))   # DEFAITE_TOURS
    drones_hs = [DroneSimple(0), DroneSimple(0)]
    print(verifier_fin_partie(5, 20, drones_hs, 3))    # DEFAITE_DRONES
