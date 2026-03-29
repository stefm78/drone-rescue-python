# =============================================================================
# EXERCICE 06 — Grille et affichage
# Module correspondant : cours/06_grille_et_affichage.md
# =============================================================================
# Objectifs :
#   - Créer et manipuler une grille 2D avec des listes imbriquées
#   - Positionner des entités sur la grille
#   - Afficher la grille en console avec coordonnées
#   - Utiliser les codes ANSI pour colorer l'affichage
# =============================================================================


# -----------------------------------------------------------------------------
# EXERCICE 1 — Créer une grille vide
# -----------------------------------------------------------------------------
# La grille de Drone Rescue fait 12×12 cases.
# Chaque case est initialisée avec le symbole '.' (vide).
#
# Écris une fonction creer_grille(taille=12) qui retourne
# une liste de listes : grille[ligne][colonne]
# Attention : ligne 0 = ligne 1 du jeu (index décalé de 1)
# -----------------------------------------------------------------------------

def creer_grille(taille=12):
    """
    Retourne une grille taille×taille remplie de '.'.
    grille[i][j] = case à la ligne i+1, colonne chr(65+j).
    """
    # TODO : utiliser une compréhension de liste imbriquée
    pass


# Tests exercice 1
if __name__ == "__main__":
    g = creer_grille()
    print(len(g))        # 12
    print(len(g[0]))     # 12
    print(g[0][0])       # .
    print(g[11][11])     # .


# -----------------------------------------------------------------------------
# EXERCICE 2 — Placer et lire une entité sur la grille
# -----------------------------------------------------------------------------
# Écris deux fonctions :
#   placer(grille, colonne_lettre, ligne_num, symbole)
#     → place le symbole sur la grille (ligne_num commence à 1)
#   lire(grille, colonne_lettre, ligne_num)
#     → retourne le contenu de la case
#
# Colonnes : A=0, B=1, ..., L=11  (ord(col) - ord('A'))
# Lignes   : 1=index 0, 2=index 1, ..., 12=index 11
# -----------------------------------------------------------------------------

def placer(grille, colonne, ligne, symbole):
    # TODO
    pass


def lire(grille, colonne, ligne):
    # TODO
    pass


# Tests exercice 2
if __name__ == "__main__":
    g = creer_grille()
    placer(g, "A", 12, "H")   # Hôpital en A12
    placer(g, "D", 3, "D1")   # Drone D1 en D3
    placer(g, "G", 7, "S")    # Survivant en G7
    print(lire(g, "A", 12))   # H
    print(lire(g, "D", 3))    # D1
    print(lire(g, "B", 1))    # .


# -----------------------------------------------------------------------------
# EXERCICE 3 — Afficher la grille
# -----------------------------------------------------------------------------
# Écris une fonction afficher_grille(grille) qui affiche :
#
#      A   B   C   D  ...  L
#   1  .   .   .   D1 ...  .
#   2  .   .   .   .  ...  .
#  ...
#  12  H   .   .   .  ...  .
#
# Chaque case occupe exactement 4 caractères (ljust(4) ou format).
# Les numéros de ligne sont alignés à droite sur 3 caractères.
# BONUS : colorier en rouge les cases 'X', en jaune les drones,
#         en vert les survivants, en bleu l'hôpital.
# -----------------------------------------------------------------------------

COULEURS = {
    "H": "\033[94m",   # Bleu
    "S": "\033[92m",   # Vert
    "X": "\033[91m",   # Rouge
    "T": "\033[93m",   # Jaune/Orange pour tempête
    "RESET": "\033[0m",
}

def afficher_grille(grille):
    """
    Affiche la grille avec coordonnées en en-tête et numéros de ligne.
    """
    # TODO : afficher l'en-tête des colonnes
    # TODO : pour chaque ligne, afficher le numéro puis les cases
    # BONUS : appliquer les couleurs selon le contenu
    pass


# Tests exercice 3
if __name__ == "__main__":
    g = creer_grille()
    placer(g, "A", 12, "H")
    placer(g, "D", 3, "D1")
    placer(g, "G", 7, "S")
    placer(g, "C", 5, "X")
    afficher_grille(g)


# -----------------------------------------------------------------------------
# EXERCICE 4 — Trouver les cases adjacentes
# -----------------------------------------------------------------------------
# Dans Drone Rescue, les déplacements sont en distance de Chebyshev ≤ 1,
# ce qui signifie les 8 cases voisines (y compris diagonales).
#
# Écris une fonction cases_adjacentes(colonne, ligne, taille=12) qui
# retourne la liste de tuples (col_lettre, ligne_num) de toutes les
# cases à distance Chebyshev = 1, en restant dans les limites de la grille.
# -----------------------------------------------------------------------------

def cases_adjacentes(colonne, ligne, taille=12):
    """
    Retourne la liste des cases voisines (distance Chebyshev = 1).
    """
    # TODO
    # Convertir colonne lettre → index, générer les 8 directions,
    # filtrer celles qui sortent de la grille, reconvertir en lettre
    pass


# Tests exercice 4
if __name__ == "__main__":
    voisins = cases_adjacentes("A", 1)   # coin supérieur gauche
    print(len(voisins))   # 3 (B1, A2, B2)
    voisins2 = cases_adjacentes("F", 6)  # case centrale
    print(len(voisins2))  # 8
    print(sorted(voisins2))  # toutes les 8 directions
