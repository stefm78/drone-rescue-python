# ============================================================
# EXERCICE 01 — Structures de base
# Module : cours/01_structures_de_base.md
# ============================================================
# Objectif : manipuler variables, types, listes, dictionnaires
# et tuples en contexte Drone Rescue.
# ============================================================

# ----------------------------------------------------------
# PARTIE A — Variables et types
# ----------------------------------------------------------
# Exercice A1
# Créez les variables suivantes en respectant les types indiqués :
#   - nb_drones      : int, valeur 6
#   - batterie_max   : int, valeur 20
#   - batterie_init  : int, valeur 10
#   - proba_prop     : float, valeur 0.3
#   - nom_jeu        : str, valeur "Drone Rescue"
#   - partie_active  : bool, valeur True

# Votre code ici :


# Test A1
assert isinstance(nb_drones, int) and nb_drones == 6, "A1 : nb_drones incorrect"
assert isinstance(batterie_max, int) and batterie_max == 20, "A1 : batterie_max incorrect"
assert isinstance(proba_prop, float), "A1 : proba_prop doit être un float"
assert isinstance(nom_jeu, str), "A1 : nom_jeu doit être une str"
print("A1 OK")

# ----------------------------------------------------------
# Exercice A2
# Calculez la batterie restante après 3 déplacements :
#   - batterie_courante : batterie_init - 3
# Puis affichez : "Batterie : X/20" (avec la valeur réelle)

# Votre code ici :


# Test A2
assert batterie_courante == batterie_init - 3, "A2 : calcul incorrect"
print("A2 OK")

# ----------------------------------------------------------
# PARTIE B — Listes
# ----------------------------------------------------------
# Exercice B1
# Créez la liste ids_drones contenant les chaînes
# "D1", "D2", "D3", "D4", "D5", "D6".

# Votre code ici :


# Test B1
assert ids_drones == ["D1", "D2", "D3", "D4", "D5", "D6"], "B1 : liste incorrecte"
print("B1 OK")

# Exercice B2
# Ajoutez un 7e drone "D7" à la liste ids_drones.
# Puis retirez-le (il n'est présent que pour ce test).

# Votre code ici :


# Test B2
assert "D7" not in ids_drones, "B2 : D7 aurait dû être retiré"
assert len(ids_drones) == 6, "B2 : la liste doit à nouveau contenir 6 éléments"
print("B2 OK")

# Exercice B3
# Créez la liste batteries contenant la batterie_init pour chacun
# des 6 drones (6 fois la même valeur batterie_init).
# Utilisez la multiplication de liste.

# Votre code ici :


# Test B3
assert batteries == [10, 10, 10, 10, 10, 10], "B3 : liste incorrecte"
print("B3 OK")

# ----------------------------------------------------------
# PARTIE C — Dictionnaires
# ----------------------------------------------------------
# Exercice C1
# Créez le dictionnaire drone_d1 représentant le drone D1 :
#   clés : "id", "position", "batterie", "survivant", "bloque"
#   valeurs : "D1", "A1", 10, None, False

# Votre code ici :


# Test C1
assert drone_d1["id"] == "D1", "C1 : id incorrect"
assert drone_d1["batterie"] == 10, "C1 : batterie incorrecte"
assert drone_d1["survivant"] is None, "C1 : survivant doit être None"
print("C1 OK")

# Exercice C2
# Le drone D1 vient de se déplacer vers B2 et a consommé 1 point de batterie.
# Mettez à jour les clés "position" et "batterie" dans drone_d1.

# Votre code ici :


# Test C2
assert drone_d1["position"] == "B2", "C2 : position incorrecte"
assert drone_d1["batterie"] == 9, "C2 : batterie incorrecte après déplacement"
print("C2 OK")

# Exercice C3
# Créez le dictionnaire etat_jeu avec les clés :
#   "tour" → 1
#   "score" → 0
#   "nb_survivants_restants" → 10
#   "partie_terminee" → False

# Votre code ici :


# Test C3
assert etat_jeu["tour"] == 1, "C3 : tour incorrect"
assert etat_jeu["score"] == 0, "C3 : score incorrect"
print("C3 OK")

# ----------------------------------------------------------
# PARTIE D — Tuples
# ----------------------------------------------------------
# Exercice D1
# Une position sur la grille est représentée par un tuple (col, ligne)
# où col est un int (0-11) et ligne est un int (0-11).
# Créez les tuples pos_drone et pos_hopital :
#   pos_drone   : (1, 0)   → colonne B, ligne 1
#   pos_hopital : (0, 11)  → colonne A, ligne 12

# Votre code ici :


# Test D1
assert isinstance(pos_drone, tuple) and len(pos_drone) == 2, "D1 : pos_drone doit être un tuple de 2"
assert pos_hopital == (0, 11), "D1 : pos_hopital incorrecte"
print("D1 OK")

# Exercice D2
# Décomposez pos_drone en deux variables col et ligne
# en utilisant le déballage (unpacking).

# Votre code ici :


# Test D2
assert col == 1 and ligne == 0, "D2 : unpacking incorrect"
print("D2 OK")

print("\n=== Tous les tests de l'exercice 01 sont passés ! ===")
