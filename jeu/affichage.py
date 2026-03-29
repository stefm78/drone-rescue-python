# =============================================================================
# affichage.py — Rendu de l'interface console de Drone Rescue
#
# Fonctions :
#   render_grille(etat)         -> str  (la grille 12x12 avec en-têtes)
#   render_drones(etat)         -> str  (tableau état des drones)
#   render_tempetes(etat)       -> str  (tableau état des tempêtes)
#   render_score(etat)          -> str  (ligne de score)
#   render_historique(etat, n)  -> str  (n dernières lignes du log)
#   render_console(messages)    -> str  (zone de saisie/réponses)
#   render_complet(etat, msgs)  -> None (affiche tout l'écran d'un coup)
# =============================================================================

from modeles import EtatJeu, Drone
from config import NB_TOURS_MAX

# Symboles avec couleurs ANSI (terminaux compatibles)
_COULEURS = {
    'D': '\033[94m',   # Bleu  — drone
    'T': '\033[91m',   # Rouge — tempête
    'S': '\033[92m',   # Vert  — survivant
    'H': '\033[93m',   # Jaune — hôpital
    'B': '\033[90m',   # Gris  — bâtiment
    'X': '\033[35m',   # Magenta — zone X
    '.': '',
    'RESET': '\033[0m',
    'BOLD': '\033[1m',
}


def _colorier(symbole: str) -> str:
    """Applique une couleur ANSI au symbole si disponible."""
    c = _COULEURS.get(symbole, '')
    r = _COULEURS['RESET']
    return f"{c}{symbole}{r}" if c else symbole


# ---------------------------------------------------------------------------
# Grille
# ---------------------------------------------------------------------------

def render_grille(etat: EtatJeu) -> str:
    """
    Retourne la représentation textuelle de la grille 12x12.
    Format :
        A   B   C  ...
     1  .   B   S  ...
     2  D   .   .  ...
    ...
    12  H   .   T  ...
    """
    lignes = []
    taille = etat.grille.taille

    # En-tête colonnes
    lettres = list("ABCDEFGHIJKL")
    entete = "     " + "   ".join(lettres[:taille])
    lignes.append(_COULEURS['BOLD'] + entete + _COULEURS['RESET'])
    lignes.append("    " + "─" * (taille * 4))

    for lig_idx in range(taille):
        num_lig = str(lig_idx + 1).rjust(2)
        cases = []
        for col_idx in range(taille):
            sym = etat.grille.cases[lig_idx][col_idx]
            cases.append(_colorier(sym))
        ligne = f"{num_lig} | " + "   ".join(cases)
        lignes.append(ligne)

    return "\n".join(lignes)


# ---------------------------------------------------------------------------
# Tableau Drones
# ---------------------------------------------------------------------------

def render_drones(etat: EtatJeu) -> str:
    """
    Retourne le tableau d'état des drones.

    Format :
    DRONES
    ID   Pos   Bat      Surv   Blq
    D1   A1    10/20    —       —
    D3   E6    5/20     S3      2t
    D6   F12    0/20   —       HS
    """
    entete = f"{'ID':<5} {'Pos':<6} {'Bat':<10} {'Surv':<7} {'Blq'}"
    sep = "─" * len(entete)
    lignes = [_COULEURS['BOLD'] + "DRONES" + _COULEURS['RESET'], entete, sep]

    for drone in etat.drones:
        statut = ""
        if drone.hors_service:
            statut = "HS"
        elif drone.est_bloque():
            statut = f"{drone.bloque}t"
        bat_str = f"{drone.batterie}/{drone.batterie_max}"
        surv_str = drone.survivant.identifiant if drone.survivant else "—"
        pos_str = str(drone.position)
        ligne = f"{drone.identifiant:<5} {pos_str:<6} {bat_str:<10} {surv_str:<7} {statut}"
        if drone.hors_service:
            ligne = _COULEURS['T'] + ligne + _COULEURS['RESET']
        elif drone.est_bloque():
            ligne = _COULEURS['X'] + ligne + _COULEURS['RESET']
        lignes.append(ligne)

    return "\n".join(lignes)


# ---------------------------------------------------------------------------
# Tableau Tempêtes
# ---------------------------------------------------------------------------

def render_tempetes(etat: EtatJeu) -> str:
    """
    Retourne le tableau d'état des tempêtes.

    Format :
    TEMPÊTES
    ID   Pos
    T1   J2
    T2   E6
    """
    entete = f"{'ID':<5} {'Pos'}"
    sep = "─" * 12
    lignes = [_COULEURS['BOLD'] + "TEMPÊTES" + _COULEURS['RESET'], entete, sep]
    for t in etat.tempetes:
        ligne = f"{t.identifiant:<5} {t.position}"
        ligne = _COULEURS['T'] + ligne + _COULEURS['RESET']
        lignes.append(ligne)
    return "\n".join(lignes)


# ---------------------------------------------------------------------------
# Ligne de score
# ---------------------------------------------------------------------------

def render_score(etat: EtatJeu) -> str:
    """
    Retourne la ligne de score.
    Exemple : Score 3  ·  Surv. rest. 7  ·  Zones X 2  ·  Tour 4/20
    """
    nb_zones = len(etat.zones_x)
    nb_surv_rest = etat.survivants_restants()
    return (
        f"{_COULEURS['BOLD']}Score {etat.score}{_COULEURS['RESET']}  ·  "
        f"Surv. rest. {nb_surv_rest}  ·  "
        f"Zones X {nb_zones}  ·  "
        f"Tour {etat.tour}/{NB_TOURS_MAX}"
    )


# ---------------------------------------------------------------------------
# Historique
# ---------------------------------------------------------------------------

def render_historique(etat: EtatJeu, nb_lignes: int = 10) -> str:
    """
    Retourne les nb_lignes dernières lignes de l'historique.

    Paramètres
    ----------
    etat      : EtatJeu
    nb_lignes : int  (défaut 10)
    """
    titre = _COULEURS['BOLD'] + "HISTORIQUE" + _COULEURS['RESET']
    if not etat.historique:
        return titre + "\n  (aucune action enregistrée)"
    extrait = etat.historique[-nb_lignes:]
    return titre + "\n" + "\n".join(f"  {ligne}" for ligne in extrait)


# ---------------------------------------------------------------------------
# Zone console (saisie / réponses)
# ---------------------------------------------------------------------------

def render_console(messages: list) -> str:
    """
    Affiche la zone de console (droite de l'écran).
    messages : liste de tuples (type, texte)
      type = 'saisie' | 'info' | 'erreur' | 'ok'

    Exemple :
        > D3
        [D3] pos. B7 sélect.
        > E6
          Cible E6 ✓ valide
        > ok
          D3→E6  bat.6→5
    """
    titre = _COULEURS['BOLD'] + "CONSOLE" + _COULEURS['RESET']
    sep = "─" * 30
    lignes = [titre, sep]
    for type_msg, texte in messages:
        if type_msg == 'saisie':
            lignes.append(f"> {texte}")
        elif type_msg == 'erreur':
            lignes.append(_COULEURS['T'] + f"  ✗ {texte}" + _COULEURS['RESET'])
        elif type_msg == 'ok':
            lignes.append(_COULEURS['S'] + f"  ✓ {texte}" + _COULEURS['RESET'])
        else:
            lignes.append(f"  {texte}")
    return "\n".join(lignes)


# ---------------------------------------------------------------------------
# Affichage complet (efface et redessine l'écran)
# ---------------------------------------------------------------------------

def render_complet(etat: EtatJeu, messages_console: list = None):
    """
    Efface le terminal et affiche l'écran complet :
    - Titre + numéro de tour
    - Grille (gauche) + Console (droite) sur la même zone
    - Tableau Drones + Tableau Tempêtes
    - Score
    - Historique (scroll)

    Note : l'affichage côte-à-côte nécessite un terminal large (>= 100 col).
    Pour simplicité, on affiche les blocs en séquence verticale.
    """
    if messages_console is None:
        messages_console = []

    # Effacer l'écran
    print("\033[2J\033[H", end="")

    # Titre
    titre = (
        f"{_COULEURS['BOLD']}DRONE RESCUE{_COULEURS['RESET']}  ·  "
        f"Tour {etat.tour}/{NB_TOURS_MAX}"
    )
    print(titre)
    print("═" * 60)

    # Grille
    print(render_grille(etat))
    print()

    # Console
    if messages_console:
        print(render_console(messages_console))
        print()

    # Drones + Tempêtes
    print(render_drones(etat))
    print()
    print(render_tempetes(etat))
    print()

    # Score
    print("═" * 60)
    print(render_score(etat))
    print("═" * 60)

    # Historique
    print(render_historique(etat, nb_lignes=8))
    print()
