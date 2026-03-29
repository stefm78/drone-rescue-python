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
    - Drones placés aléatoirement (pas sur bâtiment, hôpital, ou entre eux)
    - Tempêtes placées aléatoirement
    - Survivants placés aléatoirement
    - Zones X placées aléatoirement
    """
    etat = EtatJeu()
    occupees: set = set()

    # --- Hôpital ---
    pos_hopital = etat.hopital.position
    etat.grille.definir(pos_hopital, 'H')
    occupees.add(pos_hopital)

    # --- Bâtiments ---
    for i in range(NB_BATIMENTS):
        pos = _position_aleatoire(occupees)
        if pos is None:
            break  # grille saturée (ne devrait pas arriver sur 12x12)
        bat = Batiment(pos)
        etat.batiments.append(bat)
        etat.grille.definir(pos, 'B')
        occupees.add(pos)

    # --- Drones ---
    for i in range(1, NB_DRONES + 1):
        pos = _position_aleatoire(occupees)
        if pos is None:
            break
        drone = Drone(f"D{i}", pos)
        etat.drones.append(drone)
        etat.grille.definir(pos, 'D')
        occupees.add(pos)

    # --- Tempêtes (pas sur hôpital) ---
    for i in range(1, NB_TEMPETES + 1):
        pos = _position_aleatoire(occupees)
        if pos is None:
            break
        tempete = Tempete(f"T{i}", pos)
        etat.tempetes.append(tempete)
        etat.grille.definir(pos, 'T')
        occupees.add(pos)

    # --- Survivants ---
    for i in range(1, NB_SURVIVANTS + 1):
        pos = _position_aleatoire(occupees)
        if pos is None:
            break
        surv = Survivant(f"S{i}", pos)
        etat.survivants.append(surv)
        etat.grille.definir(pos, 'S')
        occupees.add(pos)

    # --- Zones X ---
    for _ in range(NB_ZONES_DANGER):
        pos = _position_aleatoire(occupees)
        if pos is None:
            break
        etat.zones_x.add(pos)
        etat.grille.definir(pos, 'X')
        occupees.add(pos)

    return etat


def _position_aleatoire(occupees: set, max_tentatives: int = 200) -> Position | None:
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

    Retourne (True, "") si le mouvement est valide,
             (False, raison) sinon.

    Règles vérifiées :
      - Drone actif (pas HS, pas bloqué)
      - Cible dans les limites de la grille
      - Distance Chebyshev <= 1 (un pas à la fois)
      - La cible n'est pas un bâtiment
      - Le drone a de la batterie
    """
    if drone.hors_service:
        return False, f"{drone.identifiant} est hors service (batterie à 0)"
    if drone.est_bloque():
        return False, f"{drone.identifiant} est bloqué par une tempête ({drone.bloque} tour(s) restant(s))"
    if not cible.est_valide():
        return False, f"Position {cible} hors de la grille"
    if drone.position.distance_chebyshev(cible) > 1:
        return False, f"Distance trop grande (max 1 case par déplacement)"
    if etat.batiment_sur_case(cible):
        return False, f"Case {cible} bloquée par un bâtiment"
    if drone.batterie <= 0:
        return False, f"{drone.identifiant} n'a plus de batterie"
    return True, ""


# ---------------------------------------------------------------------------
# Exécution d'un mouvement drone
# ---------------------------------------------------------------------------

def executer_mouvement(etat: EtatJeu, drone: Drone, cible: Position) -> str:
    """
    Déplace le drone vers cible (valider_mouvement doit avoir été appelé avant).
    Gère :
      - Mise à jour position + grille
      - Consommation batterie
      - Blocage si tempête sur la cible
      - Récupération automatique d'un survivant
      - Livraison automatique à l'hôpital
      - Recharge automatique à l'hôpital

    Retourne la ligne de log correspondante.
    """
    depart = Position(drone.position.col, drone.position.lig)

    # --- Vérifier blocage tempête sur la cible ---
    tempete_sur_cible = etat.tempete_sur_case(cible)
    if tempete_sur_cible:
        # Drone immobilisé, batterie non consommée
        drone.bloque = 2  # bloqué 2 tours
        drone.position = cible
        _mettre_a_jour_grille(etat)
        evt = f"BLOQUÉ({tempete_sur_cible.identifiant})"
        surv_id = drone.survivant.identifiant if drone.survivant else "—"
        return _format_log(etat, 'D', drone.identifiant, depart, cible,
                           bat_avant=drone.batterie, bat_apres=drone.batterie,
                           surv=surv_id, evenement=evt)

    # --- Déplacement normal ---
    bat_avant = drone.batterie
    drone.position = cible
    drone.consommer_batterie(1)
    bat_apres = drone.batterie

    evenement = ""
    surv_id = "—"

    # --- Recharge à l'hôpital ---
    if cible == etat.hopital.position:
        bat_avant_recharge = drone.batterie
        drone.recharger()
        # Si le drone portait un survivant, on le livre
        if drone.survivant:
            s = drone.deposer_survivant_hopital()
            if s:
                etat.score += 1
                evenement = "LIVRAISON +1pt"
                surv_id = s.identifiant
        else:
            evenement = "RECHARGE"

    else:
        # --- Récupération d'un survivant sur la case ---
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
    return _format_log(etat, 'D', drone.identifiant, depart, cible,
                       bat_avant=bat_avant, bat_apres=bat_apres,
                       surv=surv_id, evenement=evenement)


# ---------------------------------------------------------------------------
# Propagation des tempêtes
# ---------------------------------------------------------------------------

def propager_tempetes(etat: EtatJeu) -> list:
    """
    Appelé tous les PROPAGATION_FREQUENCE tours.
    Pour chaque tempête, tente de créer une nouvelle zone X sur chaque
    voisin orthogonal éligible (ni bâtiment, ni hôpital, ni survivant, ni zone X existante).
    La probabilité de création est PROBA_PROPAGATION.

    Retourne la liste des lignes de log.
    """
    logs = []
    if etat.tour % PROPAGATION_FREQUENCE != 0:
        return logs

    nouvelles_zones = set()
    hopital_pos = etat.hopital.position

    for tempete in etat.tempetes:
        for voisin in tempete.position.voisins_ortho():
            # Exclure : bâtiment, hôpital, survivant, zone X déjà existante
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
                    _format_log(etat, 'T', tempete.identifiant,
                                tempete.position, tempete.position,
                                evenement=f"PROPAGATION→{voisin}")
                )

    for pos in nouvelles_zones:
        etat.zones_x.add(pos)
        etat.grille.definir(pos, 'X')

    return logs


# ---------------------------------------------------------------------------
# Déplacement automatique des tempêtes (IA basique)
# ---------------------------------------------------------------------------

def deplacer_tempetes(etat: EtatJeu) -> list:
    """
    Chaque tempête se déplace aléatoirement de 1 à MAX_DEPL_TEMPETE fois.
    Contraintes : ne peut pas aller sur l'hôpital.
    Retourne la liste des lignes de log.
    """
    logs = []
    hopital_pos = etat.hopital.position

    for tempete in etat.tempetes:
        depart = Position(tempete.position.col, tempete.position.lig)
        for _ in range(MAX_DEPL_TEMPETE):
            voisins = [v for v in tempete.position.voisins_diag() if v != hopital_pos]
            if not voisins:
                break
            tempete.position = random.choice(voisins)

        logs.append(
            _format_log(etat, 'T', tempete.identifiant, depart, tempete.position)
        )

    # Mettre à jour les blocages des drones sous une tempête
    appliquer_blocages(etat)
    _mettre_a_jour_grille(etat)
    return logs


# ---------------------------------------------------------------------------
# Blocages
# ---------------------------------------------------------------------------

def appliquer_blocages(etat: EtatJeu):
    """
    Vérifie si des drones se trouvent sur la case d'une tempête.
    Si oui, les bloque (drone.bloque = 2 tours).
    Décrémente aussi le compteur des drones déjà bloqués.
    """
    for drone in etat.drones:
        if drone.hors_service:
            continue
        # Décrémenter le blocage existant
        if drone.bloque > 0:
            drone.bloque -= 1
        # Nouveau blocage si tempête présente
        t = etat.tempete_sur_case(drone.position)
        if t:
            drone.bloque = 2


# ---------------------------------------------------------------------------
# Vérification fin de partie
# ---------------------------------------------------------------------------

def verifier_fin_partie(etat: EtatJeu) -> bool:
    """
    Met à jour etat.partie_finie et etat.victoire.
    Retourne True si la partie est terminée.

    Conditions de victoire : tous les survivants sont sauvés.
    Conditions de défaite  : nombre de tours max atteint
                              OU aucun drone actif restant.
    """
    # Victoire
    if all(s.est_sauve() for s in etat.survivants):
        etat.partie_finie = True
        etat.victoire = True
        return True

    # Défaite — tours épuisés
    if etat.tour > NB_TOURS_MAX:
        etat.partie_finie = True
        etat.victoire = False
        return True

    # Défaite — plus de drones actifs
    if not etat.drones_actifs():
        etat.partie_finie = True
        etat.victoire = False
        return True

    return False


# ---------------------------------------------------------------------------
# Recharge explicite d'un drone à l'hôpital
# ---------------------------------------------------------------------------

def recharger_drone(etat: EtatJeu, drone: Drone) -> str:
    """
    Recharge le drone si et seulement s'il est sur la case de l'hôpital.
    Retourne un message de résultat.
    """
    if drone.position != etat.hopital.position:
        return f"{drone.identifiant} n'est pas à l'hôpital (position : {drone.position})"
    bat_avant = drone.batterie
    drone.recharger()
    return f"{drone.identifiant} rechargé : {bat_avant}→{drone.batterie}/{drone.batterie_max}"


# ---------------------------------------------------------------------------
# Utilitaire : mise à jour de la grille depuis les entités
# ---------------------------------------------------------------------------

def _mettre_a_jour_grille(etat: EtatJeu):
    """
    Reconstruit les symboles de la grille depuis l'état réel des entités.
    Priorité d'affichage : Bâtiment > Hôpital > Tempête > Zone X > Drone > Survivant > vide
    """
    g = etat.grille
    taille = g.taille

    # Réinitialiser à vide
    for lig in range(taille):
        for col in range(taille):
            g.cases[lig][col] = '.'

    # Zones X
    for pos in etat.zones_x:
        g.definir(pos, 'X')

    # Survivants en attente
    for s in etat.survivants:
        if s.etat == "en_attente":
            g.definir(s.position, 'S')

    # Drones actifs
    for d in etat.drones:
        if not d.hors_service:
            g.definir(d.position, 'D')

    # Tempêtes (priorité sur les drones)
    for t in etat.tempetes:
        g.definir(t.position, 'T')

    # Hôpital
    g.definir(etat.hopital.position, 'H')

    # Bâtiments (priorité maximale)
    for b in etat.batiments:
        g.definir(b.position, 'B')


# ---------------------------------------------------------------------------
# Utilitaire : formatage d'une ligne de log
# ---------------------------------------------------------------------------

def _format_log(etat: EtatJeu, type_entite: str, identifiant: str,
                depart: Position, arrivee: Position,
                bat_avant: int = None, bat_apres: int = None,
                surv: str = "—", evenement: str = "") -> str:
    """
    Format : T[nn] P1 [D|T]  [ID] [dep]→[arr]  bat:[x→y]  surv:[id|—]  [EVENEMENT]
    """
    bat_str = ""
    if bat_avant is not None and bat_apres is not None:
        bat_str = f"bat:{bat_avant}→{bat_apres}"
    elif bat_avant is not None:
        bat_str = f"bat:{bat_avant}"

    parties = [
        f"T{etat.tour:02d}",
        "P1",
        type_entite,
        f"{identifiant:3s}",
        f"{depart}→{arrivee}",
    ]
    if bat_str:
        parties.append(bat_str)
    if surv and surv != "—":
        parties.append(f"surv:{surv}")
    if evenement:
        parties.append(evenement)

    return "  ".join(parties)
