# =============================================================================
# EXERCICE 08 — Console et log
# Module correspondant : cours/08_console_et_log.md
# =============================================================================
# Objectifs :
#   - Parser et valider les commandes saisies par le joueur
#   - Afficher des prompts et gérer la boucle de saisie
#   - Écrire des logs simultanément en mémoire et dans un fichier
#   - Formater les messages de log selon le standard du jeu
# =============================================================================


# -----------------------------------------------------------------------------
# EXERCICE 1 — Parser une commande joueur
# -----------------------------------------------------------------------------
# Le joueur saisit des commandes texte dans le terminal :
#   "D3"   → sélectionner le drone D3
#   "T2"   → sélectionner la tempête T2
#   "E6"   → cible de déplacement (colonne E, ligne 6)
#   "ok"   → confirmer le déplacement
#   "next" → passer au tour suivant
#   "quit" → quitter le jeu
#
# Écris : parser_commande(saisie)
#   → retourne un tuple (type_cmd, valeur)
#   → types possibles : "DRONE", "TEMPETE", "CIBLE", "OK", "NEXT", "QUIT", "INCONNU"
#   → valeur : identifiant ("D3"), position ("E6"), ou None
#
# Règles de parsing :
#   - Ignorer la casse ("d3" == "D3")
#   - Drone : 1 lettre D + 1 chiffre 1-6
#   - Tempête : 1 lettre T + 1 chiffre 1-4
#   - Cible : 1 lettre A-L + 1-2 chiffres 1-12
# -----------------------------------------------------------------------------

import re

def parser_commande(saisie):
    """
    Parse la saisie joueur et retourne (type_commande, valeur).
    """
    # TODO
    # Nettoyer la saisie (strip, upper)
    # Tester dans l'ordre : QUIT, NEXT, OK, DRONE, TEMPETE, CIBLE, INCONNU
    pass


# Tests exercice 1
if __name__ == "__main__":
    print(parser_commande("D3"))    # ("DRONE", "D3")
    print(parser_commande("d3"))    # ("DRONE", "D3")
    print(parser_commande("T2"))    # ("TEMPETE", "T2")
    print(parser_commande("E6"))    # ("CIBLE", "E6")
    print(parser_commande("A12"))   # ("CIBLE", "A12")
    print(parser_commande("ok"))    # ("OK", None)
    print(parser_commande("next"))  # ("NEXT", None)
    print(parser_commande("quit"))  # ("QUIT", None)
    print(parser_commande("xyz"))   # ("INCONNU", "XYZ")


# -----------------------------------------------------------------------------
# EXERCICE 2 — Formater une ligne de log
# -----------------------------------------------------------------------------
# Le format standard du jeu est :
#   T[nn] P[n] [D|T]  [ID] [départ]→[arrivée]  bat:[x→y]  surv:[id|—]  [ÉVÈNEMENT]
#
# Exemples :
#   "T04 P1 D  D3 B7→E6    bat:6→5    surv:—"
#   "T04 P1 D  D2 D5→D5    BLOQUÉ(T2) bat:—   surv:S3"
#   "T05 P1 D  D4 E7→A12   bat:5→4    surv:S3  LIVRAISON +1pt"
#   "T04 P1 T  T1 J2→K2"
#
# Écris : formater_log(tour, phase, type_entite, id_entite,
#                       depart, arrivee, bat_avant=None, bat_apres=None,
#                       survivant=None, evenement="")
#   → retourne la chaîne de log formatée
# -----------------------------------------------------------------------------

def formater_log(tour, phase, type_entite, id_entite,
                 depart, arrivee, bat_avant=None, bat_apres=None,
                 survivant=None, evenement=""):
    """
    Retourne une ligne de log au format standard Drone Rescue.
    tour : int, phase : int, type_entite : "D" ou "T"
    depart, arrivee : str ex "B7", "E6"
    """
    # TODO
    # Format tour : T04 (zfill 2)
    # Format déplacement : "B7→E6"
    # Format batterie : "bat:6→5" ou "bat:—" si bloqué
    # Format survivant : "surv:S3" ou "surv:—"
    pass


# Tests exercice 2
if __name__ == "__main__":
    print(formater_log(4, 1, "D", "D3", "B7", "E6", 6, 5))
    # T04 P1 D  D3 B7→E6    bat:6→5    surv:—
    print(formater_log(5, 1, "D", "D4", "E7", "A12", 5, 4, survivant="S3", evenement="LIVRAISON +1pt"))
    # T05 P1 D  D4 E7→A12   bat:5→4    surv:S3  LIVRAISON +1pt
    print(formater_log(4, 1, "T", "T1", "J2", "K2"))
    # T04 P1 T  T1 J2→K2


# -----------------------------------------------------------------------------
# EXERCICE 3 — Système de log (mémoire + fichier)
# -----------------------------------------------------------------------------
# Dans Drone Rescue, chaque action est loggée simultanément :
#   - Dans une liste Python en mémoire (pour affichage dans le jeu)
#   - Dans un fichier .log (pour relecture après partie)
#
# Crée une classe Logger avec :
#   - __init__(self, nom_fichier="partie.log")
#     → ouvre le fichier en mode écriture (ou crée)
#     → initialise self.historique = []
#   - log(self, message)
#     → ajoute message à self.historique
#     → écrit message + "\n" dans le fichier
#   - get_historique(self, n=10)
#     → retourne les n dernières lignes de self.historique
#   - fermer(self)
#     → ferme le fichier proprement
# -----------------------------------------------------------------------------

class Logger:
    def __init__(self, nom_fichier="partie.log"):
        # TODO
        pass

    def log(self, message):
        # TODO
        pass

    def get_historique(self, n=10):
        # TODO
        pass

    def fermer(self):
        # TODO
        pass


# Tests exercice 3
if __name__ == "__main__":
    import os
    logger = Logger("test_partie.log")
    logger.log("T01 P1 D  D1 A1→B2  bat:10→9  surv:—")
    logger.log("T02 P1 D  D2 C3→D4  bat:8→7   surv:S1  COLLECTE")
    print(logger.get_historique())    # les 2 lignes
    print(logger.get_historique(1))   # dernière ligne seulement
    logger.fermer()
    # Vérifier que le fichier existe
    print(os.path.exists("test_partie.log"))  # True
    with open("test_partie.log") as f:
        contenu = f.read()
    print(contenu)  # les 2 lignes
    os.remove("test_partie.log")  # nettoyage


# -----------------------------------------------------------------------------
# EXERCICE 4 — Boucle de saisie interactive (simulation)
# -----------------------------------------------------------------------------
# La boucle de saisie du jeu demande des commandes au joueur jusqu'à
# recevoir "next" (fin de tour) ou "quit" (quitter).
#
# Écris : simuler_saisie(commandes_joueur)
#   → prend une liste de chaînes (simule l'entrée clavier)
#   → retourne la liste des tuples (type_cmd, valeur) traités
#   → s'arrête quand NEXT ou QUIT est reçu
#   → ignore les commandes INCONNU (les loguer mais continuer)
# -----------------------------------------------------------------------------

def simuler_saisie(commandes_joueur):
    """
    Simule la boucle de saisie avec une liste de commandes pré-définies.
    Retourne la liste des commandes traitées (NEXT/QUIT inclus).
    """
    # TODO : utiliser parser_commande sur chaque élément
    pass


# Tests exercice 4
if __name__ == "__main__":
    cmds = ["D3", "E6", "ok", "D1", "B2", "ok", "next"]
    resultat = simuler_saisie(cmds)
    for cmd in resultat:
        print(cmd)
    # ("DRONE", "D3"), ("CIBLE", "E6"), ("OK", None),
    # ("DRONE", "D1"), ("CIBLE", "B2"), ("OK", None), ("NEXT", None)
