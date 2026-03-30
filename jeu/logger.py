# =============================================================================
# logger.py — Journalisation et sauvegarde des résultats
#
# Deux fichiers sont créés :
#   - partie.log   : journal de tous les événements du jeu
#   - resultats.txt: score et bilan final de la partie
# =============================================================================

import os

_DOSSIER = os.path.dirname(os.path.abspath(__file__))
_CHEMIN_LOG = os.path.join(_DOSSIER, "partie.log")
_CHEMIN_RESULTATS = os.path.join(_DOSSIER, "resultats.txt")


def demarrer_log():
    """Crée (ou recrée) le fichier de log au début de la partie."""
    with open(_CHEMIN_LOG, "w", encoding="utf-8") as f:
        f.write("=== DRONE RESCUE — Journal de partie ===\n")
        f.write("Tour | Entité | Mouvement | Événement\n")
        f.write("-" * 50 + "\n")


def enregistrer_log(ligne):
    """Ajoute une ligne au journal de la partie."""
    with open(_CHEMIN_LOG, "a", encoding="utf-8") as f:
        f.write(ligne + "\n")


def sauvegarder_resultats(etat):
    """
    Enregistre le bilan final dans resultats.txt.
    Conformément aux contraintes du sujet : fichier séparé du journal.
    """
    sauves = sum(1 for s in etat["survivants"].values() if s["etat"] == "sauve")
    total = len(etat["survivants"])
    issue = "VICTOIRE" if etat["victoire"] else "DÉFAITE"

    with open(_CHEMIN_RESULTATS, "w", encoding="utf-8") as f:
        f.write("=== DRONE RESCUE — Résultats ===\n")
        f.write(f"Issue         : {issue}\n")
        f.write(f"Score final   : {etat['score']} pt(s)\n")
        f.write(f"Tours joués   : {etat['tour']}\n")
        f.write(f"Survivants    : {sauves}/{total} sauvés\n")
        f.write("\nDétail drones :\n")
        for d in etat["drones"].values():
            etat_drone = "HS" if d["hors_service"] else "actif"
            f.write(f"  {d['id']} : batterie {d['batterie']}/{d['batterie_max']} — {etat_drone}\n")
