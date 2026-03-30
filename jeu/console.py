# =============================================================================
# console.py — Interface de saisie joueur pour Drone Rescue
#
# RÈGLES STRICTES APPLIQUÉES :
#   Tour Drones (P1) :
#     - 3 déplacements max au total
#     - Chaque drone se déplace au plus 1 fois par tour
#     - 1 seule case par déplacement
#   Tour Tempêtes (P2) :
#     - 2 déplacements manuels max au total
#     - Chaque tempête déplacée au plus 1 fois par tour
#     - 1 seule case par déplacement
#   Recharge hôpital : 1 seule fois par tour par drone
#
# Si un mouvement est invalide :
#   - message d'erreur affiché INLINE (pas dans le log)
#   - on reste sur la saisie de cible (pas de ok/next)
# =============================================================================

from modeles import EtatJeu, Drone, Tempete, Position
from logique import (
    valider_mouvement, valider_mouvement_tempete,
    executer_mouvement, executer_mouvement_tempete,
    deplacer_tempetes, propager_tempetes,
    appliquer_blocages, verifier_fin_partie
)
from affichage import render_complet
from logger import log_action
from config import MAX_DEPL_DRONE, MAX_DEPL_TEMPETE


# ---------------------------------------------------------------------------
# Parser de commande
# ---------------------------------------------------------------------------

def parser_commande(texte: str) -> tuple:
    """
    Analyse une commande saisie.
    Retourne (type, valeur) :
      ('drone',    'D3')   identifiant drone
      ('tempete',  'T2')   identifiant tempête
      ('position', 'E6')   coordonnées cible
      ('next',     None)   passer au tour / phase suivante
      ('aide',     None)
      ('quitter',  None)
      ('inconnu',  texte)
    """
    t = texte.strip().upper()
    if not t:
        return ('inconnu', texte)
    if t in ('NEXT', 'N'):
        return ('next', None)
    if t in ('AIDE', '?', 'HELP'):
        return ('aide', None)
    if t in ('Q', 'QUITTER', 'QUIT'):
        return ('quitter', None)
    if len(t) == 2 and t[0] == 'D' and t[1].isdigit():
        return ('drone', t)
    if len(t) == 2 and t[0] == 'T' and t[1].isdigit():
        return ('tempete', t)
    if len(t) >= 2 and t[0].isalpha() and t[1:].isdigit():
        return ('position', t)
    return ('inconnu', texte)


# ---------------------------------------------------------------------------
# Utilitaire : afficher une erreur inline (zone prompt)
# ---------------------------------------------------------------------------

def _print_erreur(msg: str):
    print(f"\033[91m  ✗ {msg}\033[0m")


def _print_info(msg: str):
    print(f"  {msg}")


# ---------------------------------------------------------------------------
# Phase Drones (P1)
# ---------------------------------------------------------------------------

def phase_drones(etat: EtatJeu, log_tour: list) -> bool:
    """
    Phase de commande des drones.

    Règles :
      - MAX_DEPL_DRONE déplacements totaux dans le tour
      - Chaque drone au plus 1 déplacement par tour
      - Séquence : sélection drone → saisie cible (validation immédiate)
        Si cible invalide : redemander la cible, pas de ok/next
        Si cible valide   : déplacement exécuté directement (pas de ok)

    Retourne False si le joueur veut quitter.
    """
    # drone_id -> bool : a déjà bougé ce tour
    drones_bouge = {d.identifiant: False for d in etat.drones}
    # drone_id -> bool : a déjà été rechargé ce tour (hôpital)
    drones_recharges: set = set()
    deplacements_restants = MAX_DEPL_DRONE
    drone_actuel: Drone = None

    render_complet(etat, log_tour, phase='DRONES', depl_restants=deplacements_restants,
                   entite_selectionnee=None)

    while deplacements_restants > 0:
        # --- Prompt sélection drone ---
        if drone_actuel is None:
            print(f"  P1-DRONES | dépl. restants : {deplacements_restants}/{MAX_DEPL_DRONE}"
                  "  — sélectionner un drone (D1..D6) ou 'next' : ", end="")
        else:
            pos_str = str(drone_actuel.position)
            bat_str = f"bat:{drone_actuel.batterie}/{drone_actuel.batterie_max}"
            surv_str = f" [{drone_actuel.survivant.identifiant}]" if drone_actuel.survivant else ""
            print(f"  {drone_actuel.identifiant} | {pos_str} | {bat_str}{surv_str}"
                  f" | dépl. restants : {deplacements_restants}"
                  "  — cible (ex: E6) ou nouveau drone ou 'next' : ", end="")

        try:
            saisie = input().strip()
        except (EOFError, KeyboardInterrupt):
            return False

        type_cmd, valeur = parser_commande(saisie)

        if type_cmd == 'quitter':
            return False

        if type_cmd == 'aide':
            _afficher_aide()
            continue

        if type_cmd == 'next':
            break  # fin de la phase drones volontaire

        if type_cmd == 'drone':
            d = etat.drone_par_id(valeur)
            if d is None:
                _print_erreur(f"{valeur} : drone inexistant")
                continue
            if d.hors_service:
                _print_erreur(f"{valeur} est hors service")
                continue
            if d.est_bloque():
                _print_erreur(f"{valeur} est bloqué ({d.bloque} tour(s))")
                continue
            if drones_bouge[valeur]:
                _print_erreur(f"{valeur} a déjà bougé ce tour (1 déplacement/drone/tour)")
                continue
            drone_actuel = d
            _print_info(f"{valeur} sélectionné — position : {d.position}")
            continue

        if type_cmd == 'position':
            if drone_actuel is None:
                _print_erreur("Sélectionner d'abord un drone (D1..D6)")
                continue
            pos = Position.depuis_chaine(valeur)
            if pos is None:
                _print_erreur(f"{valeur} : coordonnées invalides")
                continue
            ok, raison = valider_mouvement(etat, drone_actuel, pos)
            if not ok:
                # Mouvement invalide → redemander la cible (pas de ok/next)
                _print_erreur(raison)
                continue
            # Mouvement valide → exécuter directement
            ligne_log = executer_mouvement(etat, drone_actuel, pos, drones_recharges)
            log_action(etat, ligne_log)
            log_tour.append(ligne_log)
            drones_bouge[drone_actuel.identifiant] = True
            deplacements_restants -= 1
            drone_actuel = None  # forcer nouvelle sélection
            render_complet(etat, log_tour, phase='DRONES', depl_restants=deplacements_restants,
                           entite_selectionnee=None)
            continue

        _print_erreur(f"Commande inconnue : '{saisie}'  (aide : ?)")  

    return True


# ---------------------------------------------------------------------------
# Phase Tempêtes manuelle (P2)
# ---------------------------------------------------------------------------

def phase_tempetes(etat: EtatJeu, log_tour: list) -> bool:
    """
    Phase de déplacement manuel des tempêtes.

    Règles :
      - MAX_DEPL_TEMPETE déplacements totaux dans le tour
      - Chaque tempête au plus 1 déplacement par tour
      - Séquence : sélection tempête → saisie cible
        Si cible invalide : redemander la cible
        Si cible valide   : déplacement exécuté directement

    Retourne False si le joueur veut quitter.
    """
    tempetes_bougees = {t.identifiant: False for t in etat.tempetes}
    deplacements_restants = MAX_DEPL_TEMPETE
    tempete_actuelle: Tempete = None

    render_complet(etat, log_tour, phase='TEMPETES', depl_restants=deplacements_restants,
                   entite_selectionnee=None)

    while deplacements_restants > 0:
        if tempete_actuelle is None:
            print(f"  P2-TEMPETES | dépl. restants : {deplacements_restants}/{MAX_DEPL_TEMPETE}"
                  "  — sélectionner une tempête (T1..T4) ou 'next' : ", end="")
        else:
            print(f"  {tempete_actuelle.identifiant} | {tempete_actuelle.position}"
                  f" | dépl. restants : {deplacements_restants}"
                  "  — cible (ex: K3) ou autre tempête ou 'next' : ", end="")

        try:
            saisie = input().strip()
        except (EOFError, KeyboardInterrupt):
            return False

        type_cmd, valeur = parser_commande(saisie)

        if type_cmd == 'quitter':
            return False
        if type_cmd == 'aide':
            _afficher_aide()
            continue
        if type_cmd == 'next':
            break

        if type_cmd == 'tempete':
            t = etat.tempete_par_id(valeur)
            if t is None:
                _print_erreur(f"{valeur} : tempête inexistante")
                continue
            if tempetes_bougees[valeur]:
                _print_erreur(f"{valeur} a déjà bougé ce tour (1 déplacement/tempête/tour)")
                continue
            tempete_actuelle = t
            _print_info(f"{valeur} sélectionnée — position : {t.position}")
            continue

        if type_cmd == 'position':
            if tempete_actuelle is None:
                _print_erreur("Sélectionner d'abord une tempête (T1..T4)")
                continue
            pos = Position.depuis_chaine(valeur)
            if pos is None:
                _print_erreur(f"{valeur} : coordonnées invalides")
                continue
            ok, raison = valider_mouvement_tempete(etat, tempete_actuelle, pos)
            if not ok:
                _print_erreur(raison)
                continue
            ligne_log = executer_mouvement_tempete(etat, tempete_actuelle, pos)
            log_action(etat, ligne_log)
            log_tour.append(ligne_log)
            tempetes_bougees[tempete_actuelle.identifiant] = True
            deplacements_restants -= 1
            tempete_actuelle = None
            render_complet(etat, log_tour, phase='TEMPETES', depl_restants=deplacements_restants,
                           entite_selectionnee=None)
            continue

        _print_erreur(f"Commande inconnue : '{saisie}'  (aide : ?)")

    return True


# ---------------------------------------------------------------------------
# Boucle de saisie principale (un tour complet)
# ---------------------------------------------------------------------------

def boucle_saisie(etat: EtatJeu) -> bool:
    """
    Gère un tour complet :
    1. Phase Drones (P1) — joueur pilote ses drones
    2. Phase Tempêtes manuelle (P2) — joueur déplace les tempêtes
    3. Déplacement automatique résiduel des tempêtes
    4. Propagation éventuelle
    5. Vérification fin de partie

    Retourne True si la partie continue, False pour quitter.
    """
    log_tour: list = []

    # --- P1 : Drones ---
    if not phase_drones(etat, log_tour):
        return False

    # --- P2 : Tempêtes (manuel) ---
    if not phase_tempetes(etat, log_tour):
        return False

    # --- Automatique : propagation ---
    for ligne in propager_tempetes(etat):
        log_action(etat, ligne)
        log_tour.append(ligne)

    # --- Fin de tour ---
    etat.tour += 1

    render_complet(etat, log_tour)

    if verifier_fin_partie(etat):
        if etat.victoire:
            print("\n  ★★★ VICTOIRE ! Tous les survivants ont été sauvés ! ★★★")
        else:
            raison = ("Nombre de tours maximum atteint." if etat.tour > 20
                      else "Plus aucun drone actif.")
            print(f"\n  ✕ DÉFAITE. {raison}")
        return False

    return True


# ---------------------------------------------------------------------------
# Aide
# ---------------------------------------------------------------------------

def _afficher_aide():
    print("""
  COMMANDES
  ─────────
  D1..D6     Sélectionner un drone        (P1)
  T1..T4     Sélectionner une tempête     (P2)
  A1..L12    Case cible du déplacement
  next / n   Terminer la phase en cours
  aide / ?   Cette aide
  q          Quitter la partie

  RÈGLES
  ──────
  P1 : 3 déplacements de drones / tour — 1 seul dépl./drone/tour — 1 case/dépl.
  P2 : 2 déplacements de tempêtes / tour — 1 seul dépl./tempête/tour — 1 case/dépl.
  Recharge hôpital : 1 fois / tour / drone (même si le drone reste dessus)

  SYMBOLES
  ────────
  .  vide   B  bâtiment  H  hôpital
  S  surv.  D  drone     T  tempête  X  zone danger
""")
