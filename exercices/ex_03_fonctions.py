# ============================================================
# EXERCICE 03 — Fonctions
# Module : cours/03_fonctions.md
# ============================================================
# Objectif : définir et appeler des fonctions avec paramètres,
# valeurs par défaut, return, docstrings et annotations de types.
# ============================================================

# ----------------------------------------------------------
# PARTIE A — Fonctions simples
# ----------------------------------------------------------
# Exercice A1
# Écrivez la fonction distance_chebyshev qui calcule la distance
# de Chebyshev entre deux positions (col1,ligne1) et (col2,ligne2).
# La distance de Chebyshev = max(|dc|, |dl|)
# où dc = col2-col1, dl = ligne2-ligne1.
#
# C'est la distance utilisée dans Drone Rescue pour vérifier
# qu'un déplacement est valide (distance <= 1).

def distance_chebyshev(col1: int, ligne1: int, col2: int, ligne2: int) -> int:
    """
    Retourne la distance de Chebyshev entre deux cases.

    Exemples :
      (0,0) → (1,1) = 1  (diagonal)
      (0,0) → (2,1) = 2
      (3,3) → (3,3) = 0  (même case)
    """
    # Votre code ici
    pass

# Test A1
assert distance_chebyshev(0, 0, 1, 1) == 1, "A1 : diagonal"
assert distance_chebyshev(0, 0, 2, 1) == 2, "A1 : 2 colonnes"
assert distance_chebyshev(3, 3, 3, 3) == 0, "A1 : même case"
assert distance_chebyshev(0, 0, 0, 1) == 1, "A1 : vertical"
print("A1 OK")

# ----------------------------------------------------------
# Exercice A2
# Écrivez la fonction est_dans_grille qui retourne True si
# une position (col, ligne) est dans une grille de taille n x n.
# La grille a des indices de 0 à n-1 inclus.

def est_dans_grille(col: int, ligne: int, taille: int = 12) -> bool:
    """
    Retourne True si (col, ligne) est dans la grille taille x taille.
    Paramètre taille a une valeur par défaut de 12.
    """
    # Votre code ici
    pass

# Test A2
assert est_dans_grille(0, 0)    is True,  "A2 : coin haut-gauche"
assert est_dans_grille(11, 11)  is True,  "A2 : coin bas-droit"
assert est_dans_grille(12, 0)   is False, "A2 : hors grille droite"
assert est_dans_grille(0, -1)   is False, "A2 : hors grille haut"
assert est_dans_grille(5, 5, 6) is True,  "A2 : grille 6x6"
assert est_dans_grille(6, 5, 6) is False, "A2 : hors grille 6x6"
print("A2 OK")

# ----------------------------------------------------------
# PARTIE B — Fonctions avec plusieurs return
# ----------------------------------------------------------
# Exercice B1
# Écrivez la fonction valider_mouvement_drone qui vérifie
# si un drone peut se déplacer vers une cible.
# Conditions :
#   1. La cible est dans la grille (taille=12)
#   2. La distance de Chebyshev <= 1
#   3. La batterie du drone est > 0
#   4. Le drone n'est pas bloqué (bloque=False)
# Retournez (True, "") si valide, (False, message_erreur) sinon.

def valider_mouvement_drone(
    col_src: int, ligne_src: int,
    col_dst: int, ligne_dst: int,
    batterie: int,
    bloque: bool,
    taille: int = 12
) -> tuple:
    """
    Valide un déplacement de drone.
    Retourne (bool, str) : (valide, message_erreur).
    """
    # Votre code ici
    pass

# Test B1
ok, _ = valider_mouvement_drone(0, 0, 1, 1, 10, False)
assert ok is True, "B1 : mouvement diagonal valide"
ok, msg = valider_mouvement_drone(0, 0, 2, 0, 10, False)
assert ok is False and "distance" in msg.lower(), "B1 : trop loin"
ok, msg = valider_mouvement_drone(0, 0, 1, 1, 0, False)
assert ok is False and "batterie" in msg.lower(), "B1 : batterie vide"
ok, msg = valider_mouvement_drone(0, 0, 1, 1, 10, True)
assert ok is False and "bloqu" in msg.lower(), "B1 : drone bloqué"
ok, msg = valider_mouvement_drone(11, 11, 12, 11, 10, False)
assert ok is False and "grille" in msg.lower(), "B1 : hors grille"
print("B1 OK")

# ----------------------------------------------------------
# PARTIE C — Fonctions qui retournent plusieurs valeurs
# ----------------------------------------------------------
# Exercice C1
# Écrivez la fonction deplacer_drone qui exécute un mouvement
# valide et retourne le nouvel état du drone.
# La fonction prend un dictionnaire drone et une position cible.
# Elle retourne un NOUVEAU dictionnaire (ne modifiez pas l'original).
# Consommation : -1 batterie par déplacement.

def deplacer_drone(drone: dict, col_dst: int, ligne_dst: int) -> dict:
    """
    Retourne un nouveau dict drone avec position et batterie mises à jour.
    Ne modifie pas le drone original.
    """
    # Votre code ici
    pass

# Test C1
drone_test = {"id": "D1", "col": 0, "ligne": 0, "batterie": 10, "survivant": None}
nouvel_etat = deplacer_drone(drone_test, 1, 1)
assert nouvel_etat["col"] == 1,        "C1 : col incorrecte"
assert nouvel_etat["ligne"] == 1,      "C1 : ligne incorrecte"
assert nouvel_etat["batterie"] == 9,   "C1 : batterie incorrecte"
assert drone_test["col"] == 0,         "C1 : original ne doit pas être modifié"
assert drone_test["batterie"] == 10,   "C1 : original ne doit pas être modifié"
print("C1 OK")

# ----------------------------------------------------------
# PARTIE D — Fonctions génératrices de données (bonus)
# ----------------------------------------------------------
# Exercice D1
# Écrivez la fonction colonne_vers_index qui convertit
# une lettre de colonne ('A' à 'L') en index 0-based.
# 'A' → 0, 'B' → 1, ..., 'L' → 11
# Retournez -1 si la lettre est invalide.

def colonne_vers_index(lettre: str) -> int:
    """
    Convertit 'A'-'L' en 0-11. Retourne -1 si invalide.
    Astuce : utilisez ord() pour obtenir le code ASCII.
    """
    # Votre code ici
    pass

# Test D1
assert colonne_vers_index("A") == 0,  "D1 : A → 0"
assert colonne_vers_index("L") == 11, "D1 : L → 11"
assert colonne_vers_index("F") == 5,  "D1 : F → 5"
assert colonne_vers_index("Z") == -1, "D1 : invalide"
print("D1 OK")

# Exercice D2
# Écrivez la fonction index_vers_colonne : inverse de D1.
# 0 → 'A', 11 → 'L'. Retourne "?" si index invalide.

def index_vers_colonne(index: int, taille: int = 12) -> str:
    """
    Convertit 0-11 en 'A'-'L'. Retourne '?' si invalide.
    Astuce : utilisez chr().
    """
    # Votre code ici
    pass

# Test D2
assert index_vers_colonne(0)  == "A", "D2 : 0 → A"
assert index_vers_colonne(11) == "L", "D2 : 11 → L"
assert index_vers_colonne(12) == "?", "D2 : invalide"
print("D2 OK")

print("\n=== Tous les tests de l'exercice 03 sont passés ! ===")
