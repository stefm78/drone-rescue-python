# =============================================================================
# logique.py — Règles du jeu Drone Rescue
#
# Toutes les entités du jeu sont des DICTIONNAIRES Python.
# Aucune classe n'est utilisée (conformément aux contraintes du sujet).
#
# Structure d'un état de jeu (dict) :
#   etat = {
#       "tour"        : int,
#       "score"       : int,
#       "partie_finie": bool,
#       "victoire"    : bool,
#       "grille"      : list[list[str]],   # grille[lig][col]
#       "hopital"     : (col, lig),
#       "batiments"   : [(col, lig), ...],
#       "drones"      : { "D1": {drone_dict}, ... },
#       "tempetes"    : { "T1": {tempete_dict}, ... },
#       "survivants"  : { "S1": {survivant_dict}, ... },
#       "zones_x"     : {(col, lig), ...},
#       "historique"  : [str, ...],
#   }
#
# Structure d'un drone :
#   { "id": str, "col": int, "lig": int,
#     "batterie": int, "batterie_max": int,
#     "survivant": str|None,   # id du survivant embarqué
#     "bloque": int,           # tours restants de blocage
#     "hors_service": bool }
#
# Structure d'une tempête :
#   { "id": str, "col": int, "lig": int,
#     "dx": int, "dy": int }   # direction courante
#
# Structure d'un survivant :
#   { "id": str, "col": int, "lig": int,
#     "etat": "en_attente"|"embarque"|"sauve" }
# =============================================================================

import random
from config import (
    GRILLE_TAILLE, NB_DRONES, NB_TEMPETES, NB_BATIMENTS, NB_SURVIVANTS,
    BATTERIE_MAX, BATTERIE_INIT, NB_ZONES_DANGER,
    MAX_DEPL_DRONE, MAX_DEPL_TEMPETE, NB_TOURS_MAX,
    PROBA_PROPAGATION, PROPAGATION_FREQUENCE,
    COUT_TRANSPORT, COUT_ZONE_X, RECHARGE_HOPITAL,
    PROB_METEO, LETTRES
)


# ---------------------------------------------------------------------------
# Fonctions de création des entités
# ---------------------------------------------------------------------------

def creer_drone(identifiant, col, lig):
    """Retourne un dictionnaire représentant un drone."""
    return {
        "id"          : identifiant,
        "col"         : col,
        "lig"         : lig,
        "batterie"    : BATTERIE_INIT,
        "batterie_max": BATTERIE_MAX,
        "survivant"   : None,
        "bloque"      : 0,
        "hors_service": False,
    }


def creer_tempete(identifiant, col, lig):
    """Retourne un dictionnaire représentant une tempête."""
    dx = random.choice([-1, 0, 1])
    dy = random.choice([-1, 0, 1])
    if dx == 0 and dy == 0:
        dx = 1
    return {"id": identifiant, "col": col, "lig": lig, "dx": dx, "dy": dy}


def creer_survivant(identifiant, col, lig):
    """Retourne un dictionnaire représentant un survivant."""
    return {"id": identifiant, "col": col, "lig": lig, "etat": "en_attente"}


# ---------------------------------------------------------------------------
# Initialisation de la partie
# ---------------------------------------------------------------------------

def initialiser_partie():
    """
    Crée et retourne un état de jeu complet (dictionnaire).
    Placement aléatoire de toutes les entités.
    L'hôpital est placé aléatoirement. Aucun bâtiment ne peut lui être adjacent.
    """
    occupees = set()

    # Grille vide
    grille = [['.' for _ in range(GRILLE_TAILLE)] for _ in range(GRILLE_TAILLE)]

    # Hôpital
    hopital = _position_aleatoire(occupees)
    occupees.add(hopital)
    grille[hopital[1]][hopital[0]] = 'H'

    # Cases interdites aux bâtiments (8 voisins de l'hôpital)
    interdites_bat = set(_voisins_diag(hopital))

    # Bâtiments
    batiments = []
    for _ in range(NB_BATIMENTS):
        pos = _position_aleatoire(occupees, interdites=interdites_bat)
        if pos is None:
            break
        batiments.append(pos)
        occupees.add(pos)
        grille[pos[1]][pos[0]] = 'B'

    # Drones
    drones = {}
    for i in range(1, NB_DRONES + 1):
        pos = _position_aleatoire(occupees)
        if pos is None:
            break
        did = f"D{i}"
        drones[did] = creer_drone(did, pos[0], pos[1])
        occupees.add(pos)
        grille[pos[1]][pos[0]] = 'D'

    # Tempêtes
    tempetes = {}
    for i in range(1, NB_TEMPETES + 1):
        pos = _position_aleatoire(occupees)
        if pos is None:
            break
        tid = f"T{i}"
        tempetes[tid] = creer_tempete(tid, pos[0], pos[1])
        occupees.add(pos)
        grille[pos[1]][pos[0]] = 'T'

    # Survivants
    survivants = {}
    for i in range(1, NB_SURVIVANTS + 1):
        pos = _position_aleatoire(occupees)
        if pos is None:
            break
        sid = f"S{i}"
        survivants[sid] = creer_survivant(sid, pos[0], pos[1])
        occupees.add(pos)
        grille[pos[1]][pos[0]] = 'S'

    # Zones X (aucune sur l'hôpital ni les bâtiments — déjà dans occupees)
    zones_x = set()
    for _ in range(NB_ZONES_DANGER):
        pos = _position_aleatoire(occupees)
        if pos is None:
            break
        zones_x.add(pos)
        occupees.add(pos)
        grille[pos[1]][pos[0]] = 'X'

    return {
        "tour"        : 1,
        "score"       : 0,
        "partie_finie": False,
        "victoire"    : False,
        "grille"      : grille,
        "hopital"     : hopital,
        "batiments"   : batiments,
        "drones"      : drones,
        "tempetes"    : tempetes,
        "survivants"  : survivants,
        "zones_x"     : zones_x,
        "historique"  : [],
    }


# ---------------------------------------------------------------------------
# Validation des mouvements
# ---------------------------------------------------------------------------

def valider_mouvement(etat, drone, cible):
    """
    Vérifie si le drone (dict) peut se déplacer vers cible (col, lig).
    Ne contrôle PAS la batterie suffisante : ce cas est géré par executer_mouvement()
    (HS + dépôt du survivant sur place si applicable).
    Retourne (True, "") ou (False, raison).
    """
    did = drone["id"]
    if drone["hors_service"]:
        return False, f"{did} est hors service"
    if drone["bloque"] > 0:
        return False, f"{did} est bloqué ({drone['bloque']} tour(s))"
    if not _case_valide(cible):
        return False, "Position hors de la grille"
    if _distance_chebyshev(drone["col"], drone["lig"], cible[0], cible[1]) > 1:
        return False, "Max 1 case par déplacement"
    if _batiment_sur_case(etat, cible):
        return False, "Case bloquée par un bâtiment"
    if drone["batterie"] <= 0:
        return False, f"{did} n'a plus de batterie"
    return True, ""


def valider_mouvement_tempete(etat, tempete, cible):
    """Vérifie si la tempête (dict) peut se déplacer vers cible."""
    if not _case_valide(cible):
        return False, "Position hors de la grille"
    if _distance_chebyshev(tempete["col"], tempete["lig"], cible[0], cible[1]) > 1:
        return False, "Max 1 case par déplacement"
    if cible == etat["hopital"]:
        return False, "La tempête ne peut pas occuper l'hôpital"
    if _batiment_sur_case(etat, cible):
        return False, "Case bloquée par un bâtiment"
    return True, ""


# ---------------------------------------------------------------------------
# Recharge automatique en début de tour
# ---------------------------------------------------------------------------

def appliquer_recharges_hopital(etat, drones_recharges_ce_tour):
    """
    Recharge tous les drones stationnés à l'hôpital en début de tour
    (avant tout déplacement J1). C'est le SEUL mécanisme de recharge.
    Retourne la liste des lignes de log.
    """
    logs = []
    hopital = etat["hopital"]
    for drone in etat["drones"].values():
        did = drone["id"]
        if drone["hors_service"]:
            continue
        if (drone["col"], drone["lig"]) != hopital:
            continue
        if did in drones_recharges_ce_tour:
            continue
        bat_avant = drone["batterie"]
        drone["batterie"] = min(
            drone["batterie_max"],
            drone["batterie"] + RECHARGE_HOPITAL
        )
        drones_recharges_ce_tour.add(did)
        logs.append(
            f"T{etat['tour']:02d}  {did:3s}  bat +{RECHARGE_HOPITAL}  "
            f"{bat_avant}→{drone['batterie']}"
        )
    return logs


# ---------------------------------------------------------------------------
# Exécution des mouvements
# ---------------------------------------------------------------------------

def executer_mouvement(etat, drone, cible, drones_recharges_ce_tour):
    """
    Déplace le drone vers cible, applique les règles officielles.

    Règle recharge : la recharge à l'hôpital se fait UNIQUEMENT en début
    du tour suivant (appliquer_recharges_hopital). Aucune recharge immédiate
    à l'arrivée.

    Règle batterie insuffisante :
      - Le drone tombe HS sur sa case COURANTE (ne se déplace pas)
      - Si un survivant est à bord, il est déposé sur la case courante
        et repasse à l'état "en_attente"

    Règle collision tempête :
      - Le drone SE DÉPLACE vers la case tempête
      - La batterie est consommée normalement
      - Le drone est bloqué 2 tours
      - Aucune livraison/prise de survivant n'a lieu

    Retourne une ligne de log.
    """
    did = drone["id"]
    depart = (drone["col"], drone["lig"])
    bat_avant = drone["batterie"]

    # Coût de déplacement
    cout = COUT_TRANSPORT if drone["survivant"] else 1
    if cible in etat["zones_x"]:
        cout += COUT_ZONE_X

    # Batterie insuffisante : HS sur place, survivant déposé
    if drone["batterie"] < cout:
        evenement = "HS"
        if drone["survivant"]:
            s = etat["survivants"][drone["survivant"]]
            s["col"], s["lig"] = drone["col"], drone["lig"]
            s["etat"] = "en_attente"
            evenement = f"HS  {s['id']} déposé"
            drone["survivant"] = None
        drone["hors_service"] = True
        _mettre_a_jour_grille(etat)
        return _log(etat, did, depart, depart, bat_avant, drone["batterie"], evenement)

    # Consommation de la batterie
    drone["batterie"] = max(0, drone["batterie"] - cout)
    drone["col"], drone["lig"] = cible

    # Collision avec une tempête sur la cible ?
    tempete_sur_cible = _tempete_sur_case(etat, cible)
    if tempete_sur_cible:
        drone["bloque"] = 2
        if drone["batterie"] <= 0:
            evenement = f"HS+BLOQUE({tempete_sur_cible})"
            if drone["survivant"]:
                s = etat["survivants"][drone["survivant"]]
                s["col"], s["lig"] = cible
                s["etat"] = "en_attente"
                evenement = f"HS+BLOQUE({tempete_sur_cible})  {s['id']} déposé"
                drone["survivant"] = None
            drone["hors_service"] = True
            _mettre_a_jour_grille(etat)
            return _log(etat, did, depart, cible, bat_avant, drone["batterie"], evenement)
        _mettre_a_jour_grille(etat)
        return _log(etat, did, depart, cible, bat_avant, drone["batterie"],
                    f"BLOQUE({tempete_sur_cible})")

    # Mouvement normal
    evenement = ""
    surv_id = drone["survivant"]

    if cible == etat["hopital"]:
        # Livraison survivant
        if drone["survivant"]:
            s = etat["survivants"][drone["survivant"]]
            s["etat"] = "sauve"
            etat["score"] += 1
            evenement = f"LIVRAISON {s['id']} +1pt"
            drone["survivant"] = None
            surv_id = None
    else:
        # Prise de survivant
        if drone["survivant"] is None:
            s = _survivant_sur_case(etat, cible)
            if s:
                drone["survivant"] = s["id"]
                s["etat"] = "embarque"
                surv_id = s["id"]
                evenement = "PRISE"

    # Hors service (batterie tombée à 0 après mouvement normal) ?
    if drone["batterie"] <= 0:
        drone["hors_service"] = True
        if drone["survivant"]:
            s = etat["survivants"][drone["survivant"]]
            s["col"], s["lig"] = cible
            s["etat"] = "en_attente"
            evenement = f"HS  {s['id']} déposé"
            drone["survivant"] = None
            surv_id = None
        else:
            evenement = "HS"

    bat_apres = drone["batterie"]
    _mettre_a_jour_grille(etat)
    return _log(etat, did, depart, cible, bat_avant, bat_apres, evenement, surv_id)


def executer_mouvement_tempete(etat, tempete, cible):
    """Déplace manuellement une tempête (phase J2). Retourne une ligne de log."""
    tid = tempete["id"]
    depart = (tempete["col"], tempete["lig"])
    tempete["dx"] = cible[0] - depart[0]
    tempete["dy"] = cible[1] - depart[1]
    tempete["col"], tempete["lig"] = cible
    appliquer_blocages(etat)
    _mettre_a_jour_grille(etat)
    return _log(etat, tid, depart, cible)


# ---------------------------------------------------------------------------
# Phase météo : déplacement automatique des tempêtes
# ---------------------------------------------------------------------------

def deplacer_tempetes(etat, tempetes_exclues=None):
    """
    Phase automatique en fin de tour.
    Chaque tempête a PROB_METEO % de chance de bouger.
    Seuls les déplacements effectifs sont logués.
    Retourne la liste des lignes de log.
    """
    logs = []
    hopital = etat["hopital"]
    exclues = tempetes_exclues or set()

    for tempete in etat["tempetes"].values():
        tid = tempete["id"]
        depart = (tempete["col"], tempete["lig"])

        if tid in exclues:
            continue
        if random.random() > PROB_METEO:
            continue

        cible = (tempete["col"] + tempete["dx"],
                 tempete["lig"] + tempete["dy"])

        if not _case_libre_tempete(etat, cible, hopital):
            voisins = _voisins_diag(depart)
            libres = [v for v in voisins if _case_libre_tempete(etat, v, hopital)]
            if libres:
                cible = random.choice(libres)
                tempete["dx"] = cible[0] - depart[0]
                tempete["dy"] = cible[1] - depart[1]
            else:
                continue

        tempete["col"], tempete["lig"] = cible
        logs.append(_log(etat, tid, depart, cible))

    appliquer_blocages(etat)
    _mettre_a_jour_grille(etat)
    return logs


# ---------------------------------------------------------------------------
# Propagation des zones X (fin de tour, périodique)
# ---------------------------------------------------------------------------

def propager_zones_x(etat):
    """
    Tous les PROPAGATION_FREQUENCE tours, les zones X s'étendent.
    Retourne UNE SEULE ligne de log (préfixée [X]).
    """
    if etat["tour"] % PROPAGATION_FREQUENCE != 0:
        return []

    nouvelles = set()
    hopital = etat["hopital"]

    for zone in list(etat["zones_x"]):
        for voisin in _voisins_ortho(zone):
            if not _case_valide(voisin):
                continue
            if _batiment_sur_case(etat, voisin):
                continue
            if voisin == hopital:
                continue
            if voisin in etat["zones_x"] or voisin in nouvelles:
                continue
            if random.random() < PROBA_PROPAGATION:
                nouvelles.add(voisin)

    if nouvelles:
        for pos in nouvelles:
            etat["zones_x"].add(pos)
        positions_str = ", ".join(_pos_str(p) for p in sorted(nouvelles))
        log_ligne = f"T{etat['tour']:02d}  [X] +{len(nouvelles)} → {positions_str}"
    else:
        log_ligne = f"T{etat['tour']:02d}  [X] aucune extension ce tour"

    _mettre_a_jour_grille(etat)
    return [log_ligne]


# ---------------------------------------------------------------------------
# Blocages drones
# ---------------------------------------------------------------------------

def appliquer_blocages(etat):
    """Bloque les drones sous une tempête. Décrémente les compteurs de blocage."""
    tempetes_pos = {(t["col"], t["lig"]) for t in etat["tempetes"].values()}
    for drone in etat["drones"].values():
        if drone["hors_service"]:
            continue
        if drone["bloque"] > 0:
            drone["bloque"] -= 1
        if (drone["col"], drone["lig"]) in tempetes_pos:
            drone["bloque"] = 2


# ---------------------------------------------------------------------------
# Fin de partie
# ---------------------------------------------------------------------------

def verifier_fin_partie(etat):
    """Retourne True si la partie est terminée (victoire ou défaite)."""
    survivants = etat["survivants"]
    drones = etat["drones"]

    if all(s["etat"] == "sauve" for s in survivants.values()):
        etat["partie_finie"] = True
        etat["victoire"] = True
        return True
    if etat["tour"] > NB_TOURS_MAX:
        etat["partie_finie"] = True
        etat["victoire"] = False
        return True
    if all(d["hors_service"] for d in drones.values()):
        etat["partie_finie"] = True
        etat["victoire"] = False
        return True
    return False


# ---------------------------------------------------------------------------
# Helpers internes
# ---------------------------------------------------------------------------

def _case_valide(pos):
    col, lig = pos
    return 0 <= col < GRILLE_TAILLE and 0 <= lig < GRILLE_TAILLE


def _distance_chebyshev(c1, l1, c2, l2):
    return max(abs(c2 - c1), abs(l2 - l1))


def _batiment_sur_case(etat, pos):
    return pos in etat["batiments"]


def _tempete_sur_case(etat, pos):
    for t in etat["tempetes"].values():
        if (t["col"], t["lig"]) == pos:
            return t["id"]
    return None


def _survivant_sur_case(etat, pos):
    for s in etat["survivants"].values():
        if s["etat"] == "en_attente" and (s["col"], s["lig"]) == pos:
            return s
    return None


def _case_libre_tempete(etat, pos, hopital):
    return (
        _case_valide(pos)
        and not _batiment_sur_case(etat, pos)
        and pos != hopital
    )


def _position_aleatoire(occupees, interdites=None, max_tentatives=200):
    interdit = (interdites or set()) | occupees
    for _ in range(max_tentatives):
        col = random.randint(0, GRILLE_TAILLE - 1)
        lig = random.randint(0, GRILLE_TAILLE - 1)
        pos = (col, lig)
        if pos not in interdit:
            return pos
    return None


def _voisins_ortho(pos):
    col, lig = pos
    return [(col, lig - 1), (col, lig + 1), (col - 1, lig), (col + 1, lig)]


def _voisins_diag(pos):
    col, lig = pos
    return [
        (col + dc, lig + dl)
        for dc in (-1, 0, 1)
        for dl in (-1, 0, 1)
        if not (dc == 0 and dl == 0)
    ]


def _mettre_a_jour_grille(etat):
    g = etat["grille"]
    for lig in range(GRILLE_TAILLE):
        for col in range(GRILLE_TAILLE):
            g[lig][col] = '.'
    for pos in etat["zones_x"]:
        g[pos[1]][pos[0]] = 'X'
    for s in etat["survivants"].values():
        if s["etat"] == "en_attente":
            g[s["lig"]][s["col"]] = 'S'
    for d in etat["drones"].values():
        if not d["hors_service"]:
            g[d["lig"]][d["col"]] = 'D'
    for t in etat["tempetes"].values():
        g[t["lig"]][t["col"]] = 'T'
    hcol, hlig = etat["hopital"]
    g[hlig][hcol] = 'H'
    for pos in etat["batiments"]:
        g[pos[1]][pos[0]] = 'B'


def _pos_str(pos):
    col, lig = pos
    if 0 <= col < len(LETTRES):
        return f"{LETTRES[col]}{lig + 1}"
    return f"({col},{lig})"


def position_depuis_chaine(texte):
    """
    Convertit une saisie comme 'B3' ou 'b3' en tuple (col, lig).
    Retourne None si la saisie est invalide.
    """
    texte = texte.strip().upper()
    if len(texte) < 2:
        return None
    lettre = texte[0]
    if lettre not in LETTRES:
        return None
    try:
        lig = int(texte[1:]) - 1
    except ValueError:
        return None
    col = LETTRES.index(lettre)
    if _case_valide((col, lig)):
        return (col, lig)
    return None


def _log(etat, identifiant, depart, arrivee,
         bat_avant=None, bat_apres=None, evenement="", surv_id=None):
    """Formate une ligne de log condensée pour un mouvement."""
    dep_str = _pos_str(depart)
    arr_str = _pos_str(arrivee)
    parts = [f"T{etat['tour']:02d}", f"{identifiant:3s}", f"{dep_str}→{arr_str}"]
    if bat_avant is not None and bat_apres is not None:
        parts.append(f"bat:{bat_avant}→{bat_apres}")
    if surv_id:
        parts.append(f"+ [{surv_id}]")
    if evenement:
        parts.append(evenement)
    return "  ".join(parts)
