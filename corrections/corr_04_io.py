# ============================================================
# CORRECTION 04 — Modules et I/O fichiers
# ============================================================

import os
import shutil

# ----------------------------------------------------------
# A1 — Création du fichier de log
# ----------------------------------------------------------
# Mode 'w' : écrase le fichier s'il existe, le crée sinon.
# On force encoding='utf-8' pour éviter les problèmes de
# caractères spéciaux (é, à, tirets...) sur Windows.
# Le gestionnaire de contexte 'with' ferme automatiquement
# le fichier même en cas d'exception.

def creer_fichier_log(chemin: str, horodatage: str) -> None:
    """Crée le fichier de log et y écrit l'en-tête."""
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(f"=== DRONE RESCUE — Partie du {horodatage} ===\n")

chemin_test = "test_partie_corr.log"
creer_fichier_log(chemin_test, "2026-03-29 20:00")
assert os.path.exists(chemin_test)
with open(chemin_test, encoding="utf-8") as f:
    contenu = f.read()
assert "DRONE RESCUE" in contenu
assert "2026-03-29 20:00" in contenu
print("A1 OK")

# ----------------------------------------------------------
# A2 — Ajout en mode append
# ----------------------------------------------------------
# Mode 'a' : n'efface pas, ajoute à la suite.
# On s'assure que la ligne se termine par \n pour que
# chaque entrée soit sur sa propre ligne.

def ajouter_ligne_log(chemin: str, ligne: str) -> None:
    """Ajoute une ligne à la fin du fichier."""
    with open(chemin, "a", encoding="utf-8") as f:
        f.write(ligne + "\n")

ajouter_ligne_log(chemin_test, "T01 P1 D  D1 A1→B2  bat:10→9")
ajouter_ligne_log(chemin_test, "T01 P1 D  D2 C3→D4  bat:8→7")
with open(chemin_test, encoding="utf-8") as f:
    lignes = f.readlines()
assert len(lignes) == 3
assert "D1" in lignes[1]
print("A2 OK")

# ----------------------------------------------------------
# B1 — Lecture et filtrage
# ----------------------------------------------------------
# .strip() supprime les \n et espaces en début/fin.
# On filtre les lignes d'en-tête qui commencent par '='.

def lire_historique(chemin: str) -> list:
    """Retourne les lignes de log (sans \\n, sans en-têtes)."""
    with open(chemin, encoding="utf-8") as f:
        return [
            ligne.strip()
            for ligne in f
            if not ligne.startswith("=")  # exclure les en-têtes
        ]

historique = lire_historique(chemin_test)
assert len(historique) == 2
assert historique[0].endswith("bat:10→9")
print("B1 OK")

# ----------------------------------------------------------
# C1 — try / except
# ----------------------------------------------------------
# FileNotFoundError est levée quand on ouvre un fichier absent.
# On l'attrape et on retourne [] pour que l'appelant n'ait
# pas besoin de vérifier l'existence du fichier au préalable.

def lire_historique_safe(chemin: str) -> list:
    """Comme lire_historique, mais retourne [] si fichier absent."""
    try:
        return lire_historique(chemin)
    except FileNotFoundError:
        return []

resultat_absent = lire_historique_safe("fichier_inexistant.log")
assert resultat_absent == []
resultat_present = lire_historique_safe(chemin_test)
assert len(resultat_present) == 2
print("C1 OK")

# ----------------------------------------------------------
# D1 — os.path.join
# ----------------------------------------------------------
# os.path.join gère automatiquement les séparateurs selon
# le système d'exploitation (/ sur Linux/Mac, \\ sur Windows).
# Ne jamais concaténer des chemins avec des +.

def nom_fichier_log(dossier: str, partie_id: str) -> str:
    """Retourne le chemin complet du fichier de log."""
    nom = f"partie_{partie_id}.log"
    return os.path.join(dossier, nom)

chemin_genere = nom_fichier_log("logs", "001")
assert "logs" in chemin_genere
assert "partie_001.log" in chemin_genere
print("D1 OK")

# ----------------------------------------------------------
# D2 — os.makedirs avec exist_ok
# ----------------------------------------------------------
# exist_ok=True évite l'exception si le dossier existe déjà.
# makedirs crée aussi les dossiers parents manquants
# (contrairement à os.mkdir).

def creer_dossier_si_absent(chemin: str) -> None:
    """Crée le dossier (et les parents) s'il n'existe pas."""
    os.makedirs(chemin, exist_ok=True)

creer_dossier_si_absent("logs_test_corr")
assert os.path.isdir("logs_test_corr")
creer_dossier_si_absent("logs_test_corr")   # pas d'exception
print("D2 OK")

# Nettoyage
os.remove(chemin_test)
shutil.rmtree("logs_test_corr", ignore_errors=True)

print("\n=== Correction 04 : tous les tests passés ===")
