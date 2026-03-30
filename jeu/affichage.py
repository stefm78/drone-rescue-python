# =============================================================================
# affichage.py — Rendu console de Drone Rescue
#
# Travaille exclusivement avec des dictionnaires (pas de classes).
# =============================================================================

import os
from config import NB_TOURS_MAX, MAX_DEPL_DRONE, MAX_DEPL_TEMPETE, LETTRES
from logique import _pos_str


def effacer_ecran():
    """Efface le terminal (Windows et Linux/Mac)."""
    os.system('cls' if os.name == 'nt' else 'clear')


# ---------------------------------------------------------------------------
# Ligne titre + score
# ---------------------------------------------------------------------------

def render_titre_score(etat, phase='', depl_restants=-1):
    """
    Retourne la ligne de titre du jeu avec les informations clés.
    Exemple : === DRONE RESCUE ===  Score:3  Surv.:4  ZonesX:2  Tour:4/20  [P1-DRONES 2/3]
    """
    nb_surv = sum(1 for s in etat["survivants"].values() if s["etat"] != "sauve")
    nb_zones = len(etat["zones_x"])
    ligne = (
        f"=== DRONE RESCUE ===  "
        f"Score:{etat['score']}  "
        f"Surv.:{nb_surv}  "
        f"ZonesX:{nb_zones}  "
        f"Tour:{etat['tour']}/{NB_TOURS_MAX}"
    )
    if phase:
        max_d = MAX_DEPL_DRONE if 'DRONE' in phase else MAX_DEPL_TEMPETE
        if depl_restants >= 0:
            ligne += f"  [{phase} {depl_restants}/{max_d}]"
        else:
            ligne += f"  [{phase}]"
    return ligne


# ---------------------------------------------------------------------------
# Colonne 1 : Grille
# ---------------------------------------------------------------------------

def render_grille(etat):
    """
    Retourne la grille sous forme de liste de lignes texte.
    Légende : .=vide  D=drone  T=tempête  S=survivant  H=hôpital  B=bâtiment  X=zone dangereuse
    """
    taille = len(etat["grille"])
    lignes = []

    entete = "      " + "  ".join(LETTRES[:taille])
    lignes.append(entete)
    lignes.append("    " + "---" * taille)

    for lig_idx in range(taille):
        num = str(lig_idx + 1).rjust(2)
        cases = "  ".join(etat["grille"][lig_idx][col_idx] for col_idx in range(taille))
        lignes.append(f"{num} |  {cases}")

    return lignes


# ---------------------------------------------------------------------------
# Colonne 2 : Statuts drones et tempêtes
# ---------------------------------------------------------------------------

def render_statuts(etat):
    """
    Retourne les lignes de statut des drones et des tempêtes.
    Format :
      ID   Pos   Bat      Surv  Blq
      D1   A1    10/20    --
    """
    lignes = []

    lignes.append(f"{'ID':<4} {'Pos':<5} {'Bat':<9} {'Surv':<6} Blq")
    lignes.append("-" * 32)

    for drone in etat["drones"].values():
        pos = _pos_str((drone["col"], drone["lig"]))
        bat = f"{drone['batterie']}/{drone['batterie_max']}"
        surv = drone["survivant"] if drone["survivant"] else "--"
        blq = str(drone["bloque"]) + "t" if drone["bloque"] > 0 else ""
        etat_str = "[HS]" if drone["hors_service"] else ""
        lignes.append(f"{drone['id']:<4} {pos:<5} {bat:<9} {surv:<6} {blq} {etat_str}")

    lignes.append("")

    lignes.append(f"{'ID':<4} {'Pos'}")
    lignes.append("-" * 14)
    for t in etat["tempetes"].values():
        pos = _pos_str((t["col"], t["lig"]))
        lignes.append(f"{t['id']:<4} {pos}")

    return lignes


# ---------------------------------------------------------------------------
# Colonne 3 : Log condensé
# ---------------------------------------------------------------------------

def render_log_col(etat, nb_lignes=20):
    """
    Retourne les dernières lignes du log.
    Les lignes de propagation [X] sont toujours affichées en fin de liste
    pour garantir leur visibilité même en cas de log long.
    """
    lignes_titre = ["--- LOG ---"]
    if not etat["historique"]:
        return lignes_titre + ["  (aucun mouvement)"]

    historique = etat["historique"]

    # Séparer les lignes de propagation X du reste
    lignes_x     = [l for l in historique if "[X]" in l]
    lignes_autres = [l for l in historique if "[X]" not in l]

    # Prendre les (nb_lignes - 1 - len(lignes_x)) dernières lignes normales
    quota_autres = max(0, nb_lignes - 1 - len(lignes_x))
    extrait = lignes_autres[-quota_autres:] if quota_autres > 0 else []

    # Assembler : lignes normales d'abord, puis propagation X à la fin
    toutes = extrait + lignes_x
    return lignes_titre + ["  " + l for l in toutes]


# ---------------------------------------------------------------------------
# Affichage complet
# ---------------------------------------------------------------------------

def render_complet(etat, phase='', depl_restants=-1):
    """
    Efface le terminal et affiche en 3 zones côte à côte :
      Titre + score
      Grille | Statuts | Log
    """
    effacer_ecran()

    print(render_titre_score(etat, phase, depl_restants))
    print("=" * 80)

    col1 = render_grille(etat)
    col2 = render_statuts(etat)
    col3 = render_log_col(etat)

    taille = len(etat["grille"])
    col1_w = 6 + taille * 3 + 2
    col2_w = 36

    nb_max = max(len(col1), len(col2), len(col3))
    for i in range(nb_max):
        c1 = col1[i] if i < len(col1) else ""
        c2 = col2[i] if i < len(col2) else ""
        c3 = col3[i] if i < len(col3) else ""
        print(f"{c1:<{col1_w}}  |  {c2:<{col2_w}}  |  {c3}")

    print("-" * 80)
