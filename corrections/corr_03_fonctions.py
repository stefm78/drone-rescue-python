# ============================================================
# CORRECTION 03 — Fonctions
# ============================================================
# Convention : colonne str 'A'..'L', ligne int 1-based 1..12
# ============================================================

# ----------------------------------------------------------
# A1 — Distance de Chebyshev avec colonnes str
# ----------------------------------------------------------
# ord('A')=65, ord('B')=66… donc |ord(col1)-ord(col2)| donne
# la différence de colonnes en nombre de cases.
# On prend le max des deux différences absolues.

def distance_chebyshev(col1: str, lig1: int, col2: str, lig2: int) -> int:
    """Distance de Chebyshev entre deux cases."""
    dc = abs(ord(col1) - ord(col2))
    dl = abs(lig1 - lig2)
    return max(dc, dl)

assert distance_chebyshev('A', 1, 'B', 2) == 1
assert distance_chebyshev('A', 1, 'C', 2) == 2
assert distance_chebyshev('D', 5, 'D', 5) == 0
assert distance_chebyshev('A', 1, 'A', 2) == 1
print("A1 OK")

# ----------------------------------------------------------
# A2 — coord_valide avec construction dynamique des colonnes
# ----------------------------------------------------------
# On construit la liste des colonnes valides avec chr().
# chr(ord('A') + i) donne 'A', 'B', ..., 'L' pour i in range(12).
# La ligne est 1-based : valide entre 1 et taille inclus.

def coord_valide(colonne: str, ligne: int, taille: int = 12) -> bool:
    """True si la position est dans la grille taille×taille."""
    cols_valides = [chr(ord('A') + i) for i in range(taille)]
    return colonne in cols_valides and 1 <= ligne <= taille

assert coord_valide('A', 1)    is True
assert coord_valide('L', 12)   is True
assert coord_valide('M', 1)    is False
assert coord_valide('A', 0)    is False
assert coord_valide('A', 13)   is False
assert coord_valide('F', 6, 6) is True
assert coord_valide('G', 1, 6) is False
print("A2 OK")

# ----------------------------------------------------------
# B1 — Validation composée
# ----------------------------------------------------------
# Ordre : batterie → blocage → grille → distance.
# On retourne (False, motif) dès qu'une règle est violée.
# Les messages contiennent les mots-clés testés par les assert.

def valider_mouvement_drone(
    col_src: str, lig_src: int,
    col_dst: str, lig_dst: int,
    batterie: int,
    bloque: bool,
    taille: int = 12
) -> tuple:
    """Valide un déplacement de drone. Retourne (bool, str)."""
    if batterie == 0:
        return False, "batterie vide (drone HS)"
    if bloque:
        return False, "drone bloqué par une tempête"
    if not coord_valide(col_dst, lig_dst, taille):
        return False, "cible hors grille"
    dist = distance_chebyshev(col_src, lig_src, col_dst, lig_dst)
    if dist > 1:
        return False, f"distance trop grande ({dist} > 1)"
    return True, ""

ok, _ = valider_mouvement_drone('A', 1, 'B', 2, 10, False)
assert ok is True
ok, msg = valider_mouvement_drone('A', 1, 'C', 1, 10, False)
assert ok is False and 'distance' in msg.lower()
ok, msg = valider_mouvement_drone('A', 1, 'B', 2, 0, False)
assert ok is False and 'batterie' in msg.lower()
ok, msg = valider_mouvement_drone('A', 1, 'B', 2, 10, True)
assert ok is False and 'bloqu' in msg.lower()
ok, msg = valider_mouvement_drone('L', 12, 'M', 12, 10, False)
assert ok is False and 'grille' in msg.lower()
print("B1 OK")

# ----------------------------------------------------------
# C1 — Ne pas modifier l'original : dict.copy()
# ----------------------------------------------------------
# dict.copy() crée une copie superficielle : suffisant ici
# car les valeurs sont toutes immuables (str, int, None).
# On modifie les clés 'colonne', 'ligne', 'batterie' sur la copie.

def deplacer_drone(drone: dict, col_dst: str, lig_dst: int) -> dict:
    """Retourne un nouveau dict drone avec position et batterie mises à jour."""
    nouveau = drone.copy()
    nouveau['colonne']  = col_dst
    nouveau['ligne']    = lig_dst
    nouveau['batterie'] -= 1
    return nouveau

drone_test = {'id': 'D1', 'colonne': 'A', 'ligne': 1, 'batterie': 10, 'survivant': None}
nouvel_etat = deplacer_drone(drone_test, 'B', 2)
assert nouvel_etat['colonne']  == 'B'
assert nouvel_etat['batterie'] == 9
assert drone_test['colonne']   == 'A'   # original intact
assert drone_test['batterie']  == 10
print("C1 OK")

# ----------------------------------------------------------
# D1 — ord() et chr()
# ----------------------------------------------------------
# ord('A') = 65. ord(lettre) - ord('A') donne l'offset 0-based.
# On vérifie que la lettre est dans la plage 'A'..'L' (12 lettres).

def colonne_vers_index(lettre: str) -> int:
    """Convertit 'A'-'L' en 0-11. Retourne -1 si invalide."""
    if len(lettre) != 1:
        return -1
    lettre = lettre.upper()
    idx = ord(lettre) - ord('A')
    return idx if 0 <= idx < 12 else -1

assert colonne_vers_index('A') == 0
assert colonne_vers_index('L') == 11
assert colonne_vers_index('F') == 5
assert colonne_vers_index('Z') == -1
print("D1 OK")

# ----------------------------------------------------------
# D2 — chr() : inverse de ord()
# ----------------------------------------------------------

def index_vers_colonne(index: int, taille: int = 12) -> str:
    """Convertit 0-11 en 'A'-'L'. Retourne '?' si invalide."""
    return chr(ord('A') + index) if 0 <= index < taille else '?'

assert index_vers_colonne(0)  == 'A'
assert index_vers_colonne(11) == 'L'
assert index_vers_colonne(12) == '?'
print("D2 OK")

print("\n=== Correction 03 : tous les tests passés ===")
