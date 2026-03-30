# =============================================================================
# EXERCICE 08 — Console et log
# Module correspondant : cours/08_console_et_log.md
# =============================================================================
# Objectifs :
#   - Parser les commandes joueur sans régex (opérations de chaînes)
#   - Valider et exécuter selon le pattern parser → valider → exécuter
#   - Écrire un log simultanément en mémoire (liste) et dans un fichier
#   - Formater les lignes de log au standard du jeu
# =============================================================================
# Pas de classe : le logger est implémenté avec des fonctions et un dict.
# Pas de régex : on utilise .strip(), .upper(), .isdigit(), len(), indexation.
# =============================================================================


# -----------------------------------------------------------------------------
# EXERCICE 1 — Parser une commande joueur (sans re)
# -----------------------------------------------------------------------------
# Le joueur saisit des commandes texte :
#   "D3"   → ("DRONE",   "D3")
#   "T2"   → ("TEMPETE", "T2")
#   "E6"   → ("CIBLE",   (4, 5))    # col=4 (E=4), lig=5 (6-1=5)
#   "ok"   → ("OK",    None)
#   "next" → ("NEXT",  None)
#   "quit" → ("QUIT",  None)
#   autre  → ("INCONNU", saisie_normalisée)
#
# Règles de parsing (sans re) :
#   - .strip().upper() d'abord
#   - Drone : len==2, s[0]=="D", s[1] dans "123456"
#   - Tempête : len==2, s[0]=="T", s[1] dans "1234"
#   - Cible : s[0] lettre A-L, s[1:] chiffres intérieurs à 1-12
#     (utiliser try/except ValueError sur int(s[1:]))
# -----------------------------------------------------------------------------

LETTRES = list("ABCDEFGHIJKL")

def parser_commande(saisie):
    """
    Parse la saisie joueur sans régex.
    Retourne (type_commande, valeur).
    """
    # TODO
    # 1. s = saisie.strip().upper()
    # 2. Tester QUIT, NEXT, OK en premier
    # 3. Tester DRONE, TEMPETE
    # 4. Tester CIBLE : s[0] dans LETTRES + try int(s[1:])
    # 5. Sinon : ("INCONNU", s)
    pass


# Tests exercice 1
if __name__ == "__main__":
    print(parser_commande("D3"))    # ("DRONE",   "D3")
    print(parser_commande("d3"))    # ("DRONE",   "D3")
    print(parser_commande("T2"))    # ("TEMPETE", "T2")
    print(parser_commande("E6"))    # ("CIBLE",   (4, 5))  # col 4, lig 5
    print(parser_commande("A12"))   # ("CIBLE",   (0, 11)) # col 0, lig 11
    print(parser_commande("ok"))    # ("OK",    None)
    print(parser_commande("next"))  # ("NEXT",  None)
    print(parser_commande("quit"))  # ("QUIT",  None)
    print(parser_commande("xyz"))   # ("INCONNU", "XYZ")
    print(parser_commande("Z9"))    # ("INCONNU", "Z9")  Z pas dans A-L


# -----------------------------------------------------------------------------
# EXERCICE 2 — Formater une ligne de log
# -----------------------------------------------------------------------------
# Format standard :
#   T[nn] P[n] [D|T]  [ID] [départ]  [arrivée]  bat:[avant]→[après]  surv:[id|—]  [EVENT]
#
# Exemples :
#   "T04 P1 D  D3 (1,6)→(4,5)  bat:6→5    surv:—"
#   "T05 P1 D  D4 (4,6)→(0,11) bat:5→4    surv:S3  LIVRAISON +1pt"
#   "T04 P1 T  T1 (9,1)→(10,2)"
#
# Écris : formater_log(tour, phase, type_entite, id_entite,
#                       col_dep, lig_dep, col_arr, lig_arr,
#                       bat_avant=None, bat_apres=None,
#                       survivant=None, evenement="")
#   → retourne la chaîne de log
# -----------------------------------------------------------------------------

def formater_log(tour, phase, type_entite, id_entite,
                 col_dep, lig_dep, col_arr, lig_arr,
                 bat_avant=None, bat_apres=None,
                 survivant=None, evenement=""):
    """
    Retourne une ligne de log au format standard Drone Rescue.
    """
    # TODO
    # Format tour  : f"T{tour:02d}"
    # Format dépl  : f"({col_dep},{lig_dep})→({col_arr},{lig_arr})"
    # Format bat   : f"bat:{bat_avant}→{bat_apres}" ou omis si None
    # Format surv  : f"surv:{survivant}" ou "surv:—" si None
    # Tempete : pas de bat ni surv
    pass


# Tests exercice 2
if __name__ == "__main__":
    print(formater_log(4, 1, "D", "D3", 1, 6, 4, 5, 6, 5))
    # T04 P1 D  D3 (1,6)→(4,5)  bat:6→5    surv:—

    print(formater_log(5, 1, "D", "D4", 4, 6, 0, 11, 5, 4,
                       survivant="S3", evenement="LIVRAISON +1pt"))
    # T05 P1 D  D4 (4,6)→(0,11) bat:5→4    surv:S3  LIVRAISON +1pt

    print(formater_log(4, 1, "T", "T1", 9, 1, 10, 2))
    # T04 P1 T  T1 (9,1)→(10,2)


# -----------------------------------------------------------------------------
# EXERCICE 3 — Logger : fonctions + dict (sans classe)
# -----------------------------------------------------------------------------
# Le logger est un dictionnaire contenant l'état :
#   {"historique": [], "fichier": None, "nom_fichier": "partie.log"}
#
# Écris les fonctions :
#   demarrer_log(nom_fichier="partie.log") → retourne le dict logger
#   enregistrer_log(logger, message) → ajoute à historique + écrit fichier
#   get_historique(logger, n=10) → retourne les n dernières lignes
#   fermer_log(logger) → ferme le fichier
# -----------------------------------------------------------------------------

def demarrer_log(nom_fichier="partie.log"):
    """
    Crée et retourne un dict logger. Ouvre le fichier en mode 'a'.
    """
    # TODO
    pass


def enregistrer_log(logger, message):
    """
    Ajoute le message à logger["historique"] et l'écrit dans le fichier.
    """
    # TODO
    pass


def get_historique(logger, n=10):
    """
    Retourne les n dernières lignes de l'historique.
    """
    # TODO
    pass


def fermer_log(logger):
    """
    Ferme proprement le fichier de log.
    """
    # TODO
    pass


# Tests exercice 3
if __name__ == "__main__":
    import os
    log = demarrer_log("test_partie.log")
    enregistrer_log(log, "T01 P1 D  D1 (0,0)→(1,1)  bat:10→9  surv:—")
    enregistrer_log(log, "T02 P1 D  D2 (2,2)→(3,3)  bat:8→7   surv:S1  COLLECTE")
    print(get_historique(log))    # les 2 lignes
    print(get_historique(log, 1)) # dernière ligne seulement
    fermer_log(log)
    print(os.path.exists("test_partie.log"))  # True
    with open("test_partie.log", encoding="utf-8") as f:
        print(f.read())
    os.remove("test_partie.log")   # nettoyage


# -----------------------------------------------------------------------------
# EXERCICE 4 — Boucle de saisie simulée
# -----------------------------------------------------------------------------
# La boucle de saisie lit les commandes et les traite jusqu'à NEXT ou QUIT.
#
# Écris : simuler_saisie(commandes_joueur)
#   → prend une liste de chaînes (simule le clavier)
#   → retourne la liste des tuples (type, valeur) traités
#   → s'arrête quand NEXT ou QUIT est reçu (inclus dans la liste)
#   → les INCONNU sont inclus dans la liste (on les garde pour le log)
# -----------------------------------------------------------------------------

def simuler_saisie(commandes_joueur):
    """
    Simule la boucle de saisie avec des commandes pré-définies.
    Retourne la liste des commandes traitées jusqu'à NEXT ou QUIT inclus.
    """
    # TODO : utiliser parser_commande et une boucle for ou while
    pass


# Tests exercice 4
if __name__ == "__main__":
    cmds = ["D3", "E6", "ok", "D1", "B2", "ok", "next"]
    for cmd in simuler_saisie(cmds):
        print(cmd)
    # ("DRONE", "D3")
    # ("CIBLE", (4, 5))
    # ("OK", None)
    # ("DRONE", "D1")
    # ("CIBLE", (1, 1))
    # ("OK", None)
    # ("NEXT", None)
