# =============================================================================
# logger.py — Journalisation de la partie Drone Rescue
#
# Le log est condensé : 1 ligne par mouvement validé uniquement.
# Les mouvements invalides ne sont PAS loggés (affichés inline dans console.py).
# =============================================================================

import os
from config import LOG_FICHIER


def log_action(etat, ligne: str):
    """
    Ajoute une ligne à l'historique de l'état (pour l'affichage en temps réel)
    ET l'écrit dans le fichier log.

    N'est appelé que pour les mouvements validés et exécutés.
    """
    etat.historique.append(ligne)
    _ecrire_fichier(ligne)


def sauvegarder_log(etat):
    """
    Écrit l'intégralité du log de partie dans le fichier final.
    (Le fichier est aussi mis à jour en temps réel via log_action.)
    """
    try:
        with open(LOG_FICHIER, 'w', encoding='utf-8') as f:
            f.write(f"=== Drone Rescue — Partie T{etat.tour:02d} | Score {etat.score} ===\n")
            f.write(f"=== {'VICTOIRE' if etat.victoire else 'DÉFAITE'} ===\n\n")
            for ligne in etat.historique:
                f.write(ligne + "\n")
    except OSError as e:
        print(f"  [logger] Impossible d'écrire {LOG_FICHIER} : {e}")


# Fichier log temps réel (mode append, créé à la première action)
_fichier_ouvert = None


def _ecrire_fichier(ligne: str):
    """Écriture temps réel dans le fichier log (append)."""
    global _fichier_ouvert
    try:
        if _fichier_ouvert is None:
            _fichier_ouvert = open(LOG_FICHIER, 'w', encoding='utf-8')
        _fichier_ouvert.write(ligne + "\n")
        _fichier_ouvert.flush()
    except OSError:
        pass  # silencieux en cas d'erreur disque


def fermer_log():
    """Ferme le fichier log temps réel (à appeler en fin de partie)."""
    global _fichier_ouvert
    if _fichier_ouvert:
        try:
            _fichier_ouvert.close()
        except OSError:
            pass
        _fichier_ouvert = None
