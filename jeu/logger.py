# =============================================================================
# logger.py — Journal des actions de la partie
#
# Fonctions :
#   log_action(etat, texte)     -> None
#       Enregistre une ligne dans etat.historique ET dans le fichier .log
#
#   sauvegarder_log(etat)       -> None
#       Écrit tout l'historique dans le fichier LOG_FICHIER
#
#   charger_log(chemin)         -> list[str]
#       Lit un fichier .log et retourne les lignes
# =============================================================================

from config import LOG_FICHIER


def log_action(etat, texte: str):
    """
    Ajoute 'texte' à etat.historique (liste en mémoire)
    et l'écrit immédiatement dans le fichier de log (mode append).

    Paramètres
    ----------
    etat  : EtatJeu  — l'état courant de la partie
    texte : str      — la ligne à enregistrer
    """
    etat.historique.append(texte)
    try:
        with open(LOG_FICHIER, 'a', encoding='utf-8') as f:
            f.write(texte + '\n')
    except OSError as e:
        # En cas d'échec d'écriture disque, on continue sans planter le jeu
        print(f"[logger] Impossible d'écrire dans {LOG_FICHIER} : {e}")


def sauvegarder_log(etat):
    """
    Écrit l'intégralité de etat.historique dans LOG_FICHIER.
    Utile pour réécrire le log complet en fin de partie.

    Paramètres
    ----------
    etat : EtatJeu
    """
    try:
        with open(LOG_FICHIER, 'w', encoding='utf-8') as f:
            f.write('\n'.join(etat.historique))
            f.write('\n')
    except OSError as e:
        print(f"[logger] Impossible de sauvegarder {LOG_FICHIER} : {e}")


def charger_log(chemin: str = LOG_FICHIER) -> list:
    """
    Lit un fichier .log existant et retourne la liste des lignes.
    Utile pour afficher l'historique d'une partie précédente.

    Paramètres
    ----------
    chemin : str  — chemin vers le fichier (défaut : LOG_FICHIER)

    Retourne
    --------
    list[str] : liste des lignes, vide si fichier inexistant
    """
    try:
        with open(chemin, 'r', encoding='utf-8') as f:
            return [ligne.rstrip('\n') for ligne in f.readlines()]
    except FileNotFoundError:
        return []
    except OSError as e:
        print(f"[logger] Erreur lecture {chemin} : {e}")
        return []
