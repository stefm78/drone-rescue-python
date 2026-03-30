# =============================================================================
# CORRECTION 05 — Classes et objets
# Module correspondant : cours/05_classes_et_objets.md
# =============================================================================
# Convention : colonne str 'A'..'L', ligne int 1-based 1..12
# Architecture : EntiteGrille (base) → Drone / Tempete / Survivant
# =============================================================================


# -----------------------------------------------------------------------------
# CORRECTION 1+3 — Classe de base EntiteGrille et sous-classes
# -----------------------------------------------------------------------------
# EntiteGrille centralise les attributs communs à tous les objets du jeu :
# identifiant, colonne, ligne, position_str, __str__.
# Les sous-classes appellent super().__init__() pour ne pas dupliquer ce code.
# @property est utilisé pour les attributs calculés (pas stockés).
# -----------------------------------------------------------------------------

class EntiteGrille:
    """Classe de base pour tout objet positionné sur la grille."""

    def __init__(self, identifiant: str, colonne: str, ligne: int):
        self.identifiant = identifiant
        self.colonne = colonne   # str : 'A'..'L'
        self.ligne   = ligne     # int : 1..12

    @property
    def position_str(self) -> str:
        """Représentation lisible ex: 'B7' — recalculée à chaque accès."""
        return f"{self.colonne}{self.ligne}"

    def deplacer(self, nouvelle_colonne: str, nouvelle_ligne: int):
        """Met à jour la position de l'entité."""
        self.colonne = nouvelle_colonne
        self.ligne   = nouvelle_ligne

    def __str__(self) -> str:
        return f"[{self.identifiant}] {self.position_str}"


# Tests EntiteGrille
if __name__ == "__main__":
    e = EntiteGrille("X1", "D", 5)
    print(e)               # [X1] D5
    print(e.position_str)  # D5
    e.deplacer("E", 6)
    print(e)               # [X1] E6


# -----------------------------------------------------------------------------
# CORRECTION 2 — Classe Drone (hérite de EntiteGrille)
# -----------------------------------------------------------------------------
# On ajoute batterie, batterie_max, survivant, bloque.
# est_hs et est_bloque sont des @property : pas de parenthèses à l'appel.
# consommer_batterie() applique un plancher à 0.
# -----------------------------------------------------------------------------

class Drone(EntiteGrille):
    """Drone de sauvetage."""

    def __init__(self, identifiant: str, colonne: str, ligne: int,
                 batterie_init: int = 10, batterie_max: int = 20):
        super().__init__(identifiant, colonne, ligne)  # initialise id, col, lig
        self.batterie     = batterie_init
        self.batterie_max = batterie_max
        self.survivant    = None   # None ou identifiant du survivant porté
        self.bloque       = 0      # nombre de tours de blocage restants

    @property
    def est_hs(self) -> bool:
        """True si batterie épuisée. Appel : d.est_hs (sans parenthèses)."""
        return self.batterie <= 0

    @property
    def est_bloque(self) -> bool:
        """True si le drone est immobilisé par une tempête."""
        return self.bloque > 0

    def consommer_batterie(self):
        """Soustrait 1 à la batterie (plancher 0)."""
        self.batterie = max(0, self.batterie - 1)

    def __str__(self) -> str:
        surv = self.survivant if self.survivant else '—'
        etat = 'HS' if self.est_hs else (f'blq:{self.bloque}t' if self.est_bloque else 'actif')
        return (
            f"{self.identifiant} | {self.position_str} | "
            f"bat:{self.batterie}/{self.batterie_max} | surv:{surv} | {etat}"
        )


# Tests Drone
if __name__ == "__main__":
    d = Drone("D1", "B", 7)
    print(d)              # D1 | B7 | bat:10/20 | surv:— | actif
    print(d.est_hs)       # False  (pas de parenthèses !)
    d.batterie = 0
    print(d.est_hs)       # True
    d2 = Drone("D2", "A", 1, batterie_init=5)
    d2.consommer_batterie()
    print(d2.batterie)    # 4


# -----------------------------------------------------------------------------
# CORRECTION 3 — Classe Tempete (hérite de EntiteGrille)
# -----------------------------------------------------------------------------
# Tempete ajoute depl_max et depl_restants.
# reset_tour() remet depl_restants à depl_max en début de tour.
# -----------------------------------------------------------------------------

class Tempete(EntiteGrille):
    """Tempête mobile sur la grille."""

    def __init__(self, identifiant: str, colonne: str, ligne: int, depl_max: int = 2):
        super().__init__(identifiant, colonne, ligne)
        self.depl_max      = depl_max
        self.depl_restants = depl_max

    def reset_tour(self):
        """Remet le compteur de déplacements au maximum."""
        self.depl_restants = self.depl_max


# Tests Tempete
if __name__ == "__main__":
    t = Tempete("T1", "J", 2)
    print(t)                  # [T1] J2
    print(t.depl_restants)    # 2
    t.deplacer("K", 3)
    print(t)                  # [T1] K3
    t.depl_restants -= 1
    print(t.depl_restants)    # 1
    t.reset_tour()
    print(t.depl_restants)    # 2


# -----------------------------------------------------------------------------
# Bonus — Classe Survivant (hérite de EntiteGrille)
# -----------------------------------------------------------------------------

class Survivant(EntiteGrille):
    """Survivant à secourir."""

    def __init__(self, identifiant: str, colonne: str, ligne: int):
        super().__init__(identifiant, colonne, ligne)
        self.sauve     = False
        self.porte_par = None  # Drone qui le porte

    def __str__(self) -> str:
        etat = 'sauvé' if self.sauve else ('porté' if self.porte_par else 'en attente')
        return f"[{self.identifiant}] {self.position_str} ({etat})"


# Test Survivant
if __name__ == "__main__":
    s = Survivant("S3", "G", 7)
    print(s)   # [S3] G7 (en attente)
