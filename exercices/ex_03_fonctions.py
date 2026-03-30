# ============================================================
# EXERCICE 03 — Fonctions
# Module : cours/03_fonctions.md
# ============================================================
# Objectifs :
#   - Définir et appeler des fonctions avec paramètres
#   - Utiliser les valeurs par défaut et les type hints
#   - Écrire des docstrings
#   - Retourner plusieurs valeurs (tuple)
# ============================================================
#
# Convention du projet (à respecter dans tout cet exercice) :
#   colonne : str  lettre majuscule 'A'..'L'
#   ligne   : int  entier 1-based   1..12
# ============================================================

# ----------------------------------------------------------
# PARTIE A — Fonctions simples
# ----------------------------------------------------------
# Exercice A1
# Écrivez la fonction distance_chebyshev qui calcule la distance
# de Chebyshev entre deux positions (col1, lig1) et (col2, lig2).
#
# Rappel :
#   distance = max(|Δcol|, |Δlig|)
#   Pour les colonnes : |ord(col1) - ord(col2)|  (ord('A')=65, ord('B')=66…)
#
# C'est la distance utilisée dans Drone Rescue pour vérifier
# qu'un déplacement est valide (distance == 1 autorisé).

def distance_chebyshev(col1: str, lig1: int, col2: str, lig2: int) -> int:
    """
    Retourne la distance de Chebyshev entre deux cases.

    Exemples :
      ('A',1) → ('B',2) = 1  (diagonal)
      ('A',1) → ('C',2) = 2
      ('D',5) → ('D',5) = 0  (même case)
    """
    # Votre code ici
    pass

# Tests A1
assert distance_chebyshev('A', 1, 'B', 2) == 1, "A1 : diagonal"
assert distance_chebyshev('A', 1, 'C', 2) == 2, "A1 : 2 colonnes"
assert distance_chebyshev('D', 5, 'D', 5) == 0, "A1 : même case"
assert distance_chebyshev('A', 1, 'A', 2) == 1, "A1 : vertical"
print("A1 OK")

# ----------------------------------------------------------
# Exercice A2
# Écrivez la fonction coord_valide qui retourne True si
# la coordonnée (colonne, ligne) est dans la grille.
#
# Règles :
#   colonne doit être dans 'A'..'L' (les taille premières lettres)
#   ligne   doit être entre 1 et taille inclus

def coord_valide(colonne: str, ligne: int, taille: int = 12) -> bool:
    """
    Retourne True si (colonne, ligne) est dans la grille taille×taille.
    Paramètre taille a une valeur par défaut de 12.
    Astuce : construire la liste des colonnes valides avec chr() et range().
    """
    # Votre code ici
    pass

# Tests A2
assert coord_valide('A', 1)    is True,  "A2 : coin haut-gauche"
assert coord_valide('L', 12)   is True,  "A2 : coin bas-droit"
assert coord_valide('M', 1)    is False, "A2 : colonne hors grille"
assert coord_valide('A', 0)    is False, "A2 : ligne 0 invalide"
assert coord_valide('A', 13)   is False, "A2 : ligne 13 invalide"
assert coord_valide('F', 6, 6) is True,  "A2 : grille 6x6"
assert coord_valide('G', 1, 6) is False, "A2 : colonne G hors grille 6x6"
print("A2 OK")

# ----------------------------------------------------------
# PARTIE B — Fonctions avec plusieurs return
# ----------------------------------------------------------
# Exercice B1
# Écrivez la fonction valider_mouvement_drone qui vérifie
# si un drone peut se déplacer vers une cible.
#
# Conditions (dans cet ordre) :
#   1. La batterie du drone est > 0
#   2. Le drone n'est pas bloqué (bloque == False)
#   3. La cible est dans la grille (utiliser coord_valide)
#   4. La distance de Chebyshev entre départ et cible == 1
#
# Retournez (True, "") si valide, (False, message_erreur) sinon.
# Le message doit contenir : "batterie", "bloqu", "grille" ou "distance"
# selon le cas (les tests vérifient ces mots-clés).

def valider_mouvement_drone(
    col_src: str, lig_src: int,
    col_dst: str, lig_dst: int,
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

# Tests B1
ok, _ = valider_mouvement_drone('A', 1, 'B', 2, 10, False)
assert ok is True, "B1 : mouvement diagonal valide"
ok, msg = valider_mouvement_drone('A', 1, 'C', 1, 10, False)
assert ok is False and 'distance' in msg.lower(), "B1 : trop loin"
ok, msg = valider_mouvement_drone('A', 1, 'B', 2, 0, False)
assert ok is False and 'batterie' in msg.lower(), "B1 : batterie vide"
ok, msg = valider_mouvement_drone('A', 1, 'B', 2, 10, True)
assert ok is False and 'bloqu' in msg.lower(), "B1 : drone bloqué"
ok, msg = valider_mouvement_drone('L', 12, 'M', 12, 10, False)
assert ok is False and 'grille' in msg.lower(), "B1 : hors grille"
print("B1 OK")

# ----------------------------------------------------------
# PARTIE C — Fonctions qui retournent plusieurs valeurs
# ----------------------------------------------------------
# Exercice C1
# Écrivez la fonction deplacer_drone qui exécute un mouvement
# valide et retourne le nouvel état du drone.
#
# La fonction prend un dictionnaire drone et une position cible.
# Elle retourne un NOUVEAU dictionnaire (ne modifiez pas l'original).
# Consommation : -1 batterie par déplacement.
#
# Structure du dict drone :
#   {'id': 'D1', 'colonne': 'A', 'ligne': 1, 'batterie': 10, 'survivant': None}

def deplacer_drone(drone: dict, col_dst: str, lig_dst: int) -> dict:
    """
    Retourne un nouveau dict drone avec position et batterie mises à jour.
    Ne modifie pas le drone original.
    Astuce : utiliser dict.copy() puis modifier les clés.
    """
    # Votre code ici
    pass

# Tests C1
drone_test = {'id': 'D1', 'colonne': 'A', 'ligne': 1, 'batterie': 10, 'survivant': None}
nouvel_etat = deplacer_drone(drone_test, 'B', 2)
assert nouvel_etat['colonne']  == 'B',  "C1 : colonne incorrecte"
assert nouvel_etat['ligne']    == 2,    "C1 : ligne incorrecte"
assert nouvel_etat['batterie'] == 9,    "C1 : batterie incorrecte"
assert drone_test['colonne']   == 'A',  "C1 : original ne doit pas être modifié"
assert drone_test['batterie']  == 10,   "C1 : original ne doit pas être modifié"
print("C1 OK")

# ----------------------------------------------------------
# PARTIE D — Conversions de coordonnées
# ----------------------------------------------------------
# Exercice D1
# Écrivez la fonction colonne_vers_index qui convertit
# une lettre de colonne ('A' à 'L') en index 0-based.
# 'A' → 0, 'B' → 1, ..., 'L' → 11
# Retournez -1 si la lettre est invalide.

def colonne_vers_index(lettre: str) -> int:
    """
    Convertit 'A'-'L' en 0-11. Retourne -1 si invalide.
    Astuce : utiliser ord() pour obtenir le code ASCII.
    """
    # Votre code ici
    pass

# Tests D1
assert colonne_vers_index('A') == 0,  "D1 : A → 0"
assert colonne_vers_index('L') == 11, "D1 : L → 11"
assert colonne_vers_index('F') == 5,  "D1 : F → 5"
assert colonne_vers_index('Z') == -1, "D1 : invalide"
print("D1 OK")

# Exercice D2
# Écrivez la fonction index_vers_colonne : inverse de D1.
# 0 → 'A', 11 → 'L'. Retourne '?' si index invalide.

def index_vers_colonne(index: int, taille: int = 12) -> str:
    """
    Convertit 0-11 en 'A'-'L'. Retourne '?' si invalide.
    Astuce : utiliser chr().
    """
    # Votre code ici
    pass

# Tests D2
assert index_vers_colonne(0)  == 'A', "D2 : 0 → A"
assert index_vers_colonne(11) == 'L', "D2 : 11 → L"
assert index_vers_colonne(12) == '?', "D2 : invalide"
print("D2 OK")

print("\n=== Tous les tests de l'exercice 03 sont passés ! ===")
