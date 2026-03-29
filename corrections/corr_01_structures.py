# ============================================================
# CORRECTION 01 — Structures de base
# ============================================================
# Chaque réponse est commentée pour expliquer les choix.
# ============================================================

# ----------------------------------------------------------
# PARTIE A — Variables et types
# ----------------------------------------------------------

# A1 — On déclare les variables avec le type attendu.
# En Python, pas de mot-clé de type : le type est inféré à
# la création. Les constantes sont par convention en MAJUSCULES,
# mais pour un exercice de débutant on reste en minuscules.
nb_drones     = 6       # int  : nombre entier
batterie_max  = 20      # int
batterie_init = 10      # int
proba_prop    = 0.3     # float : nombre décimal
nom_jeu       = "Drone Rescue"  # str
partie_active = True    # bool

assert isinstance(nb_drones, int) and nb_drones == 6
assert isinstance(batterie_max, int) and batterie_max == 20
assert isinstance(proba_prop, float)
assert isinstance(nom_jeu, str)
print("A1 OK")

# A2 — Soustraction simple. On réutilise batterie_init
# plutôt que de hardcoder 10 : si on change batterie_init,
# le calcul reste juste.
batterie_courante = batterie_init - 3   # 10 - 3 = 7
print(f"Batterie : {batterie_courante}/20")

assert batterie_courante == batterie_init - 3
print("A2 OK")

# ----------------------------------------------------------
# PARTIE B — Listes
# ----------------------------------------------------------

# B1 — Liste littérale. On aurait pu générer avec une
# list comprehension mais la liste littérale est plus lisible
# ici car les IDs ne suivent pas une règle arithmétique stricte.
ids_drones = ["D1", "D2", "D3", "D4", "D5", "D6"]
assert ids_drones == ["D1", "D2", "D3", "D4", "D5", "D6"]
print("B1 OK")

# B2 — append() ajoute en fin de liste, remove() retire la
# première occurrence. On aurait pu utiliser pop() si on
# connaissait l'index, mais remove() est plus lisible.
ids_drones.append("D7")
assert "D7" in ids_drones   # vérification intermédiaire
ids_drones.remove("D7")
assert "D7" not in ids_drones
assert len(ids_drones) == 6
print("B2 OK")

# B3 — [valeur] * n est le moyen idiomatique de créer une liste
# avec n fois la même valeur. Equivalent à [batterie_init for _ in range(6)]
# mais plus court.
batteries = [batterie_init] * 6   # [10, 10, 10, 10, 10, 10]
assert batteries == [10, 10, 10, 10, 10, 10]
print("B3 OK")

# ----------------------------------------------------------
# PARTIE C — Dictionnaires
# ----------------------------------------------------------

# C1 — Dictionnaire avec des clés de types mixtes en valeurs
# (str, int, None, bool). None représente "aucun survivant à bord".
# C'est préférable à 0 ou "" car None est explicitement "absent".
drone_d1 = {
    "id"       : "D1",
    "position" : "A1",
    "batterie" : 10,
    "survivant": None,   # None = pas de survivant à bord
    "bloque"   : False
}
assert drone_d1["id"] == "D1"
assert drone_d1["batterie"] == 10
assert drone_d1["survivant"] is None
print("C1 OK")

# C2 — Mise à jour de deux clés. On accède directement par clé.
# -=  est un raccourci pour  drone_d1["batterie"] = drone_d1["batterie"] - 1
drone_d1["position"]  = "B2"
drone_d1["batterie"] -= 1   # 10 - 1 = 9
assert drone_d1["position"] == "B2"
assert drone_d1["batterie"] == 9
print("C2 OK")

# C3 — Dictionnaire d'état de jeu. Toutes les valeurs sont
# initialisées à leur valeur de départ de partie.
etat_jeu = {
    "tour"                  : 1,
    "score"                 : 0,
    "nb_survivants_restants": 10,
    "partie_terminee"       : False
}
assert etat_jeu["tour"] == 1
assert etat_jeu["score"] == 0
print("C3 OK")

# ----------------------------------------------------------
# PARTIE D — Tuples
# ----------------------------------------------------------

# D1 — Tuple (col, ligne) avec indices 0-based.
# On utilise un tuple et non une liste car une position est
# une valeur immuable : on ne modifie pas les coordonnées d'une
# case, on crée un nouveau tuple pour chaque nouvelle position.
pos_drone   = (1, 0)    # col=1 (B), ligne=0 (1ère ligne)
pos_hopital = (0, 11)   # col=0 (A), ligne=11 (12ème ligne)
assert isinstance(pos_drone, tuple) and len(pos_drone) == 2
assert pos_hopital == (0, 11)
print("D1 OK")

# D2 — Unpacking (déballage) : Python permet d'assigner les
# éléments d'un tuple à plusieurs variables en une ligne.
# C'est plus lisible que col = pos_drone[0] ; ligne = pos_drone[1]
col, ligne = pos_drone
assert col == 1 and ligne == 0
print("D2 OK")

print("\n=== Correction 01 : tous les tests passés ===")
