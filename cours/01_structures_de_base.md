# Module 01 — Structures de base

## Concepts couverts

- Variables et types : `int`, `float`, `str`, `bool`
- Listes : création, indexation, modification, méthodes (`append`, `pop`, `len`)
- Dictionnaires : clés/valeurs, accès, modification
- Tuples : immutabilité, déstructuration
- `None` et les valeurs manquantes

## Lien avec le projet

Dans Drone Rescue, chaque entité est représentée par un dictionnaire ou une classe :

```python
# Un drone représenté par un dictionnaire (avant d'apprendre les classes)
drone = {
    'id': 'D1',
    'col': 0,     # colonne (0 = 'A')
    'row': 0,     # ligne (0 = ligne 1)
    'batterie': 10,
    'batterie_max': 20,
    'survivant': None,   # None = ne porte personne
    'bloque': 0          # nombre de tours bloqué
}

# Une position stockée dans un tuple
position = ('A', 1)
col, row = position   # déstructuration
```

La grille est une **liste de listes** :

```python
# Grille 3x3 (exemple réduit)
grille = [
    ['.', 'B', '.'],
    ['.', '.', 'S'],
    ['H', '.', '.']
]

# Accès à la case (colonne B, ligne 1) → index [0][1]
case = grille[0][1]   # → 'B'
```

## Exercices du module

Voir `exercices/ex_01_structures.py`

## Tips et best practices

- **Nomme clairement tes variables** : `batterie_drone` plutôt que `b` ou `bd`.
- **Préfère les f-strings** pour formater du texte :
  ```python
  print(f"Drone {drone['id']} en position ({col}, {row}) — batterie : {drone['batterie']}")
  ```
- **Les tuples pour les coordonnées** : une position ne devrait pas être modifiable par erreur.
- **`None` est ton ami** : utilise-le explicitement pour indiquer l'absence de valeur (pas `0`, pas `''`).

## Références

- [Docs Python — Listes](https://docs.python.org/fr/3/tutorial/datastructures.html#more-on-lists)
- [Docs Python — Dictionnaires](https://docs.python.org/fr/3/tutorial/datastructures.html#dictionaries)
- [Real Python — Python Tuples](https://realpython.com/python-tuple/)

## Prompts IA

> *« Explique-moi la différence entre une liste et un tuple en Python avec un exemple concret de jeu de plateau. »*

> *« Comment représenter une grille de jeu en Python avec une liste de listes ? Montre-moi comment accéder à une case par ses coordonnées. »*

> *« Quelle est la différence entre `None`, `False` et `0` en Python ? Quand utiliser l'un plutôt que l'autre ? »*
