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
#   Hôpital : aucun bâtiment adjacent
#   Propagation : les ZONES X s'étendent (pas les tempêtes)
#   Déplacement auto des tempêtes : en fin de tour (après P2)
#
# PRINCIPE AFFICHAGE :
#   - Aucun print() entre render_complet() et input()
#   - Les erreurs sont passées en paramètre à render_complet() via msg_erreur=
#     -> elles s'affichent inline sur la ligne de prompt, en rouge
#   - Le log n'est jamais pollué par des erreurs
# =============================================================================

from modeles import EtatJeu, Drone, Tempete, Position
from logique import (
    valider_mouvement, valider_mouvement_tempete,
    executer_mouvement, executer_mouvement_tempete,
    deplacer_tempetes, propager_zones_x,
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
# Prompt inline — jamais de print() autonome
# ---------------------------------------------------------------------------

def _prompt(texte_prompt: str, msg_erreur: str = None) -> str:
    if msg_erreur:
        print(f"  \033[91m\u2717 {msg_erreur}\033[0m")
    print(f"  {texte_prompt}", end="", flush=True)
    try:
        return input().strip()
    except (EOFError, KeyboardInterrupt):
        return 'q'


# ---------------------------------------------------------------------------
# Phase Drones (P1)
# ---------------------------------------------------------------------------

def phase_drones(etat: EtatJeu, log_tour: list) -> bool:
    """
    Phase de commande des drones.
    Retourne False si le joueur veut quitter.
    """
    drones_bouge = {d.identifiant: False for d in etat.drones}
    drones_recharges: set = set()
    deplacements_restants = MAX_DEPL_DRONE
    drone_actuel: Drone = None
    msg_erreur: str = None

    while deplacements_restants > 0:
        render_complet(etat, log_tour, phase='DRONES', depl_restants=deplacements_restants,
                       entite_selectionnee=drone_actuel)

        if drone_actuel is None:
            texte_prompt = (f"P1-DRONES | {deplacements_restants}/{MAX_DEPL_DRONE} dépl."
                            "  — drone (D1..D6) ou 'next' : ")
        else:
            pos_str = str(drone_actuel.position)
            bat_str = f"bat:{drone_actuel.batterie}/{drone_actuel.batterie_max}"
            surv_str = f" [{drone_actuel.survivant.identifiant}]" if drone_actuel.survivant else ""
            texte_prompt = (f"{drone_actuel.identifiant} | {pos_str} | {bat_str}{surv_str}"
                            f" | {deplacements_restants} dépl. restants"
                            "  — cible (ex: E6) / autre drone / 'next' : ")

        saisie = _prompt(texte_prompt, msg_erreur)
        msg_erreur = None

        type_cmd, valeur = parser_commande(saisie)

        if type_cmd == 'quitter':
            return False

        if type_cmd == 'aide':
            render_complet(etat, log_tour, phase='DRONES', depl_restants=deplacements_restants)
            _afficher_aide()
            input("  [Entrée pour continuer]")
            continue

        if type_cmd == 'next':
            break

        if type_cmd == 'drone':
            d = etat.drone_par_id(valeur)
            if d is None:
                msg_erreur = f"{valeur} : drone inexistant"
                continue
            if d.hors_service:
                msg_erreur = f"{valeur} est hors service"
                continue
            if d.est_bloque():
                msg_erreur = f"{valeur} est bloqué ({d.bloque} tour(s))"
                continue
            if drones_bouge[valeur]:
                msg_erreur = f"{valeur} a déjà bougé ce tour (1 dépl./drone/tour)"
                continue
            drone_actuel = d
            continue

        if type_cmd == 'position':
            if drone_actuel is None:
                msg_erreur = "Sélectionner d'abord un drone (D1..D6)"
                continue
            pos = Position.depuis_chaine(valeur)
            if pos is None:
                msg_erreur = f"{valeur} : coordonnées invalides"
                continue
            ok, raison = valider_mouvement(etat, drone_actuel, pos)
            if not ok:
                msg_erreur = raison
                continue
            ligne_log = executer_mouvement(etat, drone_actuel, pos, drones_recharges)
            log_action(etat, ligne_log)
            log_tour.append(ligne_log)
            drones_bouge[drone_actuel.identifiant] = True
            deplacements_restants -= 1
            drone_actuel = None
            continue

        msg_erreur = f"Commande inconnue : '{saisie}'  (aide : ?)"

    return True


# ---------------------------------------------------------------------------
# Phase Tempêtes manuelle (P2)
# ---------------------------------------------------------------------------

def phase_tempetes(etat: EtatJeu, log_tour: list) -> bool:
    """
    Phase de déplacement manuel des tempêtes.
    Retourne False si le joueur veut quitter.
    """
    tempetes_bougees = {t.identifiant: False for t in etat.tempetes}
    deplacements_restants = MAX_DEPL_TEMPETE
    tempete_actuelle: Tempete = None
    msg_erreur: str = None

    while deplacements_restants > 0:
        render_complet(etat, log_tour, phase='TEMPETES', depl_restants=deplacements_restants,
                       entite_selectionnee=tempete_actuelle)

        if tempete_actuelle is None:
            texte_prompt = (f"P2-TEMPETES | {deplacements_restants}/{MAX_DEPL_TEMPETE} dépl."
                            "  — tempête (T1..T4) ou 'next' : ")
        else:
            texte_prompt = (f"{tempete_actuelle.identifiant} | {tempete_actuelle.position}"
                            f" | {deplacements_restants} dépl. restants"
                            "  — cible (ex: K3) / autre tempête / 'next' : ")

        saisie = _prompt(texte_prompt, msg_erreur)
        msg_erreur = None

        type_cmd, valeur = parser_commande(saisie)

        if type_cmd == 'quitter':
            return False
        if type_cmd == 'aide':
            render_complet(etat, log_tour, phase='TEMPETES', depl_restants=deplacements_restants)
            _afficher_aide()
            input("  [Entrée pour continuer]")
            continue
        if type_cmd == 'next':
            break

        if type_cmd == 'tempete':
            t = etat.tempete_par_id(valeur)
            if t is None:
                msg_erreur = f"{valeur} : tempête inexistante"
                continue
            if tempetes_bougees[valeur]:
                msg_erreur = f"{valeur} a déjà bougé ce tour (1 dépl./tempête/tour)"
                continue
            tempete_actuelle = t
            continue

        if type_cmd == 'position':
            if tempete_actuelle is None:
                msg_erreur = "Sélectionner d'abord une tempête (T1..T4)"
                continue
            pos = Position.depuis_chaine(valeur)
            if pos is None:
                msg_erreur = f"{valeur} : coordonnées invalides"
                continue
            ok, raison = valider_mouvement_tempete(etat, tempete_actuelle, pos)
            if not ok:
                msg_erreur = raison
                continue
            ligne_log = executer_mouvement_tempete(etat, tempete_actuelle, pos)
            log_action(etat, ligne_log)
            log_tour.append(ligne_log)
            tempetes_bougees[tempete_actuelle.identifiant] = True
            deplacements_restants -= 1
            tempete_actuelle = None
            continue

        msg_erreur = f"Commande inconnue : '{saisie}'  (aide : ?)"

    return True


# ---------------------------------------------------------------------------
# Boucle de saisie principale (un tour complet)
# ---------------------------------------------------------------------------

def boucle_saisie(etat: EtatJeu) -> bool:
    """
    Gère un tour complet :
    1. Phase Drones (P1)         — joueur pilote ses drones
    2. Phase Tempêtes (P2)       — joueur déplace les tempêtes manuellement
    3. Déplacement auto des tempêtes (IA)
    4. Propagation des zones X (périodique)
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

    # --- Automatique : déplacement des tempêtes (après P2) ---
    for ligne in deplacer_tempetes(etat):
        log_action(etat, ligne)
        log_tour.append(ligne)

    # --- Automatique : propagation des zones X ---
    for ligne in propager_zones_x(etat):
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
            print(f"\n  \u2715 DÉFAITE. {raison}")
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
  Recharge hôpital : 1 fois / tour / drone
  Fin de tour : les tempêtes se déplacent automatiquement
  Zones X : s'étendent périodiquement (les tempêtes ne propagent PAS)

  SYMBOLES
  ────────
  .  vide   B  bâtiment  H  hôpital
  S  surv.  D  drone     T  tempête  X  zone danger
""")
