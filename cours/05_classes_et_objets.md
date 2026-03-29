# Module 05 — Classes et objets

## Concepts couverts

- `class` — définition
- `__init__` — constructeur
- Attributs d'instance
- Méthodes
- `__str__` — représentation textuelle
- `@property` — attribut calculé
- Héritage simple

## Lien avec le projet

```python
class EntiteGrille:
    """Classe de base pour tout objet positionné sur la grille."""
    def __init__(self, id_: str, col: int, row: int):
        self.id = id_
        self.col = col   # index 0-11
        self.row = row   # index 0-11

    @property
    def position_str(self) -> str:
        """Position humainement lisible ex: 'B7'"""
        return f"{'ABCDEFGHIJKL'[self.col]}{self.row + 1}"

    def __str__(self) -> str:
        return f"{self.id}@{self.position_str}"


class Drone(EntiteGrille):
    """Drone de sauvetage."""
    def __init__(self, id_: str, col: int, row: int,
                 batterie_init: int = 10, batterie_max: int = 20):
        super().__init__(id_, col, row)
        self.batterie = batterie_init
        self.batterie_max = batterie_max
        self.survivant = None    # Survivant porté ou None
        self.bloque = 0          # Tours de blocage restants

    @property
    def est_hs(self) -> bool:
        """True si batterie vide."""
        return self.batterie <= 0

    @property
    def est_bloque(self) -> bool:
        return self.bloque > 0

    def resumer(self) -> str:
        """Ligne du tableau de bord."""
        surv = self.survivant.id if self.survivant else '—'
        if self.est_hs:
            blq = 'HS'
        elif self.est_bloque:
            blq = f'{self.bloque}t'
        else:
            blq = '—'
        return (f"  {self.id:<4} {self.position_str:<5} "
                f"{self.batterie:>2}/{self.batterie_max:<2}   {surv:<5}  {blq}")


class Tempete(EntiteGrille):
    """Tempête mobile sur la grille."""
    pass  # hérite de EntiteGrille — ajouts possibles


class Survivant(EntiteGrille):
    def __init__(self, id_: str, col: int, row: int):
        super().__init__(id_, col, row)
        self.sauve = False
        self.porte_par = None  # Drone qui le porte
```

## Exercices du module

Voir `exercices/ex_05_classes.py`

## Tips et best practices

- **`@property` pour les attributs calculés** : évite de stocker une valeur dérivée.
- **`__str__` toujours utile** : permet `print(mon_objet)` lisible.
- **`super().__init__(...)` pour l'héritage** : appel obligatoire du constructeur parent.
- **Ne pas abuser de l'héritage** : préfère la composition quand les classes sont trop différentes.

## Références

- [Docs Python — Classes](https://docs.python.org/fr/3/tutorial/classes.html)
- [Real Python — Python OOP](https://realpython.com/python3-object-oriented-programming/)
- [Real Python — @property](https://realpython.com/python-property/)

## Prompts IA

> *« Explique-moi le concept d'héritage en Python avec un exemple concret de jeu de plateau. »*

> *« Quelle est la différence entre un attribut de classe et un attribut d'instance en Python ? »*

> *« Quand utiliser @property plutôt qu'un attribut normal en Python ? »*
