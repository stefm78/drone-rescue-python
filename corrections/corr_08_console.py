# =============================================================================
# CORRECTION 08 — Console et log
# =============================================================================
# Pas de classes, pas de régex. Logger = fonctions + dict.
# =============================================================================


LETTRES = list("ABCDEFGHIJKL")


# -----------------------------------------------------------------------------
# EXERCICE 1 — Parser une commande joueur (sans re)
# -----------------------------------------------------------------------------

def parser_commande(saisie):
    """
    Parse sans régex. Retourne (type_commande, valeur).
    """
    s = saisie.strip().upper()

    # Mots-clés fixes d'abord
    if s == "QUIT":  return ("QUIT",    None)
    if s == "NEXT":  return ("NEXT",    None)
    if s == "OK":    return ("OK",      None)

    # Drone : D + chiffre 1-6
    if len(s) == 2 and s[0] == "D" and s[1] in "123456":
        return ("DRONE", s)

    # Tempête : T + chiffre 1-4
    if len(s) == 2 and s[0] == "T" and s[1] in "1234":
        return ("TEMPETE", s)

    # Cible : lettre A-L + entier 1-12
    if len(s) >= 2 and s[0] in LETTRES:
        try:
            lig_jeu = int(s[1:])          # ex : "6" -> 6, "12" -> 12
            if 1 <= lig_jeu <= 12:
                col = LETTRES.index(s[0]) # "A"->0, "B"->1, ...
                lig = lig_jeu - 1         # passage en 0-basé
                return ("CIBLE", (col, lig))
        except ValueError:
            pass   # s[1:] n'est pas un entier -> INCONNU

    return ("INCONNU", s)


if __name__ == "__main__":
    assert parser_commande("D3")   == ("DRONE",   "D3")
    assert parser_commande("d3")   == ("DRONE",   "D3")
    assert parser_commande("T2")   == ("TEMPETE", "T2")
    assert parser_commande("E6")   == ("CIBLE",   (4, 5))
    assert parser_commande("A12")  == ("CIBLE",   (0, 11))
    assert parser_commande("ok")   == ("OK",    None)
    assert parser_commande("next") == ("NEXT",  None)
    assert parser_commande("quit") == ("QUIT",  None)
    assert parser_commande("xyz")[0]  == "INCONNU"
    assert parser_commande("Z9")[0]   == "INCONNU"   # Z hors A-L
    print("Ex1 OK")


# -----------------------------------------------------------------------------
# EXERCICE 2 — Formater une ligne de log
# -----------------------------------------------------------------------------

def formater_log(tour, phase, type_entite, id_entite,
                 col_dep, lig_dep, col_arr, lig_arr,
                 bat_avant=None, bat_apres=None,
                 survivant=None, evenement=""):
    """Retourne une ligne de log au format standard Drone Rescue."""
    t_str  = f"T{tour:02d} P{phase} {type_entite}  {id_entite}"
    dep    = f"({col_dep},{lig_dep})"
    arr    = f"({col_arr},{lig_arr})"
    mouv   = f"{dep}→{arr}"

    if type_entite == "T":
        # Les tempêtes n'ont pas de section batterie ni survivant
        return f"{t_str} {mouv}"

    bat_str  = f"bat:{bat_avant}→{bat_apres}" if bat_avant is not None else ""
    surv_str = f"surv:{survivant}" if survivant else "surv:—"
    parts    = [t_str, mouv]
    if bat_str:
        parts.append(bat_str.ljust(10))
    parts.append(surv_str)
    if evenement:
        parts.append(evenement)
    return "  ".join(parts)


if __name__ == "__main__":
    ligne1 = formater_log(4, 1, "D", "D3", 1, 6, 4, 5, 6, 5)
    print(ligne1)
    ligne2 = formater_log(5, 1, "D", "D4", 4, 6, 0, 11, 5, 4,
                          survivant="S3", evenement="LIVRAISON +1pt")
    print(ligne2)
    ligne3 = formater_log(4, 1, "T", "T1", 9, 1, 10, 2)
    print(ligne3)
    print("Ex2 OK")


# -----------------------------------------------------------------------------
# EXERCICE 3 — Logger : fonctions + dict
# -----------------------------------------------------------------------------

def demarrer_log(nom_fichier="partie.log"):
    """Crée le dict logger et ouvre le fichier en mode append."""
    return {
        "historique"  : [],
        "nom_fichier" : nom_fichier,
        # On ouvre en 'a' pour ne pas écraser un log précédent
        "fichier"     : open(nom_fichier, "a", encoding="utf-8"),
    }


def enregistrer_log(logger, message):
    """Ajoute le message à l'historique et écrit dans le fichier."""
    logger["historique"].append(message)
    logger["fichier"].write(message + "\n")
    logger["fichier"].flush()  # force l'écriture immédiate sur disque


def get_historique(logger, n=10):
    """Retourne les n dernières lignes de l'historique."""
    return logger["historique"][-n:]  # slicing : [-10:] sur une liste


def fermer_log(logger):
    """Ferme proprement le fichier."""
    logger["fichier"].close()


if __name__ == "__main__":
    import os
    log = demarrer_log("test_partie.log")
    enregistrer_log(log, "T01 P1 D  D1 (0,0)→(1,1)  bat:10→9  surv:—")
    enregistrer_log(log, "T02 P1 D  D2 (2,2)→(3,3)  bat:8→7   surv:S1  COLLECTE")
    assert len(get_historique(log)) == 2
    assert get_historique(log, 1)[0].startswith("T02")
    fermer_log(log)
    assert os.path.exists("test_partie.log")
    with open("test_partie.log", encoding="utf-8") as f:
        contenu = f.read()
    assert "T01" in contenu and "T02" in contenu
    os.remove("test_partie.log")
    print("Ex3 OK")


# -----------------------------------------------------------------------------
# EXERCICE 4 — Boucle de saisie simulée
# -----------------------------------------------------------------------------

def simuler_saisie(commandes_joueur):
    """
    Simule la boucle de saisie.
    S'arrête à NEXT ou QUIT (inclus dans le résultat).
    """
    traites = []
    for saisie in commandes_joueur:
        cmd = parser_commande(saisie)
        traites.append(cmd)
        if cmd[0] in ("NEXT", "QUIT"):
            break   # fin de tour ou quitter
    return traites


if __name__ == "__main__":
    cmds = ["D3", "E6", "ok", "D1", "B2", "ok", "next"]
    resultat = simuler_saisie(cmds)
    assert resultat[-1] == ("NEXT", None)
    assert len(resultat) == 7
    for cmd in resultat:
        print(cmd)
    print("Ex4 OK")
