# Module 05 — Classes et objets

## Concepts couverts

- `class` — définition
- `__init__` — constructeur
- Attributs d'instance
- Méthodes
- `__str__` — représentation textuelle
- `@property` — attribut calculé (lecture seule)
- Héritage simple et `super()`

## Lien avec le projet

**Convention de coordonnées (identique partout dans le projet) :**
```python
# colonne : str lettre 'A'..'L'
# ligne   : int 1-based 1..12
# Conversion interne : ord(colonne) - ord('A') → index 0-based
```

```python
class EntiteGrille:
    """Classe de base pour tout objet positionné sur la grille."""

    def __init__(self, identifiant: str, colonne: str, ligne: int):
        self.identifiant = identifiant
        self.colonne = colonne   # str : 'A'..'L'
        self.ligne   = ligne     # int : 1..12

    @property
    def position_str(self) -> str:
        """Position lisible ex: 'B7' — calculée, pas stockée."""
        return f"{self.colonne}{self.ligne}"

    def __str__(self) -> str:
        return f"{self.identifiant}@{self.position_str}"


class Drone(EntiteGrille):
    """Drone de sauvetage."""

    def __init__(self, identifiant: str, colonne: str, ligne: int,
                 batterie_init: int = 10, batterie_max: int = 20):
        super().__init__(identifiant, colonne, ligne)  # appel obligatoire
        self.batterie     = batterie_init
        self.batterie_max = batterie_max
        self.survivant    = None   # Survivant porté ou None
        self.bloque       = 0      # Tours de blocage restants

    @property
    def est_hs(self) -> bool:
        """True si batterie épuisée — @property : pas de parenthèses à l'appel."""
        return self.batterie <= 0

    @property
    def est_bloque(self) -> bool:
        return self.bloque > 0

    def consommer_batterie(self):
        """Soustrait 1 à la batterie (plancher 0)."""
        self.batterie = max(0, self.batterie - 1)

    def resumer(self) -> str:
        """Ligne du tableau de bord."""
        surv = self.survivant.identifiant if self.survivant else '—'
        blq  = 'HS' if self.est_hs else (f'{self.bloque}t' if self.est_bloque else '—')
        return (
            f"  {self.identifiant:<4} {self.position_str:<5} "
            f"{self.batterie:>2}/{self.batterie_max:<2}   {surv:<5}  {blq}"
        )


class Tempete(EntiteGrille):
    """Tempête mobile sur la grille."""

    def __init__(self, identifiant: str, colonne: str, ligne: int, depl_max: int = 2):
        super().__init__(identifiant, colonne, ligne)
        self.depl_max      = depl_max
        self.depl_restants = depl_max

    def reset_tour(self):
        """Remet le compteur de déplacements au maximum en début de tour."""
        self.depl_restants = self.depl_max


class Survivant(EntiteGrille):
    def __init__(self, identifiant: str, colonne: str, ligne: int):
        super().__init__(identifiant, colonne, ligne)
        self.sauve     = False
        self.porte_par = None  # Drone qui le porte
```

## Erreurs classiques

**Erreur 1 — Oublier `self` dans une méthode**
```python
# ❌ Python cherche une variable locale `batterie`
def consommer_batterie():
    batterie = max(0, batterie - 1)   # NameError !

# ✅ Toujours passer self en premier paramètre
def consommer_batterie(self):
    self.batterie = max(0, self.batterie - 1)
```

**Erreur 2 — Oublier `super().__init__()` dans l'héritage**
```python
# ❌ Les attributs de EntiteGrille (identifiant, colonne, ligne) ne sont pas créés
class Drone(EntiteGrille):
    def __init__(self, identifiant, colonne, ligne):
        self.batterie = 10   # AttributeError plus tard : self.identifiant introuvable

# ✅
class Drone(EntiteGrille):
    def __init__(self, identifiant, colonne, ligne):
        super().__init__(identifiant, colonne, ligne)  # initialise identifiant, colonne, ligne
        self.batterie = 10
```

**Erreur 3 — Appeler un `@property` avec des parenthèses**
```python
d = Drone('D1', 'A', 1)
print(d.est_hs())   # ❌ TypeError : 'bool' object is not callable
print(d.est_hs)     # ✅ True ou False
```

## Exercice de compréhension

**Q1.** Quelle est la différence entre un attribut d'instance et un `@property` ?
<details><summary>Réponse</summary>

Un attribut d'instance est stocké en mémoire (`self.batterie = 10`). Un `@property` est une méthode déguisée en attribut : elle est recalculée à chaque accès (`self.est_hs` recalcule `self.batterie <= 0`).
</details>

**Q2.** Pourquoi `EntiteGrille` est-elle utile ici ?
<details><summary>Réponse</summary>

Elle factorise le code commun à `Drone`, `Tempete` et `Survivant` (identifiant, colonne, ligne, `position_str`, `__str__`). Sans elle, ce code serait dupliqué dans chaque classe.
</details>

**Q3.** `d = Drone('D1', 'A', 1)` — que retourne `str(d)` ?
<details><summary>Réponse</summary>

`'D1@A1'` — `__str__` est hérité de `EntiteGrille` et appelle `position_str`.
</details>

## Exercices du module

Voir `exercices/ex_05_classes.py`

## Tips et best practices

- **`@property` pour les attributs calculés** : évite de stocker une valeur dérivée.
- **`__str__` toujours utile** : permet `print(mon_objet)` lisible.
- **`super().__init__(...)` pour l'héritage** : appel obligatoire du constructeur parent.
- **Ne pas abuser de l'héritage** : préfère la composition quand les classes sont trop différentes.
- **Convention du projet** : `colonne: str` (`'A'`…`'L'`), `ligne: int` (`1`…`12`).

## Références

- [Docs Python — Classes](https://docs.python.org/fr/3/tutorial/classes.html)
- [Real Python — Python OOP](https://realpython.com/python3-object-oriented-programming/)
- [Real Python — @property](https://realpython.com/python-property/)

## Prompts IA

> *« Explique-moi le concept d'héritage en Python avec un exemple concret de jeu de plateau. »*

> *« Quelle est la différence entre un attribut de classe et un attribut d'instance en Python ? »*

> *« Quand utiliser @property plutôt qu'un attribut normal en Python ? »*
