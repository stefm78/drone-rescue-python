# =============================================================================
# modeles.py — Définition des classes du jeu Drone Rescue
#
# Classes :
#   - Position      : coordonnées (col, lig) avec helpers
#   - Batiment      : case occupée par un bâtiment
#   - Hopital       : hôpital unique, permet recharge
#   - Survivant     : survivant à secourir
#   - Drone         : drone piloté par le joueur
#   - Tempete       : tempête qui se déplace et propage des zones X
#   - Grille        : plateau de jeu 12x12
#   - EtatJeu       : état complet d'une partie
# =============================================================================

from config import (
    GRILLE_TAILLE, NB_DRONES, NB_TEMPETES, NB_BATIMENTS, NB_SURVIVANTS,
    BATTERIE_MAX, BATTERIE_INIT, NB_ZONES_DANGER,
    HOPITAL_COL, HOPITAL_LIG
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

    # ---- Représentation lisible : "A1", "L12", etc. ----------------------
    def __str__(self) -> str:
        return f"{self.LETTRES[self.col]}{self.lig + 1}"

    def __repr__(self) -> str:
        return f"Position({self.col}, {self.lig})"

    # ---- Égalité -----------------------------------------------------------
    def __eq__(self, autre) -> bool:
        if not isinstance(autre, Position):
            return False
        return self.col == autre.col and self.lig == autre.lig

    def __hash__(self):
        return hash((self.col, self.lig))

    # ---- Distance de Chebyshev (mouvement diagonal autorisé) ---------------
    def distance_chebyshev(self, autre: "Position") -> int:
        """
        Retourne la distance de Chebyshev entre self et autre.
        Deux positions adjacentes (y compris en diagonal) ont une distance de 1.
        """
        return max(abs(self.col - autre.col), abs(self.lig - autre.lig))

    # ---- Validation --------------------------------------------------------
    def est_valide(self) -> bool:
        """Retourne True si la position est dans les limites de la grille."""
        return 0 <= self.col < GRILLE_TAILLE and 0 <= self.lig < GRILLE_TAILLE

    # ---- Parsing depuis une chaîne (ex : "E6") ----------------------------
    @classmethod
    def depuis_chaine(cls, texte: str) -> "Position | None":
        """
        Convertit "E6" en Position(4, 5).
        Retourne None si le format est invalide.
        """
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

    # ---- Voisins orthogonaux (sans diagonal, pour propagation X) ----------
    def voisins_ortho(self) -> list:
        """Retourne la liste des positions orthogonales valides (haut/bas/gauche/droite)."""
        candidats = [
            Position(self.col,     self.lig - 1),
            Position(self.col,     self.lig + 1),
            Position(self.col - 1, self.lig),
            Position(self.col + 1, self.lig),
        ]
        return [p for p in candidats if p.est_valide()]

    # ---- Voisins diagonaux inclus (pour déplacement des drones/tempêtes) --
    def voisins_diag(self) -> list:
        """Retourne les 8 cases adjacentes valides (distance Chebyshev = 1)."""
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
    """Case bloquée — ni drone, ni tempête, ni survivant ne peut y entrer."""

    def __init__(self, position: Position):
        self.position = position

    def __repr__(self):
        return f"Batiment({self.position})"


# ---------------------------------------------------------------------------
# Hôpital
# ---------------------------------------------------------------------------

class Hopital:
    """
    L'hôpital est unique et fixé en A12.
    Les drones qui s'y posent se rechargent entièrement (batterie → BATTERIE_MAX).
    Plusieurs drones peuvent s'y trouver simultanément.
    """

    def __init__(self):
        self.position = Position(HOPITAL_COL, HOPITAL_LIG)

    def __repr__(self):
        return f"Hopital({self.position})"


# ---------------------------------------------------------------------------
# Survivant
# ---------------------------------------------------------------------------

class Survivant:
    """
    Un survivant attend d'être récupéré puis livré à l'hôpital.
    États : 'en_attente', 'porte' (par un drone), 'sauve'
    """

    def __init__(self, identifiant: str, position: Position):
        self.identifiant = identifiant   # ex : "S1", "S7"
        self.position = position
        self.etat = "en_attente"         # 'en_attente' | 'porte' | 'sauve'
        self.drone_porteur = None        # référence au Drone qui le porte

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
    """
    Un drone se déplace sur la grille, récupère des survivants et les livre
    à l'hôpital. Il peut se recharger à l'hôpital.

    Attributs importants :
        identifiant  : "D1".."D6"
        position     : Position courante
        batterie     : entier 0..BATTERIE_MAX
        survivant    : Survivant | None  — le survivant actuellement porté
        bloque       : int  — nombre de tours restants de blocage par tempête
        hors_service : bool  — True si batterie == 0
    """

    def __init__(self, identifiant: str, position: Position):
        self.identifiant = identifiant
        self.position = position
        self.batterie = BATTERIE_INIT
        self.batterie_max = BATTERIE_MAX
        self.survivant = None        # Survivant porté
        self.bloque = 0              # Tours de blocage restants
        self.hors_service = False

    # ---- Propriétés calculées ---------------------------------------------
    def est_actif(self) -> bool:
        """Un drone actif peut agir (non HS, non bloqué)."""
        return not self.hors_service and self.bloque == 0

    def est_bloque(self) -> bool:
        return self.bloque > 0

    # ---- Actions ----------------------------------------------------------
    def consommer_batterie(self, nb: int = 1):
        """Réduit la batterie de nb. Si elle atteint 0, le drone devient HS."""
        self.batterie -= nb
        if self.batterie <= 0:
            self.batterie = 0
            self.hors_service = True
            # Le survivant porté est déposé sur place
            if self.survivant:
                self.survivant.etat = "en_attente"
                self.survivant.drone_porteur = None
                self.survivant.position = Position(self.position.col, self.position.lig)
                self.survivant = None

    def recharger(self):
        """Recharge la batterie au maximum (uniquement à l'hôpital)."""
        self.batterie = self.batterie_max
        self.hors_service = False  # Une recharge réanime un drone HS (batterie = 0 seulement)

    def prendre_survivant(self, survivant: Survivant):
        """Le drone embarque le survivant."""
        survivant.etat = "porte"
        survivant.drone_porteur = self
        self.survivant = survivant

    def deposer_survivant_hopital(self) -> Survivant | None:
        """
        Livre le survivant à l'hôpital.
        Retourne le survivant sauvé ou None si le drone n'en portait pas.
        """
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
    Une tempête bloque les drones sur sa case et peut se propager en zones X.

    Attributs :
        identifiant  : "T1".."T4"
        position     : Position courante
    """

    def __init__(self, identifiant: str, position: Position):
        self.identifiant = identifiant
        self.position = position

    def __repr__(self):
        return f"Tempete({self.identifiant}, {self.position})"


# ---------------------------------------------------------------------------
# Grille
# ---------------------------------------------------------------------------

class Grille:
    """
    Plateau de jeu 12x12.
    La grille stocke des symboles de rendu (caractères) pour l'affichage,
    mais les entités sont gérées dans EtatJeu.

    Symboles :
        '.'  vide
        'B'  bâtiment
        'H'  hôpital
        'S'  survivant
        'D'  drone (si plusieurs : 'D')
        'T'  tempête
        'X'  zone dangereuse
    """

    def __init__(self):
        self.taille = GRILLE_TAILLE
        # cases[lig][col] = symbole caractère
        self.cases = [['.' for _ in range(self.taille)] for _ in range(self.taille)]

    def obtenir(self, position: Position) -> str:
        return self.cases[position.lig][position.col]

    def definir(self, position: Position, symbole: str):
        self.cases[position.lig][position.col] = symbole

    def est_libre(self, position: Position) -> bool:
        """Retourne True si la case est vide ('.')."""
        return self.cases[position.lig][position.col] == '.'


# ---------------------------------------------------------------------------
# EtatJeu
# ---------------------------------------------------------------------------

class EtatJeu:
    """
    Conteneur principal de l'état complet d'une partie.

    Attributs :
        grille      : Grille  — plateau de jeu
        hopital     : Hopital
        batiments   : list[Batiment]
        survivants  : list[Survivant]
        drones      : list[Drone]
        tempetes    : list[Tempete]
        zones_x     : set[Position]  — positions des zones dangereuses
        tour        : int  — numéro de tour courant (commence à 1)
        score       : int  — nombre de survivants livrés
        historique  : list[str]  — lignes de log
        partie_finie: bool
        victoire    : bool
    """

    def __init__(self):
        self.grille = Grille()
        self.hopital = Hopital()
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

    # ---- Helpers de recherche -------------------------------------------
    def drone_par_id(self, identifiant: str) -> Drone | None:
        """Retourne le drone correspondant à l'identifiant (ex : 'D3')."""
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
        """Retourne le survivant en attente sur cette case, ou None."""
        for s in self.survivants:
            if s.etat == "en_attente" and s.position == position:
                return s
        return None

    def drones_sur_case(self, position: Position) -> list:
        """Retourne la liste des drones actifs sur une case donnée."""
        return [d for d in self.drones if d.position == position and not d.hors_service]

    def tempete_sur_case(self, position: Position) -> Tempete | None:
        for t in self.tempetes:
            if t.position == position:
                return t
        return None

    def batiment_sur_case(self, position: Position) -> bool:
        return any(b.position == position for b in self.batiments)

    def survivants_restants(self) -> int:
        """Nombre de survivants pas encore sauvés."""
        return sum(1 for s in self.survivants if not s.est_sauve())

    def drones_actifs(self) -> list:
        return [d for d in self.drones if not d.hors_service]

    def __repr__(self):
        return (f"EtatJeu(tour={self.tour}, score={self.score}, "
                f"survivants_restants={self.survivants_restants()})")
