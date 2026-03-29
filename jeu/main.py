# =============================================================================
# main.py — Point d'entrée du jeu Drone Rescue
#
# Lancement : python main.py
#
# Ce fichier orchestre la boucle de jeu complète :
#   1. Affichage de l'écran de titre
#   2. Initialisation de la partie
#   3. Boucle de jeu (tour par tour)
#   4. Affichage du bilan final
#   5. Sauvegarde du fichier .log
# =============================================================================

import sys
import os

# Ajouter le dossier jeu/ au chemin Python pour les imports
sys.path.insert(0, os.path.dirname(__file__))

from modeles import EtatJeu
from logique import initialiser_partie, verifier_fin_partie
from console import boucle_saisie
from affichage import render_complet
from logger import sauvegarder_log
from config import NB_TOURS_MAX, LOG_FICHIER


# ---------------------------------------------------------------------------
# Écran de titre
# ---------------------------------------------------------------------------

TITRE = r"""

  ██████╗ ██████╗  ██████╗ ███╗   ██╗███████╗
  ██╔══██╗██╔══██╗██╔═══██╗████╗  ██║██╔════╝
  ██║  ██║██████╔╝██║   ██║██╔██╗ ██║█████╗  
  ██║  ██║██╔══██╗██║   ██║██║╚██╗██║██╔══╝  
  ██████╔╝██║  ██║╚██████╔╝██║ ╚████║███████╗
  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝

  ██████╗ ███████╗███████╗ ██████╗██╗   ██╗███████╗
  ██╔══██╗██╔════╝██╔════╝██╔════╝██║   ██║██╔════╝
  ██████╔╝█████╗  ███████╗██║     ██║   ██║█████╗  
  ██╔══██╗██╔══╝  ╚════██║██║     ██║   ██║██╔══╝  
  ██║  ██║███████╗███████║╚██████╗╚██████╔╝███████╗
  ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝

  Sauvez les survivants avant que les tempêtes ne gagnent.
  Pilotez vos 6 drones vers les survivants et ramenez-les à l'hôpital (H = A12).
"""


def ecran_titre():
    print("\033[2J\033[H", end="")  # Effacer l'écran
    print(TITRE)
    print("  " + "═" * 54)
    print("  Commandes : D1-D6 (sélect. drone)  |  A1-L12 (cible)")
    print("              ok (confirmer)          |  next (tour suiv.)")
    print("              aide (help)             |  q (quitter)")
    print("  " + "═" * 54)
    print()


# ---------------------------------------------------------------------------
# Bilan de fin de partie
# ---------------------------------------------------------------------------

def afficher_bilan(etat: EtatJeu):
    print()
    print("  " + "═" * 40)
    if etat.victoire:
        print("  ⭐ VICTOIRE ! Tous les survivants ont été sauvés.")
    else:
        print("  ✕ DÉFAITE.")
        if etat.tour > NB_TOURS_MAX:
            print(f"  Raison : nombre de tours maximum ({NB_TOURS_MAX}) atteint.")
        elif not etat.drones_actifs():
            print("  Raison : tous les drones sont hors service.")
    print()
    print(f"  Score final   : {etat.score} survivant(s) sauvé(s)")
    print(f"  Tours joués   : {etat.tour - 1}/{NB_TOURS_MAX}")
    print(f"  Survivants r. : {etat.survivants_restants()} non sauvé(s)")
    print()
    print(f"  Journal de partie sauvegardé dans : {LOG_FICHIER}")
    print("  " + "═" * 40)
    print()


# ---------------------------------------------------------------------------
# Initialisation de la partie
# ---------------------------------------------------------------------------

def initialiser_et_afficher() -> EtatJeu:
    """Initialise la partie et affiche l'écran de début."""
    print("  Initialisation de la partie...")
    etat = initialiser_partie()
    render_complet(etat)
    print()
    input("  [Entrée pour commencer le tour 1]")
    return etat


# ---------------------------------------------------------------------------
# Boucle principale
# ---------------------------------------------------------------------------

def boucle_principale(etat: EtatJeu):
    """
    Exécute la boucle de jeu tour par tour.
    Retourne quand la partie est terminée ou que le joueur quitte.
    """
    while not etat.partie_finie:
        continuer = boucle_saisie(etat)
        if not continuer:
            # Le joueur a quitté ou la partie est terminée
            break


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def main():
    ecran_titre()
    input("  Appuyer sur [Entrée] pour commencer...")

    etat = initialiser_et_afficher()
    boucle_principale(etat)

    # Bilan + sauvegarde log
    afficher_bilan(etat)
    sauvegarder_log(etat)


if __name__ == "__main__":
    main()
