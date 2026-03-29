# =============================================================================
# console.py — Interface de saisie joueur pour Drone Rescue
#
# Fonctions :
#   boucle_saisie(etat)         -> None
#       Boucle principale d'un tour complet (drones + tempêtes)
#
#   parser_commande(texte)      -> (str, str | None)
#       Analyse une commande saisie et retourne (type, valeur)
#
#   afficher_prompt(drone_ou_tempete, deplacements_restants) -> None
#       Affiche l'invite de saisie
# =============================================================================

from modeles import EtatJeu, Drone, Tempete, Position
from logique import (
    valider_mouvement, executer_mouvement,
    deplacer_tempetes, propager_tempetes,
    appliquer_blocages, verifier_fin_partie
)
from affichage import render_complet, render_console
from logger import log_action
from config import MAX_DEPL_DRONE, MAX_DEPL_TEMPETE


# ---------------------------------------------------------------------------
# Parser de commande
# ---------------------------------------------------------------------------

def parser_commande(texte: str) -> tuple:
    """
    Analyse une commande saisie par le joueur.

    Retourne un tuple (type, valeur) :
      ('drone',    'D3')   si l'entrée est un identifiant de drone
      ('tempete',  'T2')   si l'entrée est un identifiant de tempête
      ('position', 'E6')   si l'entrée ressemble à des coordonnées
      ('ok',       None)   si l'entrée est 'ok' ou 'o'
      ('next',     None)   si l'entrée est 'next' ou 'n'
      ('aide',     None)   si l'entrée est 'aide' ou '?'
      ('quitter',  None)   si l'entrée est 'q' ou 'quitter'
      ('inconnu',  texte)  sinon
    """
    t = texte.strip().upper()
    if not t:
        return ('inconnu', texte)

    if t in ('OK', 'O'):
        return ('ok', None)
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

    # Coordonnées ex : "E6", "A12"
    if len(t) >= 2 and t[0].isalpha() and t[1:].isdigit():
        return ('position', t)

    return ('inconnu', texte)


# ---------------------------------------------------------------------------
# Invite de saisie
# ---------------------------------------------------------------------------

def afficher_prompt(entite, deplacements_restants: int):
    """
    Affiche l'invite de commande adaptée à l'entité sélectionnée.

    Paramètres
    ----------
    entite               : Drone | Tempete | None
    deplacements_restants: int
    """
    if entite is None:
        print("  Saisir l'identifiant d'un drone (D1…D6) ou 'next' pour passer : ", end="")
    elif isinstance(entite, Drone):
        surv = f" [porte {entite.survivant.identifiant}]" if entite.survivant else ""
        blq = f" [BLOQUÉ {entite.bloque}t]" if entite.est_bloque() else ""
        print(f"  {entite.identifiant} | {entite.position} | bat:{entite.batterie}/{entite.batterie_max}"
              f"{surv}{blq} | dépl. restants : {deplacements_restants}", end="")
        print()
        print("  Coordonnées cible (ou 'ok' pour valider / 'next') : ", end="")
    else:
        print(f"  {entite.identifiant} | {entite.position} | dépl. restants : {deplacements_restants} : ", end="")


# ---------------------------------------------------------------------------
# Affichage d'aide
# ---------------------------------------------------------------------------

def afficher_aide():
    print("""
  COMMANDES DISPONIBLES
  ─────────────────────
  D1..D6     Sélectionner un drone
  T1..T4     Sélectionner une tempête (phase tempêtes)
  A1..L12    Case cible du déplacement
  ok  / o    Confirmer la cible et exécuter le déplacement
  next / n   Passer au tour suivant
  aide / ?   Afficher cette aide
  q          Quitter la partie

  SYMBOLES GRILLE
  .  vide     B  bâtiment  H  hôpital
  S  survivant D  drone     T  tempête  X  zone danger
""")


# ---------------------------------------------------------------------------
# Boucle de saisie — Phase Drones
# ---------------------------------------------------------------------------

def phase_drones(etat: EtatJeu, messages: list):
    """
    Gère la phase de commande des drones pour un tour.
    Chaque drone peut se déplacer jusqu'à MAX_DEPL_DRONE fois.
    Le joueur sélectionne un drone, saisit une cible, confirme avec 'ok'.
    """
    drone_actuel = None
    cible_en_attente = None
    deplacements = {d.identifiant: 0 for d in etat.drones}

    while True:
        render_complet(etat, messages)
        afficher_prompt(drone_actuel,
                        MAX_DEPL_DRONE - deplacements.get(
                            drone_actuel.identifiant, 0) if drone_actuel else 0)

        try:
            saisie = input().strip()
        except (EOFError, KeyboardInterrupt):
            return False  # Quitter

        messages.append(('saisie', saisie))
        type_cmd, valeur = parser_commande(saisie)

        if type_cmd == 'quitter':
            return False

        if type_cmd == 'aide':
            afficher_aide()
            input("  [Entrée pour continuer]")
            continue

        if type_cmd == 'next':
            return True  # Passer au tour suivant

        if type_cmd == 'drone':
            d = etat.drone_par_id(valeur)
            if d is None:
                messages.append(('erreur', f"{valeur} : drone inexistant"))
                continue
            if d.hors_service:
                messages.append(('erreur', f"{valeur} est hors service"))
                continue
            if d.est_bloque():
                messages.append(('erreur', f"{valeur} est bloqué ({d.bloque} tour(s))"))
                continue
            if deplacements[valeur] >= MAX_DEPL_DRONE:
                messages.append(('erreur', f"{valeur} a déjà utilisé ses {MAX_DEPL_DRONE} déplacements"))
                continue
            drone_actuel = d
            cible_en_attente = None
            messages.append(('info', f"[{valeur}] pos. {d.position} sélect."))
            continue

        if type_cmd == 'position':
            if drone_actuel is None:
                messages.append(('erreur', "Sélectionner d'abord un drone (D1..D6)"))
                continue
            pos = Position.depuis_chaine(valeur)
            if pos is None:
                messages.append(('erreur', f"{valeur} : coordonnées invalides"))
                continue
            ok, raison = valider_mouvement(etat, drone_actuel, pos)
            if not ok:
                messages.append(('erreur', raison))
                cible_en_attente = None
                continue
            cible_en_attente = pos
            messages.append(('ok', f"Cible {pos} ✓ valide — saisir 'ok' pour confirmer"))
            continue

        if type_cmd == 'ok':
            if drone_actuel is None or cible_en_attente is None:
                messages.append(('erreur', "Aucune cible validée à confirmer"))
                continue
            ligne_log = executer_mouvement(etat, drone_actuel, cible_en_attente)
            log_action(etat, ligne_log)
            messages.append(('ok', ligne_log))
            deplacements[drone_actuel.identifiant] += 1
            cible_en_attente = None
            # Forcer sélection à None si plus de déplacements restants
            if deplacements[drone_actuel.identifiant] >= MAX_DEPL_DRONE:
                messages.append(('info', f"{drone_actuel.identifiant} a utilisé tous ses déplacements"))
                drone_actuel = None
            continue

        messages.append(('erreur', f"Commande inconnue : '{saisie}'. Taper 'aide' pour l'aide."))


# ---------------------------------------------------------------------------
# Boucle de saisie principale
# ---------------------------------------------------------------------------

def boucle_saisie(etat: EtatJeu) -> bool:
    """
    Gère un tour complet :
    1. Phase drones (joueur pilote ses drones)
    2. Phase tempêtes (déplacement automatique + propagation)
    3. Vérification fin de partie

    Retourne True si la partie continue, False pour quitter.
    """
    messages = []

    # --- Phase Drones ---
    continuer = phase_drones(etat, messages)
    if not continuer:
        return False

    # --- Phase Tempêtes (automatique) ---
    logs_tempetes = deplacer_tempetes(etat)
    for ligne in logs_tempetes:
        log_action(etat, ligne)
        messages.append(('info', ligne))

    logs_propagation = propager_tempetes(etat)
    for ligne in logs_propagation:
        log_action(etat, ligne)
        messages.append(('info', ligne))

    # --- Fin de tour ---
    etat.tour += 1

    # Afficher l'écran final du tour
    render_complet(etat, messages)

    # Vérification fin de partie
    if verifier_fin_partie(etat):
        if etat.victoire:
            print("\n  ★★★ VICTOIRE ! Tous les survivants ont été sauvés ! ★★★")
        else:
            print("\n  ✕ DÉFAITE. " + (
                "Nombre de tours maximum atteint." if etat.tour > 20
                else "Plus aucun drone actif."
            ))
        return False

    return True
