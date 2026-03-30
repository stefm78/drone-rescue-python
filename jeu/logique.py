# =============================================================================
# logique.py — Règles du jeu Drone Rescue
#
# Fonctions :
#   initialiser_partie()        -> EtatJeu
#   valider_mouvement()         -> (bool, str)
#   executer_mouvement()        -> str
#   propager_zones_x()          -> list[str]   (≠ tempêtes !)
#   deplacer_tempetes()         -> list[str]   (auto, IA)
#   appliquer_blocages()        -> None
#   verifier_fin_partie()       -> bool
#   recharger_drone()           -> str
#
# RÈGLES STRICTES :
#   - Tour Drone  : 3 déplacements max, 1 case/drone, chaque drone 1 fois max
#   - Tour Tempête: 2 déplacements manuels max, 1 case/tempête, chaque tempête 1 fois max
#   - Recharge hôpital : 1 seule fois par tour par drone
#   - Hôpital : aucun bâtiment ne peut être adjacent (8 cases)
#   - Propagation : les ZONES X se propagent depuis les zones X existantes
#     Les TEMPÊTES ne se propagent PAS — elles se déplacent d'elles-mêmes
#   - Déplacement auto des tempêtes (fin de tour) selon direction aléatoire
# =============================================================================

import random
from modeles import (
    EtatJeu, Position, Batiment, Hopital, Survivant, Drone, Tempete, Grille
)
from config import (
    GRILLE_TAILLE, NB_DRONES, NB_TEMPETES, NB_BATIMENTS, NB_SURVIVANTS,
    BATTERIE_MAX, BATTERIE_INIT, NB_ZONES_DANGER,
    MAX_DEPL_DRONE, MAX_DEPL_TEMPETE, NB_TOURS_MAX,
    PROBA_PROPAGATION, PROPAGATION_FREQUENCE,
    HOPITAL_COL, HOPITAL_LIG
)


# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------

def initialiser_partie() -> EtatJeu:
    """
    Crée et retourne un EtatJeu initialisé :
    - Grille vide
    - Hôpital placé en A12 (position fixe depuis config)
    - Bâtiments placés aléatoirement — JAMAIS adjacents à l'hôpital (8 cases)
    - Drones, Tempêtes, Survivants, Zones X aléatoires
    """
    etat = EtatJeu()
    occupees: set = set()

    pos_hopital = etat.hopital.position
    etat.grille.definir(pos_hopital, 'H')
    occupees.add(pos_hopital)

    # Bloquer les 8 cases adjacentes à l'hôpital pour les bâtiments
    cases_autour_hopital: set = set(pos_hopital.voisins_diag())

    for i in range(NB_BATIMENTS):
        pos = _position_aleatoire(occupees, interdites=cases_autour_hopital)
        if pos is None:
            break
        bat = Batiment(pos)
        etat.batiments.append(bat)
        etat.grille.definir(pos, 'B')
        occupees.add(pos)

    for i in range(1, NB_DRONES + 1):
        pos = _position_aleatoire(occupees)
        if pos is None:
            break
        drone = Drone(f"D{i}", pos)
        etat.drones.append(drone)
        etat.grille.definir(pos, 'D')
        occupees.add(pos)

    for i in range(1, NB_TEMPETES + 1):
        pos = _position_aleatoire(occupees)
        if pos is None:
            break
        tempete = Tempete(f"T{i}", pos)
        etat.tempetes.append(tempete)
        etat.grille.definir(pos, 'T')
        occupees.add(pos)

    for i in range(1, NB_SURVIVANTS + 1):
        pos = _position_aleatoire(occupees)
        if pos is None:
            break
        surv = Survivant(f"S{i}", pos)
        etat.survivants.append(surv)
        etat.grille.definir(pos, 'S')
        occupees.add(pos)

    for _ in range(NB_ZONES_DANGER):
        pos = _position_aleatoire(occupees)
        if pos is None:
            break
        etat.zones_x.add(pos)
        etat.grille.definir(pos, 'X')
        occupees.add(pos)

    return etat


def _position_aleatoire(occupees: set, interdites: set = None,
                        max_tentatives: int = 200) -> 'Position | None':
    """
    Retourne une position aléatoire libre dans la grille,
    en évitant `occupees` ET `interdites`.
    """
    interdit = (interdites or set()) | occupees
    for _ in range(max_tentatives):
        col = random.randint(0, GRILLE_TAILLE - 1)
        lig = random.randint(0, GRILLE_TAILLE - 1)
        pos = Position(col, lig)
        if pos not in interdit:
            return pos
    return None


# ---------------------------------------------------------------------------
# Validation d'un mouvement drone
# ---------------------------------------------------------------------------

def valider_mouvement(etat: EtatJeu, drone: Drone, cible: Position) -> tuple:
    """
    Vérifie si le drone peut se déplacer vers la cible.
    Retourne (True, "") si valide, (False, raison) sinon.
    """
    if drone.hors_service:
        return False, f"{drone.identifiant} est hors service (batterie à 0)"
    if drone.est_bloque():
        return False, f"{drone.identifiant} est bloqué ({drone.bloque} tour(s) restant(s))"
    if not cible.est_valide():
        return False, f"Position {cible} hors de la grille"
    if drone.position.distance_chebyshev(cible) > 1:
        return False, f"Max 1 case par déplacement"
    if etat.batiment_sur_case(cible):
        return False, f"Case {cible} bloquée par un bâtiment"
    if drone.batterie <= 0:
        return False, f"{drone.identifiant} n'a plus de batterie"
    return True, ""


def valider_mouvement_tempete(etat: EtatJeu, tempete: Tempete, cible: Position) -> tuple:
    """
    Vérifie si la tempête peut se déplacer vers la cible (déplacement manuel P2).
    """
    if not cible.est_valide():
        return False, f"Position {cible} hors de la grille"
    if tempete.position.distance_chebyshev(cible) > 1:
        return False, f"Max 1 case par déplacement"
    if cible == etat.hopital.position:
        return False, f"La tempête ne peut pas occuper l'hôpital"
    if etat.batiment_sur_case(cible):
        return False, f"Case {cible} bloquée par un bâtiment"
    return True, ""


# ---------------------------------------------------------------------------
# Exécution d'un mouvement drone
# ---------------------------------------------------------------------------

def executer_mouvement(etat: EtatJeu, drone: Drone, cible: Position,
                       drones_recharges_ce_tour: set) -> str:
    depart = Position(drone.position.col, drone.position.lig)

    tempete_sur_cible = etat.tempete_sur_case(cible)
    if tempete_sur_cible:
        drone.bloque = 2
        drone.position = cible
        _mettre_a_jour_grille(etat)
        evt = f"BLOQUÉ({tempete_sur_cible.identifiant})"
        return _format_log_condense(etat, drone.identifiant, depart, cible,
                                    drone.batterie, drone.batterie, evt)

    bat_avant = drone.batterie
    drone.position = cible
    drone.consommer_batterie(1)
    bat_apres = drone.batterie

    evenement = ""
    surv_id = drone.survivant.identifiant if drone.survivant else None

    if cible == etat.hopital.position:
        if drone.survivant:
            s = drone.deposer_survivant_hopital()
            if s:
                etat.score += 1
                evenement = f"LIVRAISON {s.identifiant} +1pt"
                surv_id = None
        if drone.identifiant not in drones_recharges_ce_tour:
            drone.recharger()
            bat_apres = drone.batterie
            drones_recharges_ce_tour.add(drone.identifiant)
            if not evenement:
                evenement = "RECHARGE"
    else:
        if drone.survivant is None:
            s = etat.survivant_sur_case(cible)
            if s:
                drone.prendre_survivant(s)
                surv_id = s.identifiant
                evenement = f"PRISE {s.identifiant}"
        else:
            surv_id = drone.survivant.identifiant

    if drone.hors_service:
        evenement = "HS"

    _mettre_a_jour_grille(etat)
    return _format_log_condense(etat, drone.identifiant, depart, cible,
                                bat_avant, bat_apres, evenement, surv_id)


def executer_mouvement_tempete(etat: EtatJeu, tempete: Tempete, cible: Position) -> str:
    depart = Position(tempete.position.col, tempete.position.lig)
    tempete.position = cible
    # Mémoriser la direction choisie manuellement
    tempete.direction = (
        cible.col - depart.col,
        cible.lig - depart.lig
    )
    appliquer_blocages(etat)
    _mettre_a_jour_grille(etat)
    return _format_log_condense(etat, tempete.identifiant, depart, cible)


# ---------------------------------------------------------------------------
# Propagation des ZONES X (fin de tour, périodique)
# Les TEMPÊTES NE SE PROPAGENT PAS.
# Ce sont les zones X existantes qui s'étendent vers leurs voisins ortho.
# ---------------------------------------------------------------------------

def propager_zones_x(etat: EtatJeu) -> list:
    """
    Tous les PROPAGATION_FREQUENCE tours, les zones X s'étendent.
    Source : chaque zone X existante (pas les tempêtes).
    Cibles : cases orthogonalement adjacentes à une zone X.
    Exclues : bâtiments, hôpital, zones X déjà existantes.
    Probabilité par case : PROBA_PROPAGATION.
    Retourne la liste des lignes de log.
    """
    logs = []
    if etat.tour % PROPAGATION_FREQUENCE != 0:
        return logs

    nouvelles_zones = set()
    hopital_pos = etat.hopital.position

    for zone_x in list(etat.zones_x):
        for voisin in zone_x.voisins_ortho():
            if etat.batiment_sur_case(voisin):
                continue
            if voisin == hopital_pos:
                continue
            if voisin in etat.zones_x:
                continue
            if voisin in nouvelles_zones:
                continue
            if random.random() < PROBA_PROPAGATION:
                nouvelles_zones.add(voisin)
                logs.append(f"T{etat.tour:02d}  X   PROPAGATION→{voisin}")

    for pos in nouvelles_zones:
        etat.zones_x.add(pos)
        etat.grille.definir(pos, 'X')

    return logs


# ---------------------------------------------------------------------------
# Déplacement automatique des tempêtes (IA — fin de tour)
# Appelé dans boucle_saisie() après la phase P2 manuelle.
# ---------------------------------------------------------------------------

def deplacer_tempetes(etat: EtatJeu) -> list:
    """
    Chaque tempête se déplace automatiquement de 1 case selon sa direction courante.
    Règles :
      - La tempête suit tempete.direction (dx, dy) initialisée aléatoirement
      - Si la case suivante est invalide / bâtiment / hôpital :
          rebond : nouvelle direction valide aléatoire parmi les 8 voisins
      - Si aucune direction libre : la tempête reste sur place
    Retourne la liste des lignes de log.
    """
    logs = []
    hopital_pos = etat.hopital.position

    def _cible_libre(pos):
        return (
            pos.est_valide()
            and not etat.batiment_sur_case(pos)
            and pos != hopital_pos
        )

    for tempete in etat.tempetes:
        depart = Position(tempete.position.col, tempete.position.lig)
        dx, dy = tempete.direction
        cible = Position(tempete.position.col + dx, tempete.position.lig + dy)

        if not _cible_libre(cible):
            voisins_libres = [
                v for v in tempete.position.voisins_diag()
                if _cible_libre(v)
            ]
            if voisins_libres:
                cible = random.choice(voisins_libres)
                tempete.direction = (
                    cible.col - tempete.position.col,
                    cible.lig - tempete.position.lig
                )
            else:
                logs.append(
                    _format_log_condense(etat, tempete.identifiant, depart, depart)
                )
                continue
        else:
            tempete.direction = (dx, dy)

        tempete.position = cible
        logs.append(
            _format_log_condense(etat, tempete.identifiant, depart, cible)
        )

    appliquer_blocages(etat)
    _mettre_a_jour_grille(etat)
    return logs


# ---------------------------------------------------------------------------
# Blocages
# ---------------------------------------------------------------------------

def appliquer_blocages(etat: EtatJeu):
    """Bloque les drones sous une tempête. Décrémente les blocages existants."""
    for drone in etat.drones:
        if drone.hors_service:
            continue
        if drone.bloque > 0:
            drone.bloque -= 1
        t = etat.tempete_sur_case(drone.position)
        if t:
            drone.bloque = 2


# ---------------------------------------------------------------------------
# Vérification fin de partie
# ---------------------------------------------------------------------------

def verifier_fin_partie(etat: EtatJeu) -> bool:
    if all(s.est_sauve() for s in etat.survivants):
        etat.partie_finie = True
        etat.victoire = True
        return True
    if etat.tour > NB_TOURS_MAX:
        etat.partie_finie = True
        etat.victoire = False
        return True
    if not etat.drones_actifs():
        etat.partie_finie = True
        etat.victoire = False
        return True
    return False


# ---------------------------------------------------------------------------
# Recharge explicite
# ---------------------------------------------------------------------------

def recharger_drone(etat: EtatJeu, drone: Drone) -> str:
    if drone.position != etat.hopital.position:
        return f"{drone.identifiant} n'est pas à l'hôpital"
    bat_avant = drone.batterie
    drone.recharger()
    return f"{drone.identifiant} rechargé : {bat_avant}→{drone.batterie}/{drone.batterie_max}"


# ---------------------------------------------------------------------------
# Utilitaire : mise à jour de la grille
# ---------------------------------------------------------------------------

def _mettre_a_jour_grille(etat: EtatJeu):
    g = etat.grille
    taille = g.taille
    for lig in range(taille):
        for col in range(taille):
            g.cases[lig][col] = '.'
    for pos in etat.zones_x:
        g.definir(pos, 'X')
    for s in etat.survivants:
        if s.etat == "en_attente":
            g.definir(s.position, 'S')
    for d in etat.drones:
        if not d.hors_service:
            g.definir(d.position, 'D')
    for t in etat.tempetes:
        g.definir(t.position, 'T')
    g.definir(etat.hopital.position, 'H')
    for b in etat.batiments:
        g.definir(b.position, 'B')


# ---------------------------------------------------------------------------
# Utilitaire : log condensé (1 ligne)
# ---------------------------------------------------------------------------

def _format_log_condense(etat: EtatJeu, identifiant: str,
                         depart: 'Position', arrivee: 'Position',
                         bat_avant: int = None, bat_apres: int = None,
                         evenement: str = "", surv_id: str = None) -> str:
    parts = [f"T{etat.tour:02d}", f"{identifiant:3s}", f"{depart}→{arrivee}"]
    if bat_avant is not None and bat_apres is not None:
        parts.append(f"bat:{bat_avant}→{bat_apres}")
    if surv_id:
        parts.append(f"[{surv_id}]")
    if evenement:
        parts.append(evenement)
    return "  ".join(parts)
