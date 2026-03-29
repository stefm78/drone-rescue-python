# =============================================================================
# EXERCICE 05 — Classes et objets
# Module correspondant : cours/05_classes_et_objets.md
# =============================================================================
# Objectifs :
#   - Comprendre la syntaxe class / __init__ / self
#   - Créer des attributs et des méthodes
#   - Utiliser l'héritage simple
#   - Implémenter __str__ pour l'affichage
# =============================================================================


# -----------------------------------------------------------------------------
# EXERCICE 1 — Créer une classe Position
# -----------------------------------------------------------------------------
# Dans Drone Rescue, chaque entité a une position sur la grille.
# Une position est définie par une colonne (lettre A-L) et une ligne (1-12).
#
# Crée une classe Position avec :
#   - __init__(self, colonne, ligne) → stocke les attributs
#   - __str__(self) → retourne "A1", "B7", "K12" etc.
#   - distance_chebyshev(self, autre_position) → retourne la distance
#     de Chebyshev entre deux positions (max des différences absolues)
#     Rappel : dist = max(|col1-col2|, |lig1-lig2|)
#     Les colonnes A=0, B=1, ..., L=11
# -----------------------------------------------------------------------------

class Position:
    def __init__(self, colonne, ligne):
        # TODO : stocker colonne et ligne comme attributs
        pass

    def __str__(self):
        # TODO : retourner la représentation "colonne+ligne" ex: "A1"
        pass

    def distance_chebyshev(self, autre):
        # TODO : calculer la distance de Chebyshev
        # Convertir la colonne lettre en index : ord(self.colonne) - ord('A')
        pass


# Tests exercice 1
if __name__ == "__main__":
    p1 = Position("A", 1)
    p2 = Position("B", 2)
    print(str(p1))  # Attendu : A1
    print(str(p2))  # Attendu : B2
    print(p1.distance_chebyshev(p2))  # Attendu : 1
    p3 = Position("A", 1)
    p4 = Position("D", 5)
    print(p3.distance_chebyshev(p4))  # Attendu : 4


# -----------------------------------------------------------------------------
# EXERCICE 2 — Créer une classe Drone
# -----------------------------------------------------------------------------
# Un drone a : un identifiant (ex: "D1"), une position, une batterie courante,
# une batterie max, un survivant transporté (None ou str), et un compteur
# de blocage (0 = libre).
#
# Crée une classe Drone avec :
#   - __init__(self, identifiant, position, batterie_max=20, batterie_init=10)
#   - __str__(self) → "D1 | B7 | bat:8/20 | surv:S3"
#   - est_hs(self) → True si batterie == 0
#   - est_bloque(self) → True si blocage > 0
#   - consommer_batterie(self) → soustrait 1 à batterie (min 0)
# -----------------------------------------------------------------------------

class Drone:
    def __init__(self, identifiant, position, batterie_max=20, batterie_init=10):
        # TODO
        pass

    def __str__(self):
        # TODO : format → "D1 | B7 | bat:8/20 | surv:—"
        pass

    def est_hs(self):
        # TODO
        pass

    def est_bloque(self):
        # TODO
        pass

    def consommer_batterie(self):
        # TODO
        pass


# Tests exercice 2
if __name__ == "__main__":
    pos = Position("B", 7)
    d = Drone("D1", pos)
    print(d)             # D1 | B7 | bat:10/20 | surv:—
    print(d.est_hs())    # False
    d.batterie = 0
    print(d.est_hs())    # True
    d2 = Drone("D2", Position("A", 1), batterie_max=20, batterie_init=5)
    d2.consommer_batterie()
    print(d2.batterie)   # 4


# -----------------------------------------------------------------------------
# EXERCICE 3 — Héritage : classe Entite et sous-classes
# -----------------------------------------------------------------------------
# Dans Drone Rescue, Drone et Tempete partagent des comportements communs :
# ils ont tous les deux un identifiant, une position, et peuvent se déplacer.
#
# Crée une classe de base Entite avec :
#   - __init__(self, identifiant, position)
#   - deplacer(self, nouvelle_position) → met à jour self.position
#   - __str__(self) → "[D1] A1" ou "[T2] K3"
#
# Crée une classe Tempete qui hérite de Entite :
#   - __init__(self, identifiant, position, depl_max=2)
#   - propriété depl_restants (initialisée à depl_max)
#   - reset_tour(self) → remet depl_restants à depl_max
# -----------------------------------------------------------------------------

class Entite:
    def __init__(self, identifiant, position):
        # TODO
        pass

    def deplacer(self, nouvelle_position):
        # TODO
        pass

    def __str__(self):
        # TODO
        pass


class Tempete(Entite):
    def __init__(self, identifiant, position, depl_max=2):
        # TODO : appeler super().__init__ puis initialiser depl_restants
        pass

    def reset_tour(self):
        # TODO
        pass


# Tests exercice 3
if __name__ == "__main__":
    t = Tempete("T1", Position("J", 2))
    print(t)                  # [T1] J2
    print(t.depl_restants)    # 2
    t.deplacer(Position("K", 3))
    print(t)                  # [T1] K3
    t.depl_restants -= 1
    print(t.depl_restants)    # 1
    t.reset_tour()
    print(t.depl_restants)    # 2
