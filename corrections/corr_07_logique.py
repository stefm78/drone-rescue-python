# =============================================================================
# CORRECTION 07 — Logique de jeu
# Module correspondant : cours/07_logique_de_jeu.md
# Convention : colonne str 'A'..'L', ligne int 1-based 1..12
# =============================================================================

import random


# -----------------------------------------------------------------------------
# CORRECTION 0 — Helpers utilisés dans ce module
# -----------------------------------------------------------------------------
# Ces fonctions représentent la convention pédagogique du projet :
#   colonne : str lettre 'A'..'L'
#   ligne   : int 1-based 1..12
# Elles sont cohérentes avec cours/03 et cours/07.
# -----------------------------------------------------------------------------

def distance_chebyshev(col1: str, lig1: int, col2: str, lig2: int) -> int:
    """Distance de Chebyshev entre deux cases (diagonal = 1 pas)."""
    return max(abs(ord(col1) - ord(col2)), abs(lig1 - lig2))


def coord_valide(colonne: str, ligne: int, taille: int = 12) -> bool:
    """True si la coordonnée est dans la grille."""
    return 'A' <= colonne <= chr(ord('A') + taille - 1) and 1 <= ligne <= taille


# -----------------------------------------------------------------------------
# CORRECTION 1 — Valider un mouvement de drone
# -----------------------------------------------------------------------------
# Ordre des vérifications : déplacements restants → HS → bloqué → grille → distance.
# On retourne (False, motif) dès qu'une règle est violée, (True, "") si tout est OK.
# Le drone expose : colonne str, ligne int, batterie int, bloque int, survivant.
# -----------------------------------------------------------------------------

def valider_mouvement_drone(
    drone,
    col_cible: str, lig_cible: int,
    depl_restants: int,
    taille: int = 12
) -> tuple:
    """
    Valide le déplacement du drone vers (col_cible, lig_cible).
    Retourne (bool, message_erreur).
    """
    if depl_restants <= 0:
        return False, 'plus de déplacements ce tour'
    if drone.batterie == 0:
        return False, 'drone HS'
    if drone.bloque > 0:
        return False, f'drone bloqué ({drone.bloque} tours restants)'
    if not coord_valide(col_cible, lig_cible, taille):
        return False, 'case hors grille'
    if distance_chebyshev(drone.colonne, drone.ligne, col_cible, lig_cible) != 1:
        return False, 'distance invalide (> 1 case)'
    return True, ''


# Tests
if __name__ == '__main__':
    class DroneFictif:
        colonne = 'B'; ligne = 3; batterie = 8; bloque = 0; survivant = None

    d = DroneFictif()
    print(valider_mouvement_drone(d, 'C', 3, 3))   # (True, '')
    print(valider_mouvement_drone(d, 'D', 5, 3))   # (False, 'distance invalide...')
    print(valider_mouvement_drone(d, 'C', 3, 0))   # (False, 'plus de déplacements...')
    d.batterie = 0
    print(valider_mouvement_drone(d, 'C', 3, 3))   # (False, 'drone HS')


# -----------------------------------------------------------------------------
# CORRECTION 2 — Exécuter un mouvement (collecte, livraison, blocage)
# -----------------------------------------------------------------------------
# Séquence : déplacer → consommer batterie → vérifier tempête → survivant → hôpital.
# On retourne une liste d'événements (tuples) pour que la vue les affiche.
# Jamais de print() ici : la logique ne gère pas l'affichage.
# -----------------------------------------------------------------------------

def executer_mouvement(drone, col_cible: str, lig_cible: int, etat) -> list:
    """
    Déplace le drone (mouvement déjà validé), applique les effets.
    etat : objet avec .tempetes, .survivants, .hopital (colonne+ligne), .score
    Retourne la liste des événements survenus.
    """
    evenements = []
    drone.colonne = col_cible
    drone.ligne   = lig_cible

    # Tempête sur la case d'arrivée ? → blocage, pas de consommation batterie
    tempete = next(
        (t for t in etat.tempetes if t.colonne == col_cible and t.ligne == lig_cible),
        None
    )
    if tempete:
        drone.bloque = 2
        evenements.append(('BLOQUE', drone.identifiant, tempete.identifiant))
    else:
        drone.batterie = max(0, drone.batterie - 1)

    # Survivant libre sur la case ? → chargement automatique
    surv = next(
        (s for s in etat.survivants
         if s.etat == 'en_attente' and s.colonne == col_cible and s.ligne == lig_cible),
        None
    )
    if surv and drone.survivant is None:
        drone.survivant = surv
        surv.etat = 'porte'
        evenements.append(('CHARGE', drone.identifiant, surv.identifiant))

    # Hôpital + drone porte un survivant → livraison + recharge
    if (col_cible == etat.hopital.colonne and lig_cible == etat.hopital.ligne
            and drone.survivant):
        s = drone.survivant
        s.etat = 'sauve'
        drone.survivant = None
        etat.score += 1
        drone.batterie = drone.batterie_max
        evenements.append(('LIVRAISON', drone.identifiant, s.identifiant))

    return evenements


# -----------------------------------------------------------------------------
# CORRECTION 3 — Propagation d'une tempête
# -----------------------------------------------------------------------------
# 4 directions orthogonales. On filtre hors grille et cases protégées.
# Chaque voisin éligible est transformé en X avec probabilité proba.
# Convention : tempête.colonne str, tempête.ligne int.
# -----------------------------------------------------------------------------

def propager_tempete(tempete, etat, proba: float = 0.3) -> list:
    """
    Propage la tempête orthogonalement.
    Retourne la liste des tuples (colonne, ligne) nouvellement affectés.
    """
    nouvelles = []
    COLS = [chr(ord('A') + i) for i in range(12)]
    i_col = ord(tempete.colonne) - ord('A')

    for dcol, dlig in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nc = i_col + dcol
        nl = tempete.ligne + dlig
        if not (0 <= nc < 12 and 1 <= nl <= 12):
            continue
        col_v = COLS[nc]
        # Case protégée : hôpital
        if col_v == etat.hopital.colonne and nl == etat.hopital.ligne:
            continue
        if random.random() < proba:
            nouvelles.append((col_v, nl))

    return nouvelles


# Tests (proba=1.0 pour résultat déterministe)
if __name__ == '__main__':
    class Hopital:
        colonne = 'A'; ligne = 12

    class Tempete:
        identifiant = 'T1'; colonne = 'F'; ligne = 6

    class EtatSimple:
        tempetes   = []
        survivants = []
        hopital    = Hopital()
        score      = 0

    t = Tempete()
    e = EtatSimple()
    nouvelles = propager_tempete(t, e, proba=1.0)
    print(sorted(nouvelles))  # [('E',6), ('F',5), ('F',7), ('G',6)]


# -----------------------------------------------------------------------------
# CORRECTION 4 — Vérifier la fin de partie
# -----------------------------------------------------------------------------
# Ordre de priorité : VICTOIRE → DEFAITE_DRONES → DEFAITE_TOURS → EN_COURS.
# drone.batterie int, drone.survivant : None ou objet.
# -----------------------------------------------------------------------------

def verifier_fin_partie(
    tour_actuel: int, tour_max: int,
    drones: list, nb_survivants_restants: int
) -> str:
    """
    Retourne : 'VICTOIRE', 'DEFAITE_TOURS', 'DEFAITE_DRONES', ou 'EN_COURS'.
    """
    if nb_survivants_restants == 0:
        return 'VICTOIRE'
    if all(d.batterie == 0 for d in drones):
        return 'DEFAITE_DRONES'
    if tour_actuel >= tour_max:
        return 'DEFAITE_TOURS'
    return 'EN_COURS'


# Tests
if __name__ == '__main__':
    class DS:
        def __init__(self, bat): self.batterie = bat

    drones_ok = [DS(10), DS(5), DS(0)]
    print(verifier_fin_partie(5,  20, drones_ok, 3))   # EN_COURS
    print(verifier_fin_partie(5,  20, drones_ok, 0))   # VICTOIRE
    print(verifier_fin_partie(20, 20, drones_ok, 3))   # DEFAITE_TOURS
    print(verifier_fin_partie(5,  20, [DS(0), DS(0)], 3))  # DEFAITE_DRONES
