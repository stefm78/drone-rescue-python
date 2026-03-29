# ============================================================
# CORRECTION 03 — Fonctions
# ============================================================

# ----------------------------------------------------------
# A1 — Distance de Chebyshev
# ----------------------------------------------------------
# max(|dc|, |dl|) : la plus grande différence entre les axes.
# C'est la distance "roi aux échecs" : un déplacement diagonal
# compte pour 1, pas pour sqrt(2).

def distance_chebyshev(col1: int, ligne1: int, col2: int, ligne2: int) -> int:
    """Distance de Chebyshev entre deux cases."""
    return max(abs(col2 - col1), abs(ligne2 - ligne1))

assert distance_chebyshev(0, 0, 1, 1) == 1
assert distance_chebyshev(0, 0, 2, 1) == 2
assert distance_chebyshev(3, 3, 3, 3) == 0
assert distance_chebyshev(0, 0, 0, 1) == 1
print("A1 OK")

# ----------------------------------------------------------
# A2 — est_dans_grille avec valeur par défaut
# ----------------------------------------------------------
# 0 <= x < taille pour chaque axe.
# On utilise un paramètre par défaut taille=12 pour pouvoir
# tester avec d'autres tailles sans casser l'interface habituelle.

def est_dans_grille(col: int, ligne: int, taille: int = 12) -> bool:
    """True si la position est dans la grille taille x taille."""
    return 0 <= col < taille and 0 <= ligne < taille

assert est_dans_grille(0, 0)    is True
assert est_dans_grille(11, 11)  is True
assert est_dans_grille(12, 0)   is False
assert est_dans_grille(0, -1)   is False
assert est_dans_grille(5, 5, 6) is True
assert est_dans_grille(6, 5, 6) is False
print("A2 OK")

# ----------------------------------------------------------
# B1 — Validation composée
# ----------------------------------------------------------
# On vérifie les conditions dans un ordre logique :
# d'abord les conditions sur la cible, puis sur la source.
# Chaque condition a son propre message d'erreur spécifique.

def valider_mouvement_drone(
    col_src: int, ligne_src: int,
    col_dst: int, ligne_dst: int,
    batterie: int,
    bloque: bool,
    taille: int = 12
) -> tuple:
    """Valide un déplacement de drone. Retourne (bool, str)."""
    if batterie == 0:
        return False, "batterie vide (drone HS)"
    if bloque:
        return False, "drone bloqué par une tempête"
    if not est_dans_grille(col_dst, ligne_dst, taille):
        return False, "cible hors grille"
    dist = distance_chebyshev(col_src, ligne_src, col_dst, ligne_dst)
    if dist > 1:
        return False, f"distance trop grande ({dist} > 1)"
    return True, ""

ok, _ = valider_mouvement_drone(0, 0, 1, 1, 10, False)
assert ok is True
ok, msg = valider_mouvement_drone(0, 0, 2, 0, 10, False)
assert ok is False and "distance" in msg.lower()
ok, msg = valider_mouvement_drone(0, 0, 1, 1, 0, False)
assert ok is False and "batterie" in msg.lower()
ok, msg = valider_mouvement_drone(0, 0, 1, 1, 10, True)
assert ok is False and "bloqu" in msg.lower()
ok, msg = valider_mouvement_drone(11, 11, 12, 11, 10, False)
assert ok is False and "grille" in msg.lower()
print("B1 OK")

# ----------------------------------------------------------
# C1 — Ne pas modifier l'original : copie du dict
# ----------------------------------------------------------
# On crée un nouveau dictionnaire avec dict.copy() ou {**drone}.
# Modifier l'original serait un effet de bord non voulu.

def deplacer_drone(drone: dict, col_dst: int, ligne_dst: int) -> dict:
    """Retourne un nouveau dict drone avec position et batterie mises à jour."""
    nouveau = drone.copy()          # copie superficielle du dict
    nouveau["col"]      = col_dst
    nouveau["ligne"]    = ligne_dst
    nouveau["batterie"] -= 1
    return nouveau

drone_test = {"id": "D1", "col": 0, "ligne": 0, "batterie": 10, "survivant": None}
nouvel_etat = deplacer_drone(drone_test, 1, 1)
assert nouvel_etat["col"] == 1
assert nouvel_etat["batterie"] == 9
assert drone_test["col"] == 0      # original intact
assert drone_test["batterie"] == 10
print("C1 OK")

# ----------------------------------------------------------
# D1 — ord() et chr()
# ----------------------------------------------------------
# ord('A') = 65 en ASCII. ord(lettre) - ord('A') donne l'offset.
# On vérifie que la lettre est dans la plage valide avant.

def colonne_vers_index(lettre: str) -> int:
    """Convertit 'A'-'L' en 0-11. Retourne -1 si invalide."""
    if len(lettre) != 1:
        return -1
    lettre = lettre.upper()
    idx = ord(lettre) - ord("A")
    if 0 <= idx < 12:
        return idx
    return -1

assert colonne_vers_index("A") == 0
assert colonne_vers_index("L") == 11
assert colonne_vers_index("F") == 5
assert colonne_vers_index("Z") == -1
print("D1 OK")

# ----------------------------------------------------------
# D2 — chr() : inverse de ord()
# ----------------------------------------------------------
# chr(65) = 'A'. On ajoute l'index à ord('A').

def index_vers_colonne(index: int, taille: int = 12) -> str:
    """Convertit 0-11 en 'A'-'L'. Retourne '?' si invalide."""
    if 0 <= index < taille:
        return chr(ord("A") + index)
    return "?"

assert index_vers_colonne(0)  == "A"
assert index_vers_colonne(11) == "L"
assert index_vers_colonne(12) == "?"
print("D2 OK")

print("\n=== Correction 03 : tous les tests passés ===")
