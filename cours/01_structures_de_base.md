# Module 01 — Structures de base

## Concepts couverts

- Variables et types : `int`, `float`, `str`, `bool`
- Listes : création, indexation, modification, méthodes (`append`, `pop`, `len`)
- Dictionnaires : clés/valeurs, accès, modification
- Tuples : immutabilité, déstructuration
- `None` et les valeurs manquantes

## Lien avec le projet

Dans Drone Rescue, chaque entité est d'abord représentée par un dictionnaire
(avant d'apprendre les classes au module 05) :

```python
# Un drone représenté par un dictionnaire
drone = {
    'id'         : 'D1',
    'colonne'    : 'A',   # str lettre : 'A'..'L'  ← convention du projet
    'ligne'      : 1,     # int 1-based : 1..12
    'batterie'   : 10,
    'batterie_max': 20,
    'survivant'  : None,  # None = ne porte personne
    'bloque'     : 0      # nombre de tours bloqué
}

# Accès et modification
print(drone['colonne'])       # 'A'
drone['batterie'] -= 1        # consommer 1 de batterie
drone['colonne'] = 'B'        # déplacer vers la colonne B
```

La grille est une **liste de listes** — `grille[i][j]` avec :
- `i` = index ligne = `ligne - 1`  (ex: ligne 1 → index 0)
- `j` = index colonne = `ord(colonne) - ord('A')`  (ex: 'A' → 0, 'B' → 1)

```python
# Grille 3×3 (exemple réduit)
grille = [
    ['.', 'B', '.'],   # ligne 1
    ['.', '.', 'S'],   # ligne 2
    ['H', '.', '.']    # ligne 3
]

# Accéder à la case colonne 'B', ligne 1
j = ord('B') - ord('A')  # → 1
i = 1 - 1                # → 0
case = grille[i][j]      # → 'B'
```

Une position est souvent stockée dans un **tuple immuable** :

```python
position = ('A', 1)      # (colonne str, ligne int)
col, lig = position      # déstructuration
print(f"Position : {col}{lig}")  # A1
```

## Erreurs classiques

**Erreur 1 — Modifier une liste en l'itérant**
```python
# ❌ Résultat imprévisible : D2 n'est pas retiré
drones = ['D1', 'D2', 'D3']
for d in drones:
    if d == 'D2':
        drones.remove(d)
print(drones)  # ['D1', 'D3'] ← par chance ici, mais pas toujours

# ✅ Correct : itérer sur une copie
for d in drones[:]:
    if d == 'D2':
        drones.remove(d)
```

**Erreur 2 — Utiliser `0` ou `''` à la place de `None`**
```python
# ❌ Ambigu : 0 peut être une vraie valeur de batterie
drone['survivant'] = 0      # ne porte pas de survivant ?

# ✅ Explicite : None signifie « absent »
drone['survivant'] = None
if drone['survivant'] is None:   # toujours comparer avec `is`
    print('Drone libre')
```

**Erreur 3 — Confondre index 0-based et coordonnées 1-based**
```python
# La grille est stockée en 0-based, mais le JEU parle en 1-based
ligne_jeu = 1          # ligne 1 du jeu
index_grille = ligne_jeu - 1   # → 0  (index Python)
grille[index_grille]   # ✅

# ❌ Erreur classique :
grille[ligne_jeu]      # → ligne 2 du jeu !
```

## Exercice de compréhension

**Q1.** Qu'affiche ce code ?
```python
pos = ('B', 7)
col, lig = pos
print(f"{col}{lig}")
```
<details><summary>Réponse</summary>

`B7` — déstructuration du tuple, puis f-string.
</details>

**Q2.** Un drone a `batterie = 0` et `survivant = None`. Que signifie `survivant is None` ?
<details><summary>Réponse</summary>

`True` — le drone ne porte pas de survivant. `None` représente l'absence de valeur.
</details>

**Q3.** Comment initialiser une grille 12×12 remplie de `'.'` en une ligne ?
<details><summary>Réponse</summary>

```python
grille = [['.' for _ in range(12)] for _ in range(12)]
```
</details>

## Exercices du module

Voir `exercices/ex_01_structures.py`

## Tips et best practices

- **Nomme clairement tes variables** : `batterie_drone` plutôt que `b` ou `bd`.
- **Préfère les f-strings** pour formater du texte :
  ```python
  print(f"Drone {drone['id']} en {drone['colonne']}{drone['ligne']} — bat : {drone['batterie']}")
  ```
- **Les tuples pour les coordonnées** : une position ne devrait pas être modifiable par erreur.
- **`None` est ton ami** : utilise-le explicitement pour indiquer l'absence de valeur (pas `0`, pas `''`).
- **Convention du projet** : colonnes = lettre str `'A'`…`'L'`, lignes = int `1`…`12`.

## Références

- [Docs Python — Listes](https://docs.python.org/fr/3/tutorial/datastructures.html#more-on-lists)
- [Docs Python — Dictionnaires](https://docs.python.org/fr/3/tutorial/datastructures.html#dictionaries)
- [Real Python — Python Tuples](https://realpython.com/python-tuple/)

## Prompts IA

> *« Explique-moi la différence entre une liste et un tuple en Python avec un exemple concret de jeu de plateau. »*

> *« Comment représenter une grille de jeu en Python avec une liste de listes ? Montre-moi comment accéder à une case par ses coordonnées colonne lettre + ligne entière. »*

> *« Quelle est la différence entre `None`, `False` et `0` en Python ? Quand utiliser l'un plutôt que l'autre ? »*
