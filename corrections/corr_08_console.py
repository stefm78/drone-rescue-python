# =============================================================================
# CORRECTION 08 — Console et log
# Module correspondant : cours/08_console_et_log.md
# =============================================================================

import re
import os


# -----------------------------------------------------------------------------
# CORRECTION 1 — Parser une commande joueur
# -----------------------------------------------------------------------------
# On normalise la saisie (strip + upper) puis on teste dans l'ordre :
# QUIT, NEXT, OK (mots-clés fixes), DRONE (D1-D6), TEMPETE (T1-T4),
# CIBLE (A-L + 1-12), et INCONNU comme cas par défaut.
# On utilise re.fullmatch pour s'assurer que la saisie correspond exactement.
# -----------------------------------------------------------------------------

def parser_commande(saisie):
    """
    Parse la saisie joueur et retourne (type_commande, valeur).
    Insensible à la casse.
    """
    s = saisie.strip().upper()

    if s == "QUIT":
        return ("QUIT", None)
    if s == "NEXT":
        return ("NEXT", None)
    if s == "OK":
        return ("OK", None)

    # Drone : D suivi d'un chiffre 1-6
    if re.fullmatch(r'D[1-6]', s):
        return ("DRONE", s)

    # Tempête : T suivi d'un chiffre 1-4
    if re.fullmatch(r'T[1-4]', s):
        return ("TEMPETE", s)

    # Cible : lettre A-L suivie d'un nombre 1-12
    m = re.fullmatch(r'([A-L])(1[0-2]|[1-9])', s)
    if m:
        return ("CIBLE", s)

    return ("INCONNU", s)


# Tests
if __name__ == "__main__":
    print(parser_commande("D3"))    # ('DRONE', 'D3')
    print(parser_commande("d3"))    # ('DRONE', 'D3')
    print(parser_commande("T2"))    # ('TEMPETE', 'T2')
    print(parser_commande("E6"))    # ('CIBLE', 'E6')
    print(parser_commande("A12"))   # ('CIBLE', 'A12')
    print(parser_commande("ok"))    # ('OK', None)
    print(parser_commande("next"))  # ('NEXT', None)
    print(parser_commande("quit"))  # ('QUIT', None)
    print(parser_commande("xyz"))   # ('INCONNU', 'XYZ')


# -----------------------------------------------------------------------------
# CORRECTION 2 — Formater une ligne de log
# -----------------------------------------------------------------------------
# Le format attendu :
#   T[nn] P[n] [D|T]  [ID] [départ]→[arrivée]  bat:[x→y]  surv:[id|—]  [ÉVÈNEMENT]
# Les tempêtes n'affichent pas la batterie ni le survivant.
# Pour les drones bloqués, bat affiche "—" (bat_avant ou bat_apres peut être None).
# -----------------------------------------------------------------------------

def formater_log(tour, phase, type_entite, id_entite,
                 depart, arrivee, bat_avant=None, bat_apres=None,
                 survivant=None, evenement=""):
    """
    Retourne une ligne de log au format standard Drone Rescue.
    """
    # Numéro de tour sur 2 chiffres
    t_str = f"T{str(tour).zfill(2)}"
    p_str = f"P{phase}"
    dep_str = f"{depart}→{arrivee}"

    base = f"{t_str} {p_str} {type_entite}  {id_entite} {dep_str}"

    if type_entite == "T":
        # Les tempêtes n'ont ni batterie ni survivant dans le log
        ligne = base
    else:
        # Batterie
        if bat_avant is not None and bat_apres is not None:
            bat_str = f"bat:{bat_avant}→{bat_apres}"
        else:
            bat_str = "bat:—"

        # Survivant
        surv_str = f"surv:{survivant}" if survivant else "surv:—"

        ligne = f"{base}    {bat_str}    {surv_str}"

    if evenement:
        ligne = f"{ligne}  {evenement}"

    return ligne


# Tests
if __name__ == "__main__":
    print(formater_log(4, 1, "D", "D3", "B7", "E6", 6, 5))
    # T04 P1 D  D3 B7→E6    bat:6→5    surv:—
    print(formater_log(5, 1, "D", "D4", "E7", "A12", 5, 4, survivant="S3", evenement="LIVRAISON +1pt"))
    # T05 P1 D  D4 E7→A12   bat:5→4    surv:S3  LIVRAISON +1pt
    print(formater_log(4, 1, "T", "T1", "J2", "K2"))
    # T04 P1 T  T1 J2→K2


# -----------------------------------------------------------------------------
# CORRECTION 3 — Classe Logger
# -----------------------------------------------------------------------------
# On ouvre le fichier en mode 'w' dès l'initialisation (crée ou écrase).
# log() écrit simultanément en mémoire (liste) et dans le fichier (flush immédiat).
# get_historique(n) retourne les n derniers éléments avec une slice.
# fermer() appelle f.close() pour libérer les ressources.
# -----------------------------------------------------------------------------

class Logger:
    def __init__(self, nom_fichier="partie.log"):
        self.historique = []
        self.fichier = open(nom_fichier, 'w', encoding='utf-8')

    def log(self, message):
        """Enregistre le message en mémoire et dans le fichier."""
        self.historique.append(message)
        self.fichier.write(message + "\n")
        self.fichier.flush()  # écriture immédiate sur disque

    def get_historique(self, n=10):
        """Retourne les n dernières lignes de l'historique."""
        return self.historique[-n:]

    def fermer(self):
        """Ferme proprement le fichier de log."""
        self.fichier.close()


# Tests
if __name__ == "__main__":
    logger = Logger("test_partie.log")
    logger.log("T01 P1 D  D1 A1→B2  bat:10→9  surv:—")
    logger.log("T02 P1 D  D2 C3→D4  bat:8→7   surv:S1  COLLECTE")
    print(logger.get_historique())    # les 2 lignes
    print(logger.get_historique(1))   # dernière ligne seulement
    logger.fermer()
    print(os.path.exists("test_partie.log"))  # True
    with open("test_partie.log", encoding='utf-8') as f:
        contenu = f.read()
    print(contenu)
    os.remove("test_partie.log")  # nettoyage


# -----------------------------------------------------------------------------
# CORRECTION 4 — Boucle de saisie (simulation)
# -----------------------------------------------------------------------------
# On itère sur la liste de commandes, on parse chaque entrée.
# On ajoute le tuple au résultat, et on s'arrête dès NEXT ou QUIT.
# Les commandes INCONNU sont ajoutées mais ne stoppent pas la boucle.
# -----------------------------------------------------------------------------

def simuler_saisie(commandes_joueur):
    """
    Simule la boucle de saisie avec des commandes pré-définies.
    Retourne la liste des tuples (type_cmd, valeur) traités jusqu'à NEXT/QUIT.
    """
    traitees = []
    for saisie in commandes_joueur:
        cmd = parser_commande(saisie)
        traitees.append(cmd)
        if cmd[0] in ("NEXT", "QUIT"):
            break  # fin de tour ou sortie du jeu
    return traitees


# Tests
if __name__ == "__main__":
    cmds = ["D3", "E6", "ok", "D1", "B2", "ok", "next"]
    resultat = simuler_saisie(cmds)
    for cmd in resultat:
        print(cmd)
    # ('DRONE', 'D3'), ('CIBLE', 'E6'), ('OK', None),
    # ('DRONE', 'D1'), ('CIBLE', 'B2'), ('OK', None), ('NEXT', None)
