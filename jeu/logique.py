# =============================================================================
# logique.py — Règles du jeu Drone Rescue
#
# Fonctions :
#   initialiser_partie()        -> EtatJeu
#   valider_mouvement()         -> (bool, str)
#   executer_mouvement()        -> str
#   propager_tempetes()         -> list[str]
#   appliquer_blocages()        -> None
#   verifier_fin_partie()       -> bool
#   recharger_drone()           -> str
#
# RÈGLES STRICTES (mises à jour) :
#   - Tour Drone  : 3 déplacements max, 1 case max/drone, chaque drone 1 fois max par tour
#   - Tour Tempête: 2 déplacements manuel max, 1 case max/tempête, chaque tempête 1 fois max
#   - Recharge hôpital : 1 seule fois par tour par drone (même si le drone reste dessus)
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
    - Hôpital placé en A12
    - Bâtiments placés aléatoirement
    - Drones placés aléatoirement
    - Tempêtes placées aléatoirement
    - Survivants placés aléatoirement
    - Zones X placées aléatoirement
    """
    etat = EtatJeu()
    occupees: set = set()

    pos_hopital = etat.hopital.position
    etat.grille.definir(pos_hopital, 'H')
    occupees.add(pos_hopital)

    for i in range(NB_BATIMENTS):
        pos = _position_aleatoire(occupees)
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


def _position_aleatoire(occupees: set, max_tentatives: int = 200) -> 'Position | None':
    """Retourne une position aléatoire libre dans la grille."""
    for _ in range(max_tentatives):
        col = random.randint(0, GRILLE_TAILLE - 1)
        lig = random.randint(0, GRILLE_TAILLE - 1)
        pos = Position(col, lig)
        if pos not in occupees:
            return pos
    return None


# ---------------------------------------------------------------------------
# Validation d'un mouvement drone
# ---------------------------------------------------------------------------

def valider_mouvement(etat: EtatJeu, drone: Drone, cible: Position) -> tuple:
    """
    Vérifie si le drone peut se déplacer vers la cible.

    Retourne (True, "") si valide, (False, raison) sinon.

    Règles :
      - Drone actif (pas HS, pas bloqué)
      - Cible dans la grille
      - Distance Chebyshev == 1 (une case exactement)
      - La cible n'est pas un bâtiment
      - Batterie > 0
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
    Vérifie si la tempête peut se déplacer vers la cible.

    Règles :
      - Cible dans la grille
      - Distance Chebyshev == 1
      - La cible n'est pas l'hôpital
      - La cible n'est pas un bâtiment
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
    """
    Déplace le drone vers cible (valider_mouvement doit avoir été appelé).
    drones_recharges_ce_tour : set d'identifiants de drones déjà rechargés ce tour.

    Gère :
      - Mise à jour position + grille
      - Consommation batterie
      - Blocage si tempête sur la cible
      - Récupération automatique d'un survivant
      - Livraison + recharge à l'hôpital (1 fois/tour/drone)

    Retourne la ligne de log condensée.
    """
    depart = Position(drone.position.col, drone.position.lig)

    # --- Blocage tempête sur la cible ---
    tempete_sur_cible = etat.tempete_sur_case(cible)
    if tempete_sur_cible:
        drone.bloque = 2
        drone.position = cible
        _mettre_a_jour_grille(etat)
        evt = f"BLOQUÉ({tempete_sur_cible.identifiant})"
        return _format_log_condense(etat, drone.identifiant, depart, cible,
                                    drone.batterie, drone.batterie, evt)

    # --- Déplacement normal ---
    bat_avant = drone.batterie
    drone.position = cible
    drone.consommer_batterie(1)
    bat_apres = drone.batterie

    evenement = ""
    surv_id = drone.survivant.identifiant if drone.survivant else None

    # --- Hôpital ---
    if cible == etat.hopital.position:
        # Livraison si porte un survivant
        if drone.survivant:
            s = drone.deposer_survivant_hopital()
            if s:
                etat.score += 1
                evenement = f"LIVRAISON {s.identifiant} +1pt"
                surv_id = None
        # Recharge : 1 seule fois par tour par drone
        if drone.identifiant not in drones_recharges_ce_tour:
            drone.recharger()
            bat_apres = drone.batterie
            drones_recharges_ce_tour.add(drone.identifiant)
            if not evenement:
                evenement = "RECHARGE"
    else:
        # --- Récupération d'un survivant ---
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
    """
    Déplace la tempête vers cible (valider_mouvement_tempete doit avoir été appelé).
    Applique les blocages de drones si nécessaire.
    Retourne la ligne de log condensée.
    """
    depart = Position(tempete.position.col, tempete.position.lig)
    tempete.position = cible
    appliquer_blocages(etat)
    _mettre_a_jour_grille(etat)
    return _format_log_condense(etat, tempete.identifiant, depart, cible)


# ---------------------------------------------------------------------------
# Propagation des tempêtes (automatique, fin de tour)
# ---------------------------------------------------------------------------

def propager_tempetes(etat: EtatJeu) -> list:
    """
    Tous les PROPAGATION_FREQUENCE tours, crée de nouvelles zones X.
    Retourne la liste des lignes de log condensées.
    """
    logs = []
    if etat.tour % PROPAGATION_FREQUENCE != 0:
        return logs

    nouvelles_zones = set()
    hopital_pos = etat.hopital.position

    for tempete in etat.tempetes:
        for voisin in tempete.position.voisins_ortho():
            if etat.batiment_sur_case(voisin):
                continue
            if voisin == hopital_pos:
                continue
            if etat.survivant_sur_case(voisin):
                continue
            if voisin in etat.zones_x:
                continue
            if voisin in nouvelles_zones:
                continue
            if random.random() < PROBA_PROPAGATION:
                nouvelles_zones.add(voisin)
                logs.append(
                    f"T{etat.tour:02d}  {tempete.identifiant}  PROPAGATION→{voisin}"
                )

    for pos in nouvelles_zones:
        etat.zones_x.add(pos)
        etat.grille.definir(pos, 'X')

    return logs


# ---------------------------------------------------------------------------
# Déplacement automatique des tempêtes (IA fin de tour)
# ---------------------------------------------------------------------------

def deplacer_tempetes(etat: EtatJeu) -> list:
    """
    Chaque tempête se déplace aléatoirement de 1 case (automatique).
    Retourne la liste des lignes de log condensées.
    """
    logs = []
    hopital_pos = etat.hopital.position

    for tempete in etat.tempetes:
        depart = Position(tempete.position.col, tempete.position.lig)
        voisins = [v for v in tempete.position.voisins_diag() if v != hopital_pos]
        if voisins:
            tempete.position = random.choice(voisins)
        logs.append(
            _format_log_condense(etat, tempete.identifiant, depart, tempete.position)
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
    """
    Retourne True et met à jour etat si la partie est terminée.
    Victoire : tous les survivants sauvés.
    Défaite : tours épuisés OU plus de drones actifs.
    """
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
# Utilitaire : log condensé (1 ligne, mouvements validés uniquement)
# ---------------------------------------------------------------------------

def _format_log_condense(etat: EtatJeu, identifiant: str,
                         depart: 'Position', arrivee: 'Position',
                         bat_avant: int = None, bat_apres: int = None,
                         evenement: str = "", surv_id: str = None) -> str:
    """
    Format condensé (1 seule ligne) :
      T04  D3  B7→E6  bat:6→5  [surv:S3]  [EVENEMENT]
    Les tempêtes n'ont pas de batterie ni de survivant.
    """
    parts = [f"T{etat.tour:02d}", f"{identifiant:3s}", f"{depart}→{arrivee}"]
    if bat_avant is not None and bat_apres is not None:
        parts.append(f"bat:{bat_avant}→{bat_apres}")
    if surv_id:
        parts.append(f"[{surv_id}]")
    if evenement:
        parts.append(evenement)
    return "  ".join(parts)
