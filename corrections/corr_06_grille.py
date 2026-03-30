# =============================================================================
# CORRECTION 06 — Grille et affichage
# =============================================================================


# -----------------------------------------------------------------------------
# EXERCICE 1 — Créer une grille vide
# -----------------------------------------------------------------------------

def creer_grille(taille=8):
    """Retourne une grille taille×taille remplie de '.'."""
    # List comprehension imbriquée : grille[lig][col]
    return [['.' for _ in range(taille)] for _ in range(taille)]


if __name__ == "__main__":
    g = creer_grille()
    assert len(g) == 8
    assert len(g[0]) == 8
    assert g[0][0] == '.'
    assert g[7][7] == '.'
    print("Ex1 OK")


# -----------------------------------------------------------------------------
# EXERCICE 2 — Placer et lire une entité
# -----------------------------------------------------------------------------

def placer(grille, col, lig, symbole):
    """Place le symbole sur grille[lig][col]."""
    grille[lig][col] = symbole   # attention : lig d'abord, puis col


def lire(grille, col, lig):
    """Retourne le contenu de grille[lig][col]."""
    return grille[lig][col]


if __name__ == "__main__":
    g = creer_grille()
    placer(g, 0, 7, "H")
    placer(g, 3, 2, "D")
    placer(g, 6, 4, "S")
    assert lire(g, 0, 7) == "H"
    assert lire(g, 3, 2) == "D"
    assert lire(g, 1, 0) == "."
    print("Ex2 OK")


# -----------------------------------------------------------------------------
# EXERCICE 3 — Afficher la grille
# -----------------------------------------------------------------------------

def afficher_grille(grille):
    """Affiche la grille avec numéros de colonne et de ligne. Sans ANSI."""
    taille = len(grille)
    # En-tête colonnes
    entete = "    " + "".join(str(c).ljust(4) for c in range(taille))
    print(entete)
    # Lignes
    for lig in range(taille):
        num_lig = str(lig).rjust(3)
        cases   = "".join(str(grille[lig][col]).ljust(4) for col in range(taille))
        print(f"{num_lig} {cases}")


if __name__ == "__main__":
    g = creer_grille()
    placer(g, 0, 7, "H")
    placer(g, 3, 2, "D")
    placer(g, 6, 4, "S")
    placer(g, 2, 3, "X")
    afficher_grille(g)
    print("Ex3 OK")


# -----------------------------------------------------------------------------
# EXERCICE 4 — Distance de Chebyshev
# -----------------------------------------------------------------------------

def distance_chebyshev(col1, lig1, col2, lig2):
    """Retourne max(|col1-col2|, |lig1-lig2|)."""
    return max(abs(col2 - col1), abs(lig2 - lig1))
    # max() entre les deux différences absolues.
    # Avec les diagonales autorisées, chaque direction = 1 déplacement.


if __name__ == "__main__":
    assert distance_chebyshev(0, 0, 0, 0) == 0
    assert distance_chebyshev(0, 0, 1, 1) == 1
    assert distance_chebyshev(0, 0, 1, 0) == 1
    assert distance_chebyshev(0, 0, 0, 3) == 3
    assert distance_chebyshev(2, 3, 5, 7) == 4
    assert distance_chebyshev(0, 0, 7, 7) == 7
    print("Ex4 OK")


# -----------------------------------------------------------------------------
# EXERCICE 5 — Cases adjacentes (distance Chebyshev = 1)
# -----------------------------------------------------------------------------

def cases_adjacentes(col, lig, taille=8):
    """Retourne la liste des cases voisines dans les limites [0, taille-1]."""
    voisins = []
    for dc in (-1, 0, 1):
        for dl in (-1, 0, 1):
            if dc == 0 and dl == 0:
                continue   # la case elle-même n'est pas un voisin
            nc, nl = col + dc, lig + dl
            if 0 <= nc < taille and 0 <= nl < taille:
                voisins.append((nc, nl))
    return voisins
    # Note : on pourrait écrire en une seule list comprehension mais
    # la double boucle est plus lisible pour un débutant.


if __name__ == "__main__":
    assert len(cases_adjacentes(0, 0)) == 3   # coin : 3 voisins
    assert len(cases_adjacentes(3, 3)) == 8   # centre : 8 voisins
    print("Ex5 OK")
