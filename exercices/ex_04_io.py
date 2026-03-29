# ============================================================
# EXERCICE 04 — Modules et I/O fichiers
# Module : cours/04_modules_et_io.md
# ============================================================
# Objectif : lire et écrire des fichiers, utiliser os.path,
# gérer les exceptions liées aux fichiers.
# Dans Drone Rescue, chaque action est logée dans un fichier .log.
# ============================================================

import os

# ----------------------------------------------------------
# PARTIE A — Écriture dans un fichier
# ----------------------------------------------------------
# Exercice A1
# Écrivez la fonction creer_fichier_log qui crée (ou écrase)
# un fichier texte au chemin indiqué et y écrit une ligne d'en-tête :
#   "=== DRONE RESCUE — Partie du [horodatage] ===\n"
# où [horodatage] est une chaîne passée en paramètre.
# La fonction ne retourne rien.

def creer_fichier_log(chemin: str, horodatage: str) -> None:
    """
    Crée le fichier de log et y écrit l'en-tête.
    Utilisez open() en mode 'w' et encoding='utf-8'.
    """
    # Votre code ici
    pass

# Test A1
chemin_test = "test_partie.log"
creer_fichier_log(chemin_test, "2026-03-29 20:00")
assert os.path.exists(chemin_test), "A1 : le fichier doit exister"
with open(chemin_test, encoding="utf-8") as f:
    contenu = f.read()
assert "DRONE RESCUE" in contenu, "A1 : en-tête manquant"
assert "2026-03-29 20:00" in contenu, "A1 : horodatage manquant"
print("A1 OK")

# ----------------------------------------------------------
# Exercice A2
# Écrivez la fonction ajouter_ligne_log qui ajoute une ligne
# à la fin d'un fichier existant (mode 'a').
# La ligne doit se terminer par \n.

def ajouter_ligne_log(chemin: str, ligne: str) -> None:
    """
    Ajoute une ligne à la fin du fichier.
    Utilisez open() en mode 'a' et encoding='utf-8'.
    """
    # Votre code ici
    pass

# Test A2
ajouter_ligne_log(chemin_test, "T01 P1 D  D1 A1→B2  bat:10→9")
ajouter_ligne_log(chemin_test, "T01 P1 D  D2 C3→D4  bat:8→7")
with open(chemin_test, encoding="utf-8") as f:
    lignes = f.readlines()
assert len(lignes) == 3, f"A2 : attendu 3 lignes, obtenu {len(lignes)}"
assert "D1" in lignes[1], "A2 : ligne D1 manquante"
print("A2 OK")

# ----------------------------------------------------------
# PARTIE B — Lecture d'un fichier
# ----------------------------------------------------------
# Exercice B1
# Écrivez la fonction lire_historique qui retourne la liste
# de toutes les lignes du fichier (sans '\n' final).
# Excluez les lignes qui commencent par '=' (lignes d'en-tête).

def lire_historique(chemin: str) -> list:
    """
    Retourne la liste des lignes de log (sans \\n, sans en-têtes '===').
    """
    # Votre code ici
    pass

# Test B1
historique = lire_historique(chemin_test)
assert len(historique) == 2, f"B1 : attendu 2 lignes, obtenu {len(historique)}"
assert historique[0].endswith("bat:10→9"), "B1 : contenu ligne 1 incorrect"
print("B1 OK")

# ----------------------------------------------------------
# PARTIE C — Gestion des erreurs
# ----------------------------------------------------------
# Exercice C1
# Écrivez la fonction lire_historique_safe qui fait la même chose
# que lire_historique mais retourne une liste vide si le fichier
# n'existe pas (FileNotFoundError) au lieu de planter.

def lire_historique_safe(chemin: str) -> list:
    """
    Comme lire_historique, mais retourne [] si fichier absent.
    Utilisez try / except FileNotFoundError.
    """
    # Votre code ici
    pass

# Test C1
resultat_absent = lire_historique_safe("fichier_inexistant.log")
assert resultat_absent == [], "C1 : doit retourner [] si fichier absent"
resultat_present = lire_historique_safe(chemin_test)
assert len(resultat_present) == 2, "C1 : fichier présent : doit lire normalement"
print("C1 OK")

# ----------------------------------------------------------
# PARTIE D — os.path et gestion de chemins
# ----------------------------------------------------------
# Exercice D1
# Écrivez la fonction nom_fichier_log qui génère le chemin
# complet d'un fichier de log à partir d'un dossier et d'un
# identifiant de partie :
#   dossier="logs", partie_id="001"  →  "logs/partie_001.log"
# Utilisez os.path.join pour construire le chemin.

def nom_fichier_log(dossier: str, partie_id: str) -> str:
    """
    Retourne le chemin : dossier/partie_XXX.log
    """
    # Votre code ici
    pass

# Test D1
chemin_genere = nom_fichier_log("logs", "001")
assert "logs" in chemin_genere, "D1 : dossier manquant"
assert "partie_001.log" in chemin_genere, "D1 : nom de fichier incorrect"
print("D1 OK")

# Exercice D2
# Écrivez la fonction creer_dossier_si_absent qui crée le
# dossier donné s'il n'existe pas déjà.
# Utilisez os.makedirs(chemin, exist_ok=True).

def creer_dossier_si_absent(chemin: str) -> None:
    """
    Crée le dossier (et les parents) s'il n'existe pas.
    """
    # Votre code ici
    pass

# Test D2
creer_dossier_si_absent("logs_test")
assert os.path.isdir("logs_test"), "D2 : dossier non créé"
creer_dossier_si_absent("logs_test")  # doit ne pas planter si déjà présent
print("D2 OK")

# Nettoyage des fichiers de test
import shutil
os.remove(chemin_test)
shutil.rmtree("logs_test", ignore_errors=True)
print("\n=== Tous les tests de l'exercice 04 sont passés ! ===")
