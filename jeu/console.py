# =============================================================================
# console.py — Boucle de jeu et saisie des joueurs
#
# Architecture : parser → valider → exécuter → afficher
#
# Phase J1 (Joueur 1 — Drones) :
#   - Choisit un drone (ex: D1)
#   - Saisit une destination (ex: B3)
#   - Max 3 déplacements par tour (1 par drone)
#
# Phase J2 (Joueur 2 — Tempêtes) :
#   - Choisit une tempête (ex: T1)
#   - Saisit une destination (ex: E5)
#   - Max 2 déplacements par tour (1 par tempête)
#
# Commandes communes : 'next' = passer à la phase suivante, 'q' = quitter
# =============================================================================

from affichage import render_complet
from logique import (
    valider_mouvement, executer_mouvement,
    valider_mouvement_tempete, executer_mouvement_tempete,
    deplacer_tempetes, propager_zones_x,
    appliquer_blocages, verifier_fin_partie,
    appliquer_recharges_hopital,
    position_depuis_chaine, _pos_str
)
from config import MAX_DEPL_DRONE, MAX_DEPL_TEMPETE
from logger import enregistrer_log, sauvegarder_resultats


def boucle_de_jeu(etat):
    """
    Boucle principale du jeu.
    Alterne les phases J1 et J2 jusqu'à la fin de partie.
    """
    while not etat["partie_finie"]:
        # ── Phase J1 : Drones ──────────────────────────────────────────────────
        _phase_drones(etat)
        if etat["partie_finie"]:
            break

        # ── Phase J2 : Tempêtes (manuelle) ────────────────────────────────────
        _phase_tempetes(etat)
        if etat["partie_finie"]:
            break

        # ── Phase automatique : météo ──────────────────────────────────────────
        logs_meteo = deplacer_tempetes(etat)
        for ligne in logs_meteo:
            etat["historique"].append(ligne)
            enregistrer_log(ligne)

        # Vérification fin de partie après météo (tempêtes peuvent bloquer tous les drones)
        if verifier_fin_partie(etat):
            break

        # ── Propagation zones X ────────────────────────────────────────────────
        logs_x = propager_zones_x(etat)
        for ligne in logs_x:
            etat["historique"].append(ligne)
            enregistrer_log(ligne)

        # ── Vérification fin de partie ─────────────────────────────────────────
        if verifier_fin_partie(etat):
            break

        etat["tour"] += 1

    _afficher_fin(etat)
    sauvegarder_resultats(etat)


def _phase_drones(etat):
    """
    Phase J1 : le joueur déplace jusqu'à MAX_DEPL_DRONE drones.
    Chaque drone ne peut être déplacé qu'une seule fois par tour.
    Les drones déjà présents sur l'hôpital sont rechargés en début de phase.
    """
    depl_effectues = 0
    drones_deplaces = set()
    drones_recharges = set()

    # Recharge automatique des drones stationnaires sur l'hôpital
    logs_recharge = appliquer_recharges_hopital(etat, drones_recharges)
    for ligne in logs_recharge:
        etat["historique"].append(ligne)
        enregistrer_log(ligne)

    while depl_effectues < MAX_DEPL_DRONE:
        render_complet(etat, phase="P1-DRONES",
                       depl_restants=MAX_DEPL_DRONE - depl_effectues)

        # Drones disponibles : ni hors service, ni bloqués, ni batterie vide,
        # ni déjà déplacés ce tour
        drones_dispo = [
            did for did, d in etat["drones"].items()
            if not d["hors_service"]
            and d["bloque"] == 0
            and d["batterie"] > 0
            and did not in drones_deplaces
        ]
        if not drones_dispo:
            print("Aucun drone disponible — passage automatique à J2.")
            break

        print(f"Drones disponibles : {', '.join(drones_dispo)}")
        saisie = input("Choisir un drone (ex: D1) ou 'next' pour passer : ").strip().upper()

        if saisie == 'Q':
            etat["partie_finie"] = True
            return
        if saisie == 'NEXT':
            break

        if saisie not in etat["drones"]:
            print(f"'{saisie}' n'est pas un drone valide. Réessayez.")
            continue
        if saisie in drones_deplaces:
            print(f"{saisie} a déjà été déplacé ce tour.")
            continue

        drone = etat["drones"][saisie]
        if drone["hors_service"]:
            print(f"{saisie} est hors service.")
            continue
        if drone["bloque"] > 0:
            print(f"{saisie} est bloqué ({drone['bloque']} tour(s) restant(s)).")
            continue
        if drone["batterie"] <= 0:
            print(f"{saisie} n'a plus de batterie.")
            continue

        pos_drone = _pos_str((drone["col"], drone["lig"]))
        dest_str = input(f"{saisie} en {pos_drone} → destination (ex: B3) : ").strip()

        cible = position_depuis_chaine(dest_str)
        if cible is None:
            print(f"Destination '{dest_str}' invalide (ex: B3).")
            continue

        ok, raison = valider_mouvement(etat, drone, cible)
        if not ok:
            print(f"Mouvement refusé : {raison}")
            continue

        ligne_log = executer_mouvement(etat, drone, cible, drones_recharges)
        etat["historique"].append(ligne_log)
        enregistrer_log(ligne_log)
        drones_deplaces.add(saisie)
        depl_effectues += 1

        if verifier_fin_partie(etat):
            return


def _phase_tempetes(etat):
    """
    Phase J2 : le joueur déplace jusqu'à MAX_DEPL_TEMPETE tempêtes.
    Chaque tempête ne peut être déplacée qu'une seule fois par tour.
    """
    depl_effectues = 0
    tempetes_deplacees = set()

    while depl_effectues < MAX_DEPL_TEMPETE:
        render_complet(etat, phase="P2-TEMPETES",
                       depl_restants=MAX_DEPL_TEMPETE - depl_effectues)

        tempetes_dispo = [
            tid for tid in etat["tempetes"]
            if tid not in tempetes_deplacees
        ]
        if not tempetes_dispo:
            print("Toutes les tempêtes ont été déplacées.")
            break

        print(f"Tempêtes disponibles : {', '.join(tempetes_dispo)}")
        saisie = input("Choisir une tempête (ex: T1) ou 'next' pour passer : ").strip().upper()

        if saisie == 'Q':
            etat["partie_finie"] = True
            return
        if saisie == 'NEXT':
            break

        if saisie not in etat["tempetes"]:
            print(f"'{saisie}' n'est pas une tempête valide.")
            continue
        if saisie in tempetes_deplacees:
            print(f"{saisie} a déjà été déplacée ce tour.")
            continue

        tempete = etat["tempetes"][saisie]
        pos_t = _pos_str((tempete["col"], tempete["lig"]))
        dest_str = input(f"{saisie} en {pos_t} → destination : ").strip()

        cible = position_depuis_chaine(dest_str)
        if cible is None:
            print(f"Destination '{dest_str}' invalide.")
            continue

        ok, raison = valider_mouvement_tempete(etat, tempete, cible)
        if not ok:
            print(f"Mouvement refusé : {raison}")
            continue

        ligne_log = executer_mouvement_tempete(etat, tempete, cible)
        etat["historique"].append(ligne_log)
        enregistrer_log(ligne_log)
        tempetes_deplacees.add(saisie)
        depl_effectues += 1

        if verifier_fin_partie(etat):
            return


def _afficher_fin(etat):
    """Affiche le message de fin de partie."""
    render_complet(etat)
    print()
    if etat["victoire"]:
        print("*** VICTOIRE ! Tous les survivants ont été sauvés ! ***")
    else:
        sauves = sum(1 for s in etat["survivants"].values() if s["etat"] == "sauve")
        total = len(etat["survivants"])
        print(f"--- Fin de partie. Score final : {etat['score']} pt(s)")
        print(f"    Survivants sauvés : {sauves}/{total}")
    print()
