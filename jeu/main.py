# =============================================================================
# main.py — Point d'entrée du jeu Drone Rescue
#
# Lancement minimal :
#   python main.py
#
# Options disponibles :
#   python main.py --seed 42           # partie reproductible
#   python main.py --grille 15         # grille 15x15
#   python main.py --drones 4          # 4 drones au lieu de 6
#   python main.py --log partie.log    # chemin du fichier log
#
# Ce fichier orchestre la boucle de jeu complète :
#   1. Parsing des arguments CLI (argparse)
#   2. Affichage de l'écran de titre
#   3. Initialisation de la partie
#   4. Boucle de jeu (tour par tour)
#   5. Affichage du bilan final
#   6. Sauvegarde du fichier .log
# =============================================================================

import sys
import os
import argparse

# Ajouter le dossier jeu/ au chemin Python pour les imports
sys.path.insert(0, os.path.dirname(__file__))

import config  # import du module pour pouvoir patcher les constantes
from modeles import EtatJeu
from logique import initialiser_partie, verifier_fin_partie
from console import boucle_saisie
from affichage import render_complet
from logger import sauvegarder_log


# ---------------------------------------------------------------------------
# Parsing des arguments CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    """
    Définit et parse les arguments de la ligne de commande.
    Les valeurs par défaut sont lues depuis config.py.
    """
    parser = argparse.ArgumentParser(
        prog='drone-rescue',
        description='Drone Rescue — jeu de simulation console Python',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Graine aléatoire pour une partie reproductible (ex. : 42)'
    )
    parser.add_argument(
        '--grille',
        type=int,
        default=config.GRILLE_TAILLE,
        metavar='N',
        help='Taille de la grille N×N (min 6, max 26)'
    )
    parser.add_argument(
        '--drones',
        type=int,
        default=config.NB_DRONES,
        metavar='N',
        help='Nombre de drones (1 à 9)'
    )
    parser.add_argument(
        '--log',
        type=str,
        default=config.LOG_FICHIER,
        metavar='FICHIER',
        help='Chemin du fichier journal de partie'
    )
    return parser.parse_args()


def appliquer_args(args: argparse.Namespace) -> None:
    """
    Surcharge les constantes de config.py avec les valeurs CLI.
    Appelé avant toute initialisation de partie.
    """
    # Validation basique
    if not (6 <= args.grille <= 26):
        print(f'[Erreur] --grille doit être entre 6 et 26 (reçu : {args.grille})')
        sys.exit(1)
    if not (1 <= args.drones <= 9):
        print(f'[Erreur] --drones doit être entre 1 et 9 (reçu : {args.drones})')
        sys.exit(1)

    config.GRILLE_TAILLE = args.grille
    config.NB_DRONES     = args.drones
    config.LOG_FICHIER   = args.log

    # Seed aléatoire : on l'applique dès ici pour que l'initialisation soit reproductible
    if args.seed is not None:
        import random
        random.seed(args.seed)
        print(f'  Seed fixé : {args.seed}')


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
  Pilotez vos drones vers les survivants et ramenez-les à l'hôpital (H = A12).
"""


def ecran_titre(args: argparse.Namespace):
    print('\033[2J\033[H', end='')  # Effacer l'écran
    print(TITRE)
    print('  ' + '═' * 54)
    print('  Commandes : D1-D6 (sélect. drone)  |  A1-L12 (cible)')
    print('              ok (confirmer)          |  next (tour suiv.)')
    print('              aide (help)             |  q (quitter)')
    print('  ' + '═' * 54)
    # Afficher les paramètres actifs si différents des défauts
    params = []
    if args.seed is not None:
        params.append(f'seed={args.seed}')
    if args.grille != 12:
        params.append(f'grille={args.grille}×{args.grille}')
    if args.drones != 6:
        params.append(f'drones={args.drones}')
    if args.log != 'partie.log':
        params.append(f'log={args.log}')
    if params:
        print(f'  Paramètres actifs : {" | ".join(params)}')
    print()


# ---------------------------------------------------------------------------
# Bilan de fin de partie
# ---------------------------------------------------------------------------

def afficher_bilan(etat: EtatJeu):
    print()
    print('  ' + '═' * 40)
    if etat.victoire:
        print('  ⭐ VICTOIRE ! Tous les survivants ont été sauvés.')
    else:
        print('  ✕ DÉFAITE.')
        if etat.tour > config.NB_TOURS_MAX:
            print(f'  Raison : nombre de tours maximum ({config.NB_TOURS_MAX}) atteint.')
        elif not etat.drones_actifs():
            print('  Raison : tous les drones sont hors service.')
    print()
    print(f'  Score final   : {etat.score} survivant(s) sauvé(s)')
    print(f'  Tours joués   : {etat.tour - 1}/{config.NB_TOURS_MAX}')
    print(f'  Survivants r. : {etat.survivants_restants()} non sauvé(s)')
    print()
    print(f'  Journal de partie sauvegardé dans : {config.LOG_FICHIER}')
    print('  ' + '═' * 40)
    print()


# ---------------------------------------------------------------------------
# Initialisation de la partie
# ---------------------------------------------------------------------------

def initialiser_et_afficher() -> EtatJeu:
    """Initialise la partie et affiche l'écran de début."""
    print('  Initialisation de la partie...')
    etat = initialiser_partie()
    render_complet(etat)
    print()
    input('  [Entrée pour commencer le tour 1]')
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
            break


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def main():
    args = parse_args()
    appliquer_args(args)       # surcharge config.py AVANT toute init

    ecran_titre(args)
    input('  Appuyer sur [Entrée] pour commencer...')

    etat = initialiser_et_afficher()
    boucle_principale(etat)

    afficher_bilan(etat)
    sauvegarder_log(etat)


if __name__ == '__main__':
    main()
