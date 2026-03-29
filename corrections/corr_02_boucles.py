# ============================================================
# CORRECTION 02 — Boucles et conditions
# ============================================================

batteries      = {"D1": 10, "D2": 8, "D3": 0, "D4": 15, "D5": 0, "D6": 5}
positions      = {"D1": (0,0), "D2": (3,4), "D3": (1,1), "D4": (5,5), "D5": (0,11), "D6": (7,3)}
surv_positions = [(2,3), (4,4), (8,1), (0,7), (11,11)]

# ----------------------------------------------------------
# A1 — for sur un dictionnaire
# ----------------------------------------------------------
# .items() retourne des paires (clé, valeur).
# C'est la façon idiomatique d'itérer un dict en Python.

def afficher_batteries(batteries: dict) -> None:
    for id_drone, bat in batteries.items():
        print(f"{id_drone} : {bat}")

print("--- A1 ---")
afficher_batteries(batteries)

# ----------------------------------------------------------
# A2 — Filtrage avec for + if
# ----------------------------------------------------------
# On accumule les IDs dans une liste de résultats.
# Alternative plus compacte : list comprehension (voir E1).

def drones_actifs(batteries: dict) -> list:
    actifs = []
    for id_drone, bat in batteries.items():
        if bat > 0:
            actifs.append(id_drone)
    return actifs

resultat = drones_actifs(batteries)
assert set(resultat) == {"D1", "D2", "D4", "D6"}
print("A2 OK")

# ----------------------------------------------------------
# B1 — while avec double condition
# ----------------------------------------------------------
# On utilise while car le nombre d'itérations dépend d'une
# condition dynamique (batterie), pas d'un range fixe.
# Le "and" garantit qu'on arrête dès que l'une des deux
# conditions est fausse.

def simuler_deplacements(batterie_init: int, max_depl: int) -> tuple:
    batterie = batterie_init
    nb_depl  = 0
    while batterie > 0 and nb_depl < max_depl:
        batterie -= 1
        nb_depl  += 1
    return batterie, nb_depl

bat, nb = simuler_deplacements(10, 3)
assert bat == 7 and nb == 3
bat, nb = simuler_deplacements(1, 3)
assert bat == 0 and nb == 1
print("B1 OK")

# ----------------------------------------------------------
# C1 — if / elif / else
# ----------------------------------------------------------
# L'ordre des branches est crucial : on vérifie d'abord
# le cas le plus restrictif (== 0) avant les plages.
# Inverser l'ordre donnerait de faux résultats.

def etat_batterie(batterie: int) -> str:
    if batterie == 0:
        return "HS"
    elif batterie <= 5:
        return "critique"
    elif batterie <= 10:
        return "normal"
    else:
        return "plein"

assert etat_batterie(0)  == "HS"
assert etat_batterie(3)  == "critique"
assert etat_batterie(8)  == "normal"
assert etat_batterie(20) == "plein"
print("C1 OK")

# ----------------------------------------------------------
# C2 — Validation multi-conditions
# ----------------------------------------------------------
# On retourne un tuple (bool, str) pour que l'appelant
# sache POURQUOI le déplacement est refusé, pas seulement
# qu'il l'est. Pattern courant en validation.

def deplacement_possible(batterie: int, bloque: bool, depl_effectues: int, max_depl: int) -> tuple:
    if batterie == 0:
        return False, "batterie vide (drone HS)"
    if bloque:
        return False, "drone bloqué par une tempête"
    if depl_effectues >= max_depl:
        return False, f"nombre maximum de déplacements atteint ({max_depl})"
    return True, ""

ok, _ = deplacement_possible(10, False, 0, 3)
assert ok is True
ok, raison = deplacement_possible(0, False, 0, 3)
assert ok is False and "batterie" in raison.lower()
ok, raison = deplacement_possible(5, True, 0, 3)
assert ok is False and "bloqu" in raison.lower()
ok, raison = deplacement_possible(5, False, 3, 3)
assert ok is False
print("C2 OK")

# ----------------------------------------------------------
# D1 — break : arrêt dès qu'on trouve
# ----------------------------------------------------------
# break est ici la solution naturelle : on cherche
# le PREMIER élément qui satisfait une condition.
# Sans break, on continuerait à itérer inutilement.

def premier_surv_gauche(surv_positions: list) -> tuple | None:
    for pos in surv_positions:
        col, ligne = pos
        if col < 6:
            return pos   # équivalent à break + return
    return None

res = premier_surv_gauche(surv_positions)
assert res == (2, 3)
print("D1 OK")

# ----------------------------------------------------------
# D2 — continue : ignorer les drones HS
# ----------------------------------------------------------
# continue saute le reste de l'itération courante.
# Ici on saute les drones avec batterie == 0 pour ne pas
# les additionner. Alternative : if bat > 0: total += bat

def batterie_totale_actifs(batteries: dict) -> int:
    total = 0
    for bat in batteries.values():
        if bat == 0:
            continue   # drone HS, on ignore
        total += bat
    return total

total = batterie_totale_actifs(batteries)
assert total == 10 + 8 + 15 + 5
print("D2 OK")

# ----------------------------------------------------------
# E1 — List comprehension
# ----------------------------------------------------------
# Syntaxe : [expression for variable in iterable if condition]
# Plus concise que la boucle explicite, idiomatique Python.

def drones_actifs_v2(batteries: dict) -> list:
    return [id_d for id_d, bat in batteries.items() if bat > 0]

resultat2 = drones_actifs_v2(batteries)
assert set(resultat2) == {"D1", "D2", "D4", "D6"}
print("E1 OK")

print("\n=== Correction 02 : tous les tests passés ===")
