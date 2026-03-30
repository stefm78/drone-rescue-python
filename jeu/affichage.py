# =============================================================================
# affichage.py — Rendu de l'interface console de Drone Rescue
#
# LAYOUT :
#   ┌──────────────────────────────────────────────┐
#   │  SCORE · Surv. rest. · Zones X · Tour N/M    │  ← ligne score (haut)
#   ├──────────────────────────────────────────────┤
#   │                            │ DRONES           │
#   │   GRILLE 12x12             │ D1 A1  10/20 …  │  ← plateau + statuts droite
#   │                            │ TEMPÊTES         │
#   │                            │ T1 J2            │
#   ├──────────────────────────────────────────────┤
#   │  LOG  T04 D3 B7→E6  bat:6→5  …               │  ← log condensé (bas)
#   └──────────────────────────────────────────────┘
#   (zone saisie sous le log)
# =============================================================================

import os
import shutil
from modeles import EtatJeu, Drone
from config import NB_TOURS_MAX

# Codes ANSI
_C = {
    'D':  '\033[94m',  # Bleu   — drone
    'T':  '\033[91m',  # Rouge  — tempête
    'S':  '\033[92m',  # Vert   — survivant
    'H':  '\033[93m',  # Jaune  — hôpital
    'B':  '\033[90m',  # Gris   — bâtiment
    'X':  '\033[35m',  # Magenta — zone X
    'ERR':'\033[91m',
    'OK': '\033[92m',
    'RST':'\033[0m',
    'BLD':'\033[1m',
    'DIM':'\033[2m',
}


def _col(sym: str, txt: str = None) -> str:
    """Colore un texte avec la couleur du symbole donné."""
    c = _C.get(sym, '')
    return f"{c}{txt or sym}{_C['RST']}" if c else (txt or sym)


def _bold(txt: str) -> str:
    return f"{_C['BLD']}{txt}{_C['RST']}"


def _dim(txt: str) -> str:
    return f"{_C['DIM']}{txt}{_C['RST']}"


# ---------------------------------------------------------------------------
# Score (haut de l'écran)
# ---------------------------------------------------------------------------

def render_score(etat: EtatJeu, phase: str = '', depl_restants: int = -1) -> str:
    """
    Ligne de score affichée tout en haut.
    Exemples :
      ● Score 3  ·  Surv. 7  ·  Zones X 2  ·  Tour 4/20  ·  [P1-DRONES | dépl. 2/3]
    """
    nb_surv = etat.survivants_restants()
    nb_zones = len(etat.zones_x)
    base = (
        f"{_bold('Score')} {_col('H', str(etat.score))}  ·  "
        f"Surv. rest. {_col('S', str(nb_surv))}  ·  "
        f"Zones X {_col('X', str(nb_zones))}  ·  "
        f"Tour {etat.tour}/{NB_TOURS_MAX}"
    )
    if phase:
        from config import MAX_DEPL_DRONE, MAX_DEPL_TEMPETE
        max_d = MAX_DEPL_DRONE if 'DRONE' in phase else MAX_DEPL_TEMPETE
        if depl_restants >= 0:
            base += f"  ·  {_bold(phase)} {depl_restants}/{max_d}"
        else:
            base += f"  ·  {_bold(phase)}"
    return base


# ---------------------------------------------------------------------------
# Grille
# ---------------------------------------------------------------------------

def render_grille(etat: EtatJeu) -> list:
    """
    Retourne la grille sous forme de liste de lignes (str),
    sans retour à la ligne final, pour assemblage côte-à-côte.
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
# Statuts Drones (colonne droite)
# ---------------------------------------------------------------------------

def render_statuts_droite(etat: EtatJeu) -> list:
    """
    Retourne les lignes du panneau droit (Drones + Tempêtes),
    pour assemblage côte-à-côte avec la grille.
    """
    lignes = []

    # ── Drones ──
    lignes.append(_bold("DRONES"))
    lignes.append(_dim(f"{'ID':<4} {'Pos':<5} {'Bat':<9} {'Surv':<5} Blq"))
    lignes.append("─" * 30)
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

    lignes.append("")

    # ── Tempêtes ──
    lignes.append(_bold("TEMPÊTES"))
    lignes.append(_dim(f"{'ID':<4} {'Pos'}"))
    lignes.append("─" * 14)
    for t in etat.tempetes:
        lignes.append(_col('T', f"{t.identifiant:<4} {t.position}"))

    return lignes


# ---------------------------------------------------------------------------
# Log condensé (bas de l'écran)
# ---------------------------------------------------------------------------

def render_log_bas(etat: EtatJeu, nb_lignes: int) -> list:
    """
    Retourne les nb_lignes dernières lignes du log sous forme de liste.
    nb_lignes est calculé dynamiquement en fonction de la hauteur terminal.
    """
    if nb_lignes <= 0:
        return []
    lignes_log = [_bold("LOG") + _dim(" (mouvements validés)")]
    lignes_log.append("─" * 55)
    if not etat.historique:
        lignes_log.append(_dim("  (aucune action)"))
    else:
        extrait = etat.historique[-(nb_lignes):]  # dernières lignes
        for ligne in extrait:
            lignes_log.append(_dim("  ") + ligne)
    return lignes_log


# ---------------------------------------------------------------------------
# Affichage complet (efface et redessine l'écran)
# ---------------------------------------------------------------------------

def render_complet(etat: EtatJeu, log_tour: list = None,
                   phase: str = '', depl_restants: int = -1,
                   entite_selectionnee=None):
    """
    Efface le terminal et affiche :

      1. Score          (haut)
      2. Grille + statuts côte-à-côte
      3. Log condensé   (bas, taille adaptée au terminal)

    Paramètres
    ----------
    log_tour          : liste de lignes du tour en cours (pour info temps réel)
    phase             : 'DRONES' | 'TEMPETES' | ''
    depl_restants     : déplacements restants à afficher dans le score
    entite_selectionnee : non utilisé ici, réservé pour extensions
    """
    # Dimensions terminal
    try:
        term_cols, term_rows = shutil.get_terminal_size((120, 30))
    except Exception:
        term_cols, term_rows = 120, 30

    # Effacer l'écran
    print("\033[2J\033[H", end="")

    # ── 1. Score ──
    score_line = render_score(etat, phase, depl_restants)
    print(score_line)
    print("═" * min(term_cols, 80))

    # ── 2. Grille + Statuts côte-à-côte ──
    grille_lines  = render_grille(etat)
    droite_lines  = render_statuts_droite(etat)

    # Largeur grille brute (sans codes ANSI) : 5 + taille*4 chars
    taille = etat.grille.taille
    grille_width = 5 + taille * 4 + 2  # +2 pour la marge
    separateur = "  │  "

    nb_gr = len(grille_lines)
    nb_dr = len(droite_lines)
    max_lignes = max(nb_gr, nb_dr)

    for i in range(max_lignes):
        g = grille_lines[i] if i < nb_gr else ""
        d = droite_lines[i] if i < nb_dr else ""
        # Padding grille pour aligner la colonne droite
        g_visible = _strip_ansi(g)
        pad = grille_width - len(g_visible)
        print(g + " " * max(0, pad) + separateur + d)

    print()

    # ── 3. Log condensé (bas) ──
    # Lignes déjà utilisées : 1 score + 1 sépar + max_lignes grille + 1 vide
    lignes_utilisees = 1 + 1 + max_lignes + 1
    # Réserver 2 lignes pour le prompt de saisie
    lignes_log_dispo = max(0, term_rows - lignes_utilisees - 4)
    nb_log = min(8, max(2, lignes_log_dispo))  # entre 2 et 8 lignes

    print("─" * min(term_cols, 80))
    for ligne in render_log_bas(etat, nb_log - 1):  # -1 pour l'en-tête
        print(ligne)
    print()


def _strip_ansi(s: str) -> str:
    """Retire les codes ANSI pour calculer la largeur visible d'une chaîne."""
    import re
    return re.sub(r'\033\[[0-9;]*m', '', s)
