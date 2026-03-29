# =============================================================================
# CORRECTION 06 — Grille et affichage
# Module correspondant : cours/06_grille_et_affichage.md
# =============================================================================


# -----------------------------------------------------------------------------
# CORRECTION 1 — Créer une grille vide
# -----------------------------------------------------------------------------
# On utilise une compréhension de liste imbriquée.
# grille[i] = ligne i+1, grille[i][j] = colonne chr(65+j).
# Chaque case est initialisée à '.' (vide).
# -----------------------------------------------------------------------------

def creer_grille(taille=12):
    """
    Retourne une grille taille×taille remplie de '.'.
    grille[i][j] → ligne i+1, colonne chr(65+j).
    """
    return [['.' for _ in range(taille)] for _ in range(taille)]


# Tests
if __name__ == "__main__":
    g = creer_grille()
    print(len(g))      # 12
    print(len(g[0]))   # 12
    print(g[0][0])     # .
    print(g[11][11])   # .


# -----------------------------------------------------------------------------
# CORRECTION 2 — Placer et lire une entité
# -----------------------------------------------------------------------------
# La conversion coordonnées ↔ indices :
#   colonne lettre → index j : ord(col) - ord('A')
#   ligne num      → index i : ligne - 1
# -----------------------------------------------------------------------------

def placer(grille, colonne, ligne, symbole):
    """Place le symbole à la position (colonne lettre, ligne num) de la grille."""
    i = ligne - 1               # index ligne (0-based)
    j = ord(colonne) - ord('A') # index colonne (0-based)
    grille[i][j] = symbole


def lire(grille, colonne, ligne):
    """Retourne le contenu de la case (colonne lettre, ligne num)."""
    i = ligne - 1
    j = ord(colonne) - ord('A')
    return grille[i][j]


# Tests
if __name__ == "__main__":
    g = creer_grille()
    placer(g, "A", 12, "H")
    placer(g, "D", 3, "D1")
    placer(g, "G", 7, "S")
    print(lire(g, "A", 12))   # H
    print(lire(g, "D", 3))    # D1
    print(lire(g, "B", 1))    # .


# -----------------------------------------------------------------------------
# CORRECTION 3 — Afficher la grille
# -----------------------------------------------------------------------------
# En-tête : lettres de colonnes, alignées à 4 caractères chacune.
# Corps    : numéro de ligne (3 chars, aligné droite) + cases colorisées.
# BONUS    : codes ANSI pour colorier H, S, X, T.
# -----------------------------------------------------------------------------

COULEURS = {
    "H": "\033[94m",    # Bleu
    "S": "\033[92m",    # Vert
    "X": "\033[91m",    # Rouge
    "T": "\033[93m",    # Jaune pour tempête
    "RESET": "\033[0m",
}

def afficher_grille(grille):
    """Affiche la grille avec en-tête des colonnes et numéros de lignes."""
    taille = len(grille)
    cols = [chr(65 + j) for j in range(taille)]

    # En-tête des colonnes
    entete = "    " + "".join(c.ljust(4) for c in cols)
    print(entete)

    # Corps de la grille
    for i in range(taille):
        num_ligne = str(i + 1).rjust(3)
        ligne_str = num_ligne + " "
        for j in range(taille):
            case = grille[i][j]
            # Déterminer la clé de couleur (premier caractère pour drones ex "D1")
            cle = case[0] if case != '.' else '.'
            couleur = COULEURS.get(cle, "")
            reset = COULEURS["RESET"] if couleur else ""
            ligne_str += f"{couleur}{case.ljust(4)}{reset}"
        print(ligne_str)


# Tests
if __name__ == "__main__":
    g = creer_grille()
    placer(g, "A", 12, "H")
    placer(g, "D", 3, "D1")
    placer(g, "G", 7, "S")
    placer(g, "C", 5, "X")
    afficher_grille(g)


# -----------------------------------------------------------------------------
# CORRECTION 4 — Cases adjacentes (distance Chebyshev = 1)
# -----------------------------------------------------------------------------
# On génère les 8 directions (-1,0,+1)×(-1,0,+1) sauf (0,0).
# On filtre les cases hors grille puis on reconvertit l'index en lettre.
# -----------------------------------------------------------------------------

def cases_adjacentes(colonne, ligne, taille=12):
    """
    Retourne la liste des cases voisines à distance Chebyshev = 1.
    Chaque case est un tuple (col_lettre, ligne_num).
    """
    j0 = ord(colonne) - ord('A')
    i0 = ligne - 1
    voisins = []
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue  # case centrale exclue
            ni, nj = i0 + di, j0 + dj
            if 0 <= ni < taille and 0 <= nj < taille:
                voisins.append((chr(65 + nj), ni + 1))
    return voisins


# Tests
if __name__ == "__main__":
    voisins = cases_adjacentes("A", 1)   # coin supérieur gauche
    print(len(voisins))    # 3  → (B,1), (A,2), (B,2)
    voisins2 = cases_adjacentes("F", 6)  # case centrale
    print(len(voisins2))   # 8
    print(sorted(voisins2))
