# =============================================================================
# main.py — Point d'entrée du jeu Drone Rescue
#
# Lancement : python main.py
#
# Ce fichier est le seul à exécuter directement.
# Il initialise la partie et lance la boucle de jeu.
# =============================================================================

from logique import initialiser_partie
from console import boucle_de_jeu
from logger import demarrer_log


def main():
    """Initialise et lance une partie de Drone Rescue."""
    print("=== DRONE RESCUE ===")
    print("Sauvez les survivants avec vos drones !")
    print()

    # Créer le fichier de log
    demarrer_log()

    # Initialiser l'état du jeu (placement aléatoire)
    etat = initialiser_partie()

    # Lancer la boucle principale
    boucle_de_jeu(etat)


if __name__ == '__main__':
    main()
