# =============================================================================
# config.py — Lecture de la configuration depuis config.json
#
# Expose toutes les constantes utilisées dans le jeu.
# Le fichier config.json est la SEULE source de vérité pour les paramètres.
# =============================================================================

import json
import os

_DOSSIER = os.path.dirname(os.path.abspath(__file__))
_CHEMIN_CONFIG = os.path.join(_DOSSIER, "config.json")

with open(_CHEMIN_CONFIG, encoding="utf-8") as _f:
    _cfg = json.load(_f)

# ── Grille ──────────────────────────────────────────────────────────────────
GRILLE_TAILLE = _cfg["grille"]["lignes"]          # grille carrée

# ── Drones ──────────────────────────────────────────────────────────────────
NB_DRONES      = _cfg["drones"]["nb_max_j1"]
BATTERIE_MAX   = _cfg["drones"]["batterie_max"]
BATTERIE_INIT  = _cfg["drones"]["batterie_depart"]

# ── Tempêtes ────────────────────────────────────────────────────────────────
NB_TEMPETES    = _cfg["tempetes"]["nb_max_j2"]
PROB_METEO     = _cfg["tempetes"]["prob_meteo"]    # 50 % de bouger auto

# ── Règles de jeu ───────────────────────────────────────────────────────────
COUT_TRANSPORT   = _cfg["regles"]["cout_transport_survivant"]  # 2 unités
COUT_ZONE_X      = _cfg["regles"]["cout_entree_zone_x"]        # 2 unités
RECHARGE_HOPITAL = _cfg["regles"]["recharge_hopital_par_tour"] # +3 par tour

# ── Placement initial ────────────────────────────────────────────────────────
NB_SURVIVANTS   = 4
NB_BATIMENTS    = 3
NB_ZONES_DANGER = 3

# ── Limites de déplacement par tour ─────────────────────────────────────────
MAX_DEPL_DRONE   = 3   # J1 : 3 déplacements max (1/drone, 3 drones max)
MAX_DEPL_TEMPETE = 2   # J2 : 2 déplacements max (1/tempête, 2 tempêtes max)

# ── Tour maximum ─────────────────────────────────────────────────────────────
NB_TOURS_MAX = 20

# ── Propagation des zones X ──────────────────────────────────────────────────
PROBA_PROPAGATION    = 0.3   # probabilité qu'un voisin ortho devienne X
PROPAGATION_FREQUENCE = 3    # tous les N tours

# ── Lettres de colonnes ──────────────────────────────────────────────────────
LETTRES = _cfg["lettres"][:GRILLE_TAILLE]

# ── Directions (pour argparse futur ou aide en jeu) ──────────────────────────
DIRECTIONS = _cfg["directions"]
