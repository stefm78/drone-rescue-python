# =============================================================================
# affichage.py — Rendu de l'interface console de Drone Rescue
#
# LAYOUT (3 zones) :
#
#   ┌─────────────────────────────────────────────────────────────────────────┐
#   │  DRONE RESCUE  ·  Score 3  ·  Surv. 7  ·  Tour 4/20  ·  [P1-DRONES]  │  ← ligne titre + score
#   ├────────────────────────┬──────────────────┬──────────────────────────┤
#   │                        │  D1  A1  10/20   │  T04  D3  B7→E6  bat:5   │
#   │   GRILLE  12×12        │  D2  B3   8/20   │  T04  D1  A1→B2  bat:9   │  ← 3 colonnes
#   │                        │  T1  J2          │  ...                      │
#   ├────────────────────────┴──────────────────┴──────────────────────────┤
#   │  P1-DRONES | dépl. 2/3 — sélectionner un drone ou 'next' :  _        │  ← saisie
#   └─────────────────────────────────────────────────────────────────────┘
#
# =============================================================================

import os
import re
import shutil
from modeles import EtatJeu, Drone
from config import NB_TOURS_MAX

# ---------------------------------------------------------------------------
# Codes ANSI
# ---------------------------------------------------------------------------
_C = {
    'D':  '\033[94m',   # Bleu       — drone
    'T':  '\033[91m',   # Rouge      — tempête
    'S':  '\033[92m',   # Vert       — survivant
    'H':  '\033[93m',   # Jaune      — hôpital
    'B':  '\033[90m',   # Gris       — bâtiment
    'X':  '\033[35m',   # Magenta    — zone X
    'ERR':'\033[91m',
    'OK': '\033[92m',
    'RST':'\033[0m',
    'BLD':'\033[1m',
    'DIM':'\033[2m',
    'CYN':'\033[96m',   # Cyan clair — titre jeu
}


def _col(sym: str, txt: str = None) -> str:
    """Colore un texte avec la couleur du symbole donné."""
    c = _C.get(sym, '')
    return f"{c}{txt or sym}{_C['RST']}" if c else (txt or sym)


def _bold(txt: str) -> str:
    return f"{_C['BLD']}{txt}{_C['RST']}"


def _dim(txt: str) -> str:
    return f"{_C['DIM']}{txt}{_C['RST']}"


def _strip_ansi(s: str) -> str:
    """Retire les codes ANSI pour calculer la largeur visible."""
    return re.sub(r'\033\[[0-9;]*m', '', s)


def _pad(s: str, width: int) -> str:
    """Pad une chaîne (avec codes ANSI) à une largeur visible donnée."""
    visible = len(_strip_ansi(s))
    return s + ' ' * max(0, width - visible)


# ---------------------------------------------------------------------------
# Ligne titre + score (zone 1)
# ---------------------------------------------------------------------------

def render_titre_score(etat: EtatJeu, phase: str = '', depl_restants: int = -1) -> str:
    """
    Ligne unique combinant titre du jeu et score.
    Exemple :
      ✦ DRONE RESCUE  ·  Score 3  ·  Surv. 7  ·  Zones X 2  ·  Tour 4/20  ·  [P1-DRONES 2/3]
    """
    from config import MAX_DEPL_DRONE, MAX_DEPL_TEMPETE
    titre = f"{_C['CYN']}{_C['BLD']}✦ DRONE RESCUE{_C['RST']}"
    nb_surv = etat.survivants_restants()
    nb_zones = len(etat.zones_x)
    ligne = (
        f"{titre}  ·  "
        f"{_bold('Score')} {_col('H', str(etat.score))}  ·  "
        f"Surv. {_col('S', str(nb_surv))}  ·  "
        f"Zones X {_col('X', str(nb_zones))}  ·  "
        f"Tour {etat.tour}/{NB_TOURS_MAX}"
    )
    if phase:
        max_d = MAX_DEPL_DRONE if 'DRONE' in phase else MAX_DEPL_TEMPETE
        if depl_restants >= 0:
            ligne += f"  ·  {_bold(phase)} {depl_restants}/{max_d}"
        else:
            ligne += f"  ·  {_bold(phase)}"
    return ligne


# ---------------------------------------------------------------------------
# Colonne 1 : Grille
# ---------------------------------------------------------------------------

def render_grille(etat: EtatJeu) -> list:
    """
    Retourne la grille sous forme de liste de lignes brutes (str ANSI),
    sans newline, pour assemblage côte-à-côte.
    """
    taille = etat.grille.taille
    lettres = list("ABCDEFGHIJKL")
    lignes = []

    entete = "     " + "   ".join(lettres[:taille])
    lignes.append(_bold(entete))
    lignes.append("    " + "─" * (taille * 4))

    for lig_idx in range(taille):
        num_lig = str(lig_idx + 1).rjust(2)
        cases = []
        for col_idx in range(taille):
            sym = etat.grille.cases[lig_idx][col_idx]
            cases.append(_col(sym))
        lignes.append(f"{num_lig} | " + "   ".join(cases))

    return lignes


# ---------------------------------------------------------------------------
# Colonne 2 : Statuts Drones + Tempêtes (sans titres DRONES/TEMPÊTES)
# ---------------------------------------------------------------------------

def render_statuts(etat: EtatJeu) -> list:
    """
    Retourne les lignes de statut des drones puis des tempêtes,
    SANS les en-têtes 'DRONES' et 'TEMPÊTES' pour gagner 2 lignes.
    Format compact :
      ID   Pos   Bat       Surv  Blq
      D1   A1    10/20     —
      ...séparateur vide...
      T1   J2
    """
    lignes = []

    # ── Drones ──
    lignes.append(_dim(f"{'ID':<4} {'Pos':<5} {'Bat':<9} {'Surv':<5} Blq"))
    lignes.append(_dim("─" * 30))
    for drone in etat.drones:
        statut = ""
        if drone.hors_service:
            statut = _col('ERR', "HS")
        elif drone.est_bloque():
            statut = _col('X', f"{drone.bloque}t")
        bat_str = f"{drone.batterie}/{drone.batterie_max}"
        surv_str = drone.survivant.identifiant if drone.survivant else "—"
        pos_str = str(drone.position)
        ligne = f"{drone.identifiant:<4} {pos_str:<5} {bat_str:<9} {surv_str:<5} {statut}"
        if drone.hors_service:
            ligne = _col('ERR', ligne)
        elif drone.est_bloque():
            ligne = _col('X', ligne)
        else:
            ligne = _col('D', drone.identifiant) + ligne[2:]
        lignes.append(ligne)

    # Ligne vide séparatrice
    lignes.append("")

    # ── Tempêtes ──
    lignes.append(_dim(f"{'ID':<4} {'Pos'}"))
    lignes.append(_dim("─" * 14))
    for t in etat.tempetes:
        lignes.append(_col('T', f"{t.identifiant:<4} {t.position}"))

    return lignes


# ---------------------------------------------------------------------------
# Colonne 3 : Log condensé (mouvements validés seulement)
# ---------------------------------------------------------------------------

def render_log_col(etat: EtatJeu, nb_lignes: int) -> list:
    """
    Retourne les nb_lignes dernières entrées du log (1 ligne/mouvement).
    L'en-tête occupe la 1ère ligne, les entrées suivent.
    """
    # en-tête sur 1 ligne
    lignes = [_dim("─── LOG ─────────────────────────────────")]
    if not etat.historique:
        lignes.append(_dim("  (aucun mouvement)"))
    else:
        # garder seulement nb_lignes-1 entrées (on a déjà l'en-tête)
        extrait = etat.historique[-(max(1, nb_lignes - 1)):]
        for l in extrait:
            lignes.append(_dim("  ") + l)
    return lignes


# ---------------------------------------------------------------------------
# Affichage complet
# ---------------------------------------------------------------------------

def render_complet(etat: EtatJeu, log_tour: list = None,
                   phase: str = '', depl_restants: int = -1,
                   entite_selectionnee=None):
    """
    Efface le terminal et affiche en 3 zones :

      1. Titre + score  (1 ligne)
      2. 3 colonnes côte-à-côte sur toute la hauteur disponible :
           Col1 : plateau
           Col2 : statuts drones + tempêtes
           Col3 : log condensé (mouvements validés)
      3. Ligne de séparation  ← la saisie joueur vient juste après

    La saisie (input) est appelée dans console.py juste après ce render.
    """
    try:
        term_cols, term_rows = shutil.get_terminal_size((120, 35))
    except Exception:
        term_cols, term_rows = 120, 35

    # Effacer l'écran
    print("\033[2J\033[H", end="")

    # ── Zone 1 : Titre + Score ──
    print(render_titre_score(etat, phase, depl_restants))
    print("═" * min(term_cols, 100))

    # ── Zone 2 : 3 colonnes ──
    col1 = render_grille(etat)           # plateau
    col2 = render_statuts(etat)          # statuts

    # Hauteur disponible : term_rows - 1 titre - 1 sépar haut - 1 sépar bas - 1 prompt
    hauteur_dispo = max(5, term_rows - 4)

    col3 = render_log_col(etat, hauteur_dispo)  # log adapté à la hauteur

    # Largeurs de colonnes visibles
    taille = etat.grille.taille
    col1_w = 5 + taille * 4 + 2          # grille : "  A   B  ..." + "N | . . ." + marge
    col2_w = 34                           # statuts : ~34 chars
    # col3 prend le reste

    sep = "  │  "

    nb_max = max(len(col1), len(col2), len(col3), hauteur_dispo)
    # Limiter à la hauteur dispo
    nb_max = min(nb_max, hauteur_dispo)

    for i in range(nb_max):
        c1 = col1[i] if i < len(col1) else ""
        c2 = col2[i] if i < len(col2) else ""
        c3 = col3[i] if i < len(col3) else ""
        print(_pad(c1, col1_w) + sep + _pad(c2, col2_w) + sep + c3)

    # ── Zone 3 : séparateur avant la saisie ──
    print("─" * min(term_cols, 100))
    # La saisie (print prompt + input) est faite dans console.py,
    # immédiatement après cet appel → elle apparaît toujours en bas.
