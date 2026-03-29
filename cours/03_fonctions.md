# Module 03 — Fonctions

## Concepts couverts

- Définir une fonction : `def`, paramètres, `return`
- Paramètres positionnels vs nommés
- Valeurs par défaut
- Portée des variables (locale vs globale)
- Docstrings
- Type hints (annotations)

## Lien avec le projet

```python
def distance_chebyshev(pos_a: tuple, pos_b: tuple) -> int:
    """
    Calcule la distance de Chebyshev entre deux positions.
    Cette distance autorise les déplacements diagonaux.
    
    Args:
        pos_a: tuple (col_idx, row_idx) de départ
        pos_b: tuple (col_idx, row_idx) d'arrivée
    
    Returns:
        Distance entière (nombre de cases, diagonale = 1)
    """
    return max(abs(pos_a[0] - pos_b[0]), abs(pos_a[1] - pos_b[1]))


def coord_valide(col: str, row: int, taille: int = 12) -> bool:
    """Vérifie qu'une coordonnée est dans les limites de la grille."""
    COLS = list('ABCDEFGHIJKL')[:taille]
    return col in COLS and 1 <= row <= taille


def resumer_drone(drone: dict) -> str:
    """Retourne une ligne de résumé formatée pour le tableau de bord."""
    surv = drone['survivant'] if drone['survivant'] else '—'
    blq = f"{drone['bloque']}t" if drone['bloque'] > 0 else ('HS' if drone['batterie'] == 0 else '—')
    col_lettre = 'ABCDEFGHIJKL'[drone['col']]
    return f"  {drone['id']:<4} {col_lettre}{drone['row']:<4}  {drone['batterie']:>2}/{drone['batterie_max']:<2}   {surv:<5}  {blq}"
```

## Exercices du module

Voir `exercices/ex_03_fonctions.py`

## Tips et best practices

- **Une fonction = une responsabilité** : si ta fonction fait plus d'une chose, découpe-la.
- **Toujours écrire une docstring** pour les fonctions non triviales.
- **Utilise les type hints** : ils documentent le code et aident les IDE.
- **Nomme avec verbe + nom** : `calculer_distance`, `valider_mouvement`, `afficher_grille`.
- **Évite les variables globales** : passe les données en paramètre.

## Références

- [Docs Python — Définir des fonctions](https://docs.python.org/fr/3/tutorial/controlflow.html#defining-functions)
- [PEP 257 — Docstrings](https://peps.python.org/pep-0257/)
- [PEP 484 — Type Hints](https://peps.python.org/pep-0484/)
- [Real Python — Python Type Checking](https://realpython.com/python-type-checking/)

## Prompts IA

> *« Explique-moi le principe de responsabilité unique appliqué aux fonctions Python, avec un exemple de jeu. »*

> *« Qu'est-ce que la portée des variables en Python ? Pourquoi faut-il éviter les variables globales ? »*

> *« Comment écrire une bonne docstring Python ? Montre-moi le format Google et le format NumPy. »*
