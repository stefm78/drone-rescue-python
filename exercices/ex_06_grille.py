# =============================================================================
# EXERCICE 06 — Grille et affichage
# Module correspondant : cours/06_grille_et_affichage.md
# =============================================================================
# Objectifs :
#   - Créer et manipuler une grille 2D avec des listes imbriquées
#   - Positionner des entités sur la grille
#   - Afficher la grille en console avec coordonnées
#   - Calculer la distance de Chebyshev
# =============================================================================


# -----------------------------------------------------------------------------
# EXERCICE 1 — Créer une grille vide
# -----------------------------------------------------------------------------
# La grille de Drone Rescue est une liste de listes.
# grille[lig][col] = contenu de la case.
# col et lig sont des entiers 0-basés (0 à taille-1).
#
# Écris creer_grille(taille=8) qui retourne
# une liste de listes remplie de '.'.
# -----------------------------------------------------------------------------

def creer_grille(taille=8):
    """
    Retourne une grille taille×taille remplie de '.'.
    grille[lig][col] avec col, lig entiers 0-basés.
    """
    # TODO : utiliser une list comprehension imbriquée
    pass


# Tests exercice 1
if __name__ == "__main__":
    g = creer_grille()
    print(len(g))        # 8
    print(len(g[0]))     # 8
    print(g[0][0])       # .
    print(g[7][7])       # .


# -----------------------------------------------------------------------------
# EXERCICE 2 — Placer et lire une entité sur la grille
# -----------------------------------------------------------------------------
# Écris deux fonctions :
#   placer(grille, col, lig, symbole)
#     → place le symbole sur grille[lig][col]
#   lire(grille, col, lig)
#     → retourne le contenu de grille[lig][col]
#
# col et lig sont des entiers 0-basés.
# -----------------------------------------------------------------------------

def placer(grille, col, lig, symbole):
    # TODO
    pass


def lire(grille, col, lig):
    # TODO
    pass


# Tests exercice 2
if __name__ == "__main__":
    g = creer_grille()
    placer(g, 0, 7, "H")   # Hôpital en col=0, lig=7
    placer(g, 3, 2, "D")   # Drone en col=3, lig=2
    placer(g, 6, 4, "S")   # Survivant en col=6, lig=4
    print(lire(g, 0, 7))   # H
    print(lire(g, 3, 2))   # D
    print(lire(g, 1, 0))   # .


# -----------------------------------------------------------------------------
# EXERCICE 3 — Afficher la grille
# -----------------------------------------------------------------------------
# Écris afficher_grille(grille) qui affiche :
#
#      0   1   2   3  ...  7
#  0   .   .   .   D  ...  .
#  1   .   .   .   .  ...  .
#  ...
#  7   H   .   .   .  ...  .
#
# Chaque case occupe 4 caractères (ljust(4)).
# Les numéros de ligne sont alignés à droite sur 3 caractères (rjust(3)).
# Pas de codes de couleur ANSI.
# -----------------------------------------------------------------------------

def afficher_grille(grille):
    """
    Affiche la grille avec en-tête des colonnes et numéros de ligne.
    """
    # TODO : afficher l'en-tête des colonnes
    # TODO : pour chaque ligne lig, afficher le numéro puis les cases
    pass


# Tests exercice 3
if __name__ == "__main__":
    g = creer_grille()
    placer(g, 0, 7, "H")
    placer(g, 3, 2, "D")
    placer(g, 6, 4, "S")
    placer(g, 2, 3, "X")
    afficher_grille(g)


# -----------------------------------------------------------------------------
# EXERCICE 4 — Distance de Chebyshev
# -----------------------------------------------------------------------------
# La distance de Chebyshev entre deux cases est :
#   max(|col1 - col2|, |lig1 - lig2|)
#
# Avec des diagonales autorisées, un drone peut atteindre
# n'importe laquelle des 8 cases adjacentes en 1 déplacement.
#
# Écris distance_chebyshev(col1, lig1, col2, lig2) -> int
# -----------------------------------------------------------------------------

def distance_chebyshev(col1, lig1, col2, lig2):
    """
    Retourne la distance de Chebyshev entre (col1, lig1) et (col2, lig2).
    """
    # TODO
    pass


# Tests exercice 4
if __name__ == "__main__":
    print(distance_chebyshev(0, 0, 0, 0))   # 0 (même case)
    print(distance_chebyshev(0, 0, 1, 1))   # 1 (diagonale)
    print(distance_chebyshev(0, 0, 1, 0))   # 1 (horizontal)
    print(distance_chebyshev(0, 0, 0, 3))   # 3 (vertical)
    print(distance_chebyshev(2, 3, 5, 7))   # 4 (max(3, 4))
    print(distance_chebyshev(0, 0, 7, 7))   # 7 (diagonale coin)


# -----------------------------------------------------------------------------
# EXERCICE 5 — Cases à portée de 1 déplacement
# -----------------------------------------------------------------------------
# Écris cases_adjacentes(col, lig, taille=8) qui retourne
# la liste de tuples (col, lig) de toutes les cases à distance Chebyshev = 1,
# en restant dans les limites [0, taille-1].
# -----------------------------------------------------------------------------

def cases_adjacentes(col, lig, taille=8):
    """
    Retourne la liste des cases voisines (distance Chebyshev = 1).
    Reste dans la grille [0, taille-1].
    """
    # TODO
    # Générer les 8 directions avec dx, dy dans {-1, 0, 1}
    # Filtrer celles qui sortent de la grille
    pass


# Tests exercice 5
if __name__ == "__main__":
    voisins = cases_adjacentes(0, 0)   # coin supérieur gauche
    print(len(voisins))   # 3 : (1,0), (0,1), (1,1)
    voisins2 = cases_adjacentes(3, 3)  # case centrale
    print(len(voisins2))  # 8
    print(sorted(voisins2))  # toutes les 8 directions
