# =============================================================================
# EXERCICE 07 — Logique de jeu
# Module correspondant : cours/07_logique_de_jeu.md
# =============================================================================
# Objectifs :
#   - Valider et exécuter les déplacements selon les règles du jeu
#   - Gérer la collecte et la livraison des survivants
#   - Implémenter la propagation des tempêtes
#   - Vérifier les conditions de fin de partie
# =============================================================================

# On réutilise les classes simplifiées ci-dessous pour les tests

class Pos:
    """Position simplifiée pour les exercices."""
    def __init__(self, col, lig):
        self.col = col
        self.lig = lig
    def __str__(self):
        return f"{self.col}{self.lig}"
    def dist(self, autre):
        return max(abs(ord(self.col)-ord(autre.col)), abs(self.lig-autre.lig))
    def __eq__(self, autre):
        return self.col == autre.col and self.lig == autre.lig


# -----------------------------------------------------------------------------
# EXERCICE 1 — Valider un mouvement de drone
# -----------------------------------------------------------------------------
# Règles à vérifier :
#   1. La distance de Chebyshev entre départ et arrivée doit être == 1
#   2. Le drone ne doit pas être HS (batterie == 0)
#   3. Le drone ne doit pas être bloqué (blocage > 0)
#   4. La case cible ne doit pas être un bâtiment ('B')
#   5. Le drone doit avoir encore des déplacements restants ce tour
#
# Écris : valider_mouvement_drone(drone, cible_pos, grille, depl_restants)
#   → retourne (True, "") si valide
#   → retourne (False, "motif_erreur") sinon
# -----------------------------------------------------------------------------

def valider_mouvement_drone(drone, cible_pos, grille, depl_restants):
    """
    Valide le mouvement d'un drone vers cible_pos.
    grille est un dict {"A1": ".", "B2": "B", ...} pour simplifier.
    Retourne (bool, message_erreur).
    """
    # TODO
    pass


# Tests exercice 1
if __name__ == "__main__":
    # Drone fictif
    class DroneFictif:
        def __init__(self):
            self.position = Pos("B", 3)
            self.batterie = 8
            self.blocage = 0

    grille_test = {"C3": ".", "B4": "B", "C4": "."}
    d = DroneFictif()

    ok, msg = valider_mouvement_drone(d, Pos("C", 3), grille_test, 3)
    print(ok, msg)    # True, ""

    ok, msg = valider_mouvement_drone(d, Pos("B", 4), grille_test, 3)
    print(ok, msg)    # False, "bâtiment"

    ok, msg = valider_mouvement_drone(d, Pos("D", 5), grille_test, 3)
    print(ok, msg)    # False, "distance > 1"


# -----------------------------------------------------------------------------
# EXERCICE 2 — Collecter et livrer un survivant
# -----------------------------------------------------------------------------
# Règles :
#   - Si le drone arrive sur une case avec un survivant ("S") → collecte
#   - Si le drone arrive sur l'hôpital ("H") avec un survivant → livraison
#   - Un drone ne peut transporter qu'un survivant à la fois
#
# Écris : executer_mouvement(drone, cible_pos, grille, score)
#   → déplace le drone
#   → gère la collecte/livraison
#   → consomme la batterie
#   → retourne (nouveau_score, evenement)
#     evenement : "", "COLLECTE", "LIVRAISON +1pt", "RECHARGE"
# -----------------------------------------------------------------------------

def executer_mouvement(drone, cible_pos, grille, score):
    """
    Exécute le déplacement du drone et gère collecte/livraison.
    Modifie drone et grille en place.
    Retourne (nouveau_score, evenement_str).
    """
    # TODO
    pass


# Tests exercice 2
if __name__ == "__main__":
    class DroneFictif2:
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
    print(grille2.get("C3"))   # . (case vidée)


# -----------------------------------------------------------------------------
# EXERCICE 3 — Propagation d'une tempête
# -----------------------------------------------------------------------------
# Règles de propagation des zones X :
#   - Se propage sur les 4 cases adjacentes (haut/bas/gauche/droite, PAS diagonal)
#   - Ne se propage pas sur : bâtiment (B), hôpital (H), survivant (S)
#   - Probabilité de propagation paramétrable (ex: 0.3)
#   - Se déclenche tous les 2 tours
#
# Écris : propager_tempete(grille, tempete_pos, proba=0.3, taille=12)
#   → retourne la liste des nouvelles cases X créées
#   → modifie la grille en place pour les cases effectivement propagées
#   → utilise random.random() < proba pour chaque case candidate
# -----------------------------------------------------------------------------

import random

def propager_tempete(grille, tempete_pos, proba=0.3, taille=12):
    """
    Propage une zone X depuis tempete_pos vers les 4 cases orthogonales.
    Retourne la liste des nouvelles positions X créées.
    """
    # TODO
    # 1. Calculer les 4 voisins orthogonaux (haut, bas, gauche, droite)
    # 2. Filtrer les cases invalides (hors grille, B, H, S)
    # 3. Pour chaque case valide, tirer au sort selon proba
    # 4. Marquer la grille et retourner la liste
    pass


# Tests exercice 3 (résultats aléatoires — vérifier absence d'erreur)
if __name__ == "__main__":
    random.seed(42)
    grille3 = {"F6": "X", "E6": ".", "G6": ".", "F5": "B", "F7": "."}
    nouvelles = propager_tempete(grille3, Pos("F", 6), proba=1.0)  # proba=1 = toujours
    print(nouvelles)  # toutes les cases valides autour de F6 (E6, G6, F7 — pas F5=B)
    print(grille3)    # E6, G6, F7 passées à X


# -----------------------------------------------------------------------------
# EXERCICE 4 — Vérifier la fin de partie
# -----------------------------------------------------------------------------
# La partie se termine par :
#   VICTOIRE : tous les survivants ont été livrés (nb_survivants_restants == 0)
#   DÉFAITE  : tour max atteint OU tous les drones sont HS
#
# Écris : verifier_fin_partie(tour_actuel, tour_max, drones, nb_survivants_restants)
#   → retourne "VICTOIRE", "DEFAITE_TOURS", "DEFAITE_DRONES", ou "EN_COURS"
# -----------------------------------------------------------------------------

def verifier_fin_partie(tour_actuel, tour_max, drones, nb_survivants_restants):
    """
    Détermine l'état de la partie.
    drones : liste d'objets avec attribut batterie.
    """
    # TODO
    pass


# Tests exercice 4
if __name__ == "__main__":
    class DroneSimple:
        def __init__(self, bat): self.batterie = bat

    drones_ok = [DroneSimple(10), DroneSimple(5), DroneSimple(0)]
    print(verifier_fin_partie(5, 20, drones_ok, 3))    # EN_COURS
    print(verifier_fin_partie(5, 20, drones_ok, 0))    # VICTOIRE
    print(verifier_fin_partie(20, 20, drones_ok, 3))   # DEFAITE_TOURS
    drones_hs = [DroneSimple(0), DroneSimple(0)]
    print(verifier_fin_partie(5, 20, drones_hs, 3))    # DEFAITE_DRONES
