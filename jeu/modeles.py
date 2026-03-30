# =============================================================================
# modeles.py — Définition des classes du jeu Drone Rescue
#
# Classes :
#   - Position      : coordonnées (col, lig) avec helpers
#   - Batiment      : case occupée par un bâtiment
#   - Hopital       : hôpital unique, permet recharge
#   - Survivant     : survivant à secourir
#   - Drone         : drone piloté par le joueur
#   - Tempete       : tempête qui se déplace automatiquement
#   - Grille        : plateau de jeu 12x12
#   - EtatJeu       : état complet d'une partie
# =============================================================================

from config import (
    GRILLE_TAILLE, NB_DRONES, NB_TEMPETES, NB_BATIMENTS, NB_SURVIVANTS,
    BATTERIE_MAX, BATTERIE_INIT, NB_ZONES_DANGER
)
import random

# ---------------------------------------------------------------------------
# Position
# ---------------------------------------------------------------------------

class Position:
    """
    Coordonnées sur la grille.
    col : entier 0..11  (0 = colonne A, 11 = colonne L)
    lig : entier 0..11  (0 = ligne 1,   11 = ligne 12)
    """

    LETTRES = list("ABCDEFGHIJKL")  # Correspondance index -> lettre

    def __init__(self, col: int, lig: int):
        self.col = col
        self.lig = lig

    def __str__(self) -> str:
        return f"{self.LETTRES[self.col]}{self.lig + 1}"

    def __repr__(self) -> str:
        return f"Position({self.col}, {self.lig})"

    def __eq__(self, autre) -> bool:
        if not isinstance(autre, Position):
            return False
        return self.col == autre.col and self.lig == autre.lig

    def __hash__(self):
        return hash((self.col, self.lig))

    def distance_chebyshev(self, autre: "Position") -> int:
        return max(abs(self.col - autre.col), abs(self.lig - autre.lig))

    def est_valide(self) -> bool:
        return 0 <= self.col < GRILLE_TAILLE and 0 <= self.lig < GRILLE_TAILLE

    @classmethod
    def depuis_chaine(cls, texte: str) -> "Position | None":
        texte = texte.strip().upper()
        if len(texte) < 2:
            return None
        lettre = texte[0]
        if lettre not in cls.LETTRES:
            return None
        try:
            lig = int(texte[1:]) - 1
        except ValueError:
            return None
        col = cls.LETTRES.index(lettre)
        pos = cls(col, lig)
        return pos if pos.est_valide() else None

    def voisins_ortho(self) -> list:
        """Cases orthogonales valides (pour propagation X)."""
        candidats = [
            Position(self.col,     self.lig - 1),
            Position(self.col,     self.lig + 1),
            Position(self.col - 1, self.lig),
            Position(self.col + 1, self.lig),
        ]
        return [p for p in candidats if p.est_valide()]

    def voisins_diag(self) -> list:
        """Les 8 cases adjacentes valides (distance Chebyshev = 1)."""
        candidats = []
        for dc in [-1, 0, 1]:
            for dl in [-1, 0, 1]:
                if dc == 0 and dl == 0:
                    continue
                candidats.append(Position(self.col + dc, self.lig + dl))
        return [p for p in candidats if p.est_valide()]


# ---------------------------------------------------------------------------
# Bâtiment
# ---------------------------------------------------------------------------

class Batiment:
    def __init__(self, position: Position):
        self.position = position

    def __repr__(self):
        return f"Batiment({self.position})"


# ---------------------------------------------------------------------------
# Hôpital
# ---------------------------------------------------------------------------

class Hopital:
    """
    L'hôpital est positionné aléatoirement à la création (via EtatJeu).
    Sa position est passée en paramètre ; si None, elle sera assignée plus tard.
    """
    def __init__(self, position: Position = None):
        # Position définie à l'initialisation de la partie (aléatoire)
        self.position = position  # sera fixée par initialiser_partie()

    def __repr__(self):
        return f"Hopital({self.position})"


# ---------------------------------------------------------------------------
# Survivant
# ---------------------------------------------------------------------------

class Survivant:
    def __init__(self, identifiant: str, position: Position):
        self.identifiant = identifiant
        self.position = position
        self.etat = "en_attente"         # 'en_attente' | 'porte' | 'sauve'
        self.drone_porteur = None

    def est_sauve(self) -> bool:
        return self.etat == "sauve"

    def est_porte(self) -> bool:
        return self.etat == "porte"

    def __repr__(self):
        return f"Survivant({self.identifiant}, {self.position}, {self.etat})"


# ---------------------------------------------------------------------------
# Drone
# ---------------------------------------------------------------------------

class Drone:
    def __init__(self, identifiant: str, position: Position):
        self.identifiant = identifiant
        self.position = position
        self.batterie = BATTERIE_INIT
        self.batterie_max = BATTERIE_MAX
        self.survivant = None
        self.bloque = 0
        self.hors_service = False

    def est_actif(self) -> bool:
        return not self.hors_service and self.bloque == 0

    def est_bloque(self) -> bool:
        return self.bloque > 0

    def consommer_batterie(self, nb: int = 1):
        self.batterie -= nb
        if self.batterie <= 0:
            self.batterie = 0
            self.hors_service = True
            if self.survivant:
                self.survivant.etat = "en_attente"
                self.survivant.drone_porteur = None
                self.survivant.position = Position(self.position.col, self.position.lig)
                self.survivant = None

    def recharger(self):
        self.batterie = self.batterie_max
        self.hors_service = False

    def prendre_survivant(self, survivant: Survivant):
        survivant.etat = "porte"
        survivant.drone_porteur = self
        self.survivant = survivant

    def deposer_survivant_hopital(self) -> Survivant | None:
        if self.survivant:
            s = self.survivant
            s.etat = "sauve"
            s.drone_porteur = None
            self.survivant = None
            return s
        return None

    def __repr__(self):
        return (f"Drone({self.identifiant}, pos={self.position}, "
                f"bat={self.batterie}/{self.batterie_max}, "
                f"surv={self.survivant.identifiant if self.survivant else '—'}, "
                f"bloque={self.bloque}, hs={self.hors_service})")


# ---------------------------------------------------------------------------
# Tempête
# ---------------------------------------------------------------------------

class Tempete:
    """
    Une tempête bloque les drones sur sa case.
    Elle se déplace automatiquement en fin de tour selon sa direction courante.

    Attributs :
        identifiant : "T1".."T4"
        position    : Position courante
        direction   : (dx, dy) tuple d'entiers in {-1, 0, 1}
                      initialisé aléatoirement à la création
                      mis à jour après chaque rebond ou mouvement manuel

    Les tempêtes NE propagent PAS de zones X.
    Ce sont les zones X existantes qui s'étendent (cf. propager_zones_x).
    """

    _DIRECTIONS = [
        (dc, dl)
        for dc in (-1, 0, 1)
        for dl in (-1, 0, 1)
        if not (dc == 0 and dl == 0)
    ]

    def __init__(self, identifiant: str, position: Position):
        self.identifiant = identifiant
        self.position = position
        # Direction initiale aléatoire parmi les 8 directions possibles
        self.direction: tuple = random.choice(self._DIRECTIONS)

    def __repr__(self):
        return f"Tempete({self.identifiant}, {self.position}, dir={self.direction})"


# ---------------------------------------------------------------------------
# Grille
# ---------------------------------------------------------------------------

class Grille:
    """
    Plateau de jeu 12x12.
    Symboles : '.' vide, 'B' bâtiment, 'H' hôpital, 'S' survivant,
               'D' drone, 'T' tempête, 'X' zone dangereuse.
    """

    def __init__(self):
        self.taille = GRILLE_TAILLE
        self.cases = [['.' for _ in range(self.taille)] for _ in range(self.taille)]

    def obtenir(self, position: Position) -> str:
        return self.cases[position.lig][position.col]

    def definir(self, position: Position, symbole: str):
        self.cases[position.lig][position.col] = symbole

    def est_libre(self, position: Position) -> bool:
        return self.cases[position.lig][position.col] == '.'


# ---------------------------------------------------------------------------
# EtatJeu
# ---------------------------------------------------------------------------

class EtatJeu:
    def __init__(self):
        self.grille = Grille()
        self.hopital = Hopital()          # position=None, fixée par initialiser_partie()
        self.batiments: list = []
        self.survivants: list = []
        self.drones: list = []
        self.tempetes: list = []
        self.zones_x: set = set()
        self.tour = 1
        self.score = 0
        self.historique: list = []
        self.partie_finie = False
        self.victoire = False

    def drone_par_id(self, identifiant: str) -> Drone | None:
        for d in self.drones:
            if d.identifiant == identifiant:
                return d
        return None

    def tempete_par_id(self, identifiant: str) -> Tempete | None:
        for t in self.tempetes:
            if t.identifiant == identifiant:
                return t
        return None

    def survivant_sur_case(self, position: Position) -> Survivant | None:
        for s in self.survivants:
            if s.etat == "en_attente" and s.position == position:
                return s
        return None

    def drones_sur_case(self, position: Position) -> list:
        return [d for d in self.drones if d.position == position and not d.hors_service]

    def tempete_sur_case(self, position: Position) -> Tempete | None:
        for t in self.tempetes:
            if t.position == position:
                return t
        return None

    def batiment_sur_case(self, position: Position) -> bool:
        return any(b.position == position for b in self.batiments)

    def survivants_restants(self) -> int:
        return sum(1 for s in self.survivants if not s.est_sauve())

    def drones_actifs(self) -> list:
        return [d for d in self.drones if not d.hors_service]

    def __repr__(self):
        return (f"EtatJeu(tour={self.tour}, score={self.score}, "
                f"survivants_restants={self.survivants_restants()})")
