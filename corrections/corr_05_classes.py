# =============================================================================
# CORRECTION 05 — Classes et objets
# Module correspondant : cours/05_classes_et_objets.md
# =============================================================================


# -----------------------------------------------------------------------------
# CORRECTION 1 — Classe Position
# -----------------------------------------------------------------------------
# On stocke colonne (lettre) et ligne (entier).
# La distance de Chebyshev = max(|Δcol|, |Δlig|), colonnes converties en index.
# -----------------------------------------------------------------------------

class Position:
    def __init__(self, colonne, ligne):
        self.colonne = colonne  # lettre : "A"…"L"
        self.ligne = ligne      # entier : 1…12

    def __str__(self):
        return f"{self.colonne}{self.ligne}"

    def distance_chebyshev(self, autre):
        # Convertir les lettres en indices numériques
        dc = abs(ord(self.colonne) - ord(autre.colonne))
        dl = abs(self.ligne - autre.ligne)
        return max(dc, dl)


# Tests
if __name__ == "__main__":
    p1 = Position("A", 1)
    p2 = Position("B", 2)
    print(str(p1))                    # A1
    print(str(p2))                    # B2
    print(p1.distance_chebyshev(p2))  # 1
    p3 = Position("A", 1)
    p4 = Position("D", 5)
    print(p3.distance_chebyshev(p4))  # 4


# -----------------------------------------------------------------------------
# CORRECTION 2 — Classe Drone
# -----------------------------------------------------------------------------
# Les attributs clés : identifiant, position, batterie, batterie_max,
# survivant (None par défaut), blocage (0 = libre).
# est_hs() teste batterie == 0 ; consommer_batterie() soustrait 1 (plancher 0).
# -----------------------------------------------------------------------------

class Drone:
    def __init__(self, identifiant, position, batterie_max=20, batterie_init=10):
        self.identifiant = identifiant
        self.position = position
        self.batterie_max = batterie_max
        self.batterie = batterie_init
        self.survivant = None   # None ou identifiant du survivant porté
        self.blocage = 0        # nombre de tours restants de blocage

    def __str__(self):
        surv = self.survivant if self.survivant else "—"
        return (
            f"{self.identifiant} | {self.position} | "
            f"bat:{self.batterie}/{self.batterie_max} | surv:{surv}"
        )

    def est_hs(self):
        """Retourne True si le drone est hors service (batterie épuisée)."""
        return self.batterie == 0

    def est_bloque(self):
        """Retourne True si le drone est immobilisé par une tempête."""
        return self.blocage > 0

    def consommer_batterie(self):
        """Soustrait 1 à la batterie (jamais en dessous de 0)."""
        self.batterie = max(0, self.batterie - 1)


# Tests
if __name__ == "__main__":
    pos = Position("B", 7)
    d = Drone("D1", pos)
    print(d)              # D1 | B7 | bat:10/20 | surv:—
    print(d.est_hs())     # False
    d.batterie = 0
    print(d.est_hs())     # True
    d2 = Drone("D2", Position("A", 1), batterie_max=20, batterie_init=5)
    d2.consommer_batterie()
    print(d2.batterie)    # 4


# -----------------------------------------------------------------------------
# CORRECTION 3 — Héritage : Entite et Tempete
# -----------------------------------------------------------------------------
# Entite centralise identifiant + position + déplacement.
# Tempete hérite d'Entite et ajoute depl_max / depl_restants / reset_tour().
# On appelle super().__init__() pour ne pas dupliquer le code parent.
# -----------------------------------------------------------------------------

class Entite:
    def __init__(self, identifiant, position):
        self.identifiant = identifiant
        self.position = position

    def deplacer(self, nouvelle_position):
        """Met à jour la position de l'entité."""
        self.position = nouvelle_position

    def __str__(self):
        return f"[{self.identifiant}] {self.position}"


class Tempete(Entite):
    def __init__(self, identifiant, position, depl_max=2):
        super().__init__(identifiant, position)  # réutilise __init__ d'Entite
        self.depl_max = depl_max
        self.depl_restants = depl_max

    def reset_tour(self):
        """Remet le compteur de déplacements au maximum en début de tour."""
        self.depl_restants = self.depl_max


# Tests
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
