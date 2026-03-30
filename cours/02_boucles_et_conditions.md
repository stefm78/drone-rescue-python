# Module 02 — Boucles et conditions

## Concepts couverts

- `if`, `elif`, `else` — conditions
- Opérateurs de comparaison et logiques : `==`, `!=`, `<`, `>`, `and`, `or`, `not`
- `for` sur une liste, un range, un dictionnaire
- `while` avec condition d'arrêt
- `break`, `continue`
- `enumerate()`, `range()`
- `any()`, `all()`

## Lien avec le projet

```python
# Parcourir toute la grille pour afficher les cases
COLS = list('ABCDEFGHIJKL')
for i_lig in range(12):          # i_lig = 0..11
    for i_col, col in enumerate(COLS):
        case = grille[i_lig][i_col]
        print(case, end='  ')
    print()  # saut de ligne en fin de rangée

# Boucle de saisie — répéter jusqu'à saisie valide
while True:
    commande = input('> ').strip().upper()
    if commande == 'NEXT':
        break
    if commande in ('OK', 'QUIT'):
        traiter(commande)
        break
    print('  Commande non reconnue.')

# Compter les survivants restants avec all() / any()
tous_sauves = all(s['sauve'] for s in survivants)  # fin de partie ?
un_hs      = any(d['batterie'] == 0 for d in drones)
survivants_restants = sum(1 for s in survivants if not s['sauve'])

# Vérifier si un drone peut se déplacer
colonne_cible = 'E'
ligne_cible   = 6
cols_valides  = list('ABCDEFGHIJKL')
if colonne_cible in cols_valides and 1 <= ligne_cible <= 12:
    print('Cible dans la grille')
```

## Erreurs classiques

**Erreur 1 — Boucle infinie sans `break`**
```python
# ❌ La condition ne change jamais → boucle infinie
while True:
    commande = input('> ')
    print(f'Commande : {commande}')
    # oubli du break !

# ✅ Toujours prévoir une sortie
while True:
    commande = input('> ').strip().upper()
    if commande in ('NEXT', 'QUIT'):
        break
    print('Commande non reconnue')
```

**Erreur 2 — `range(len(...))` au lieu de `enumerate()`**
```python
# ❌ Verbeux et risqué (index hors limites possible)
for i in range(len(drones)):
    print(i, drones[i])

# ✅ Pythonique
for i, drone in enumerate(drones):
    print(i, drone)
```

**Erreur 3 — `==` vs `is` avec `None`**
```python
# ❌ Peut donner des résultats surprenants
if drone['survivant'] == None:  # déconseillé
    ...

# ✅ Toujours utiliser `is` ou `is not` avec None
if drone['survivant'] is None:
    ...
```

**Erreur 4 — `continue` mal placé**
```python
# ❌ L'affichage est sauté mais le compteur aussi
for d in drones:
    if d['batterie'] == 0:
        continue          # saute tout ce qui suit
    print(d['id'])        # ← jamais exécuté pour les HS
    compteur += 1

# ✅ Tester explicitement ce qu'on veut
for d in drones:
    if d['batterie'] > 0:
        print(d['id'])
        compteur += 1
```

## Exercice de compréhension

**Q1.** Que retourne `all(d['batterie'] == 0 for d in drones)` si la liste est vide ?
<details><summary>Réponse</summary>

`True` — `all()` sur une séquence vide retourne toujours `True` (convention mathématique). Il faut donc vérifier que la liste n'est pas vide avant.
</details>

**Q2.** Quelle est la différence entre `break` et `continue` ?
<details><summary>Réponse</summary>

`break` quitte entièrement la boucle. `continue` passe à l'itération suivante sans exécuter le reste du corps.
</details>

**Q3.** Comment afficher les colonnes A à L avec `range()` sans écrire la liste ?
<details><summary>Réponse</summary>

```python
for i in range(12):
    print(chr(ord('A') + i), end=' ')
```
</details>

## Exercices du module

Voir `exercices/ex_02_boucles.py`

## Tips et best practices

- **Évite les boucles infinies non contrôlées** : toujours prévoir un `break` ou une condition de sortie claire.
- **`enumerate()` plutôt que `range(len(...))`** — plus lisible, moins d'erreurs.
- **`any()` et `all()`** pour tester des conditions sur des collections :
  ```python
  tous_sauves = all(s['sauve'] for s in survivants)
  un_hs       = any(d['batterie'] == 0 for d in drones)
  ```
- **`is None` / `is not None`** — ne jamais utiliser `== None`.

## Références

- [Docs Python — Structures de contrôle](https://docs.python.org/fr/3/tutorial/controlflow.html)
- [Real Python — Python for Loops](https://realpython.com/python-for-loop/)
- [Real Python — Python while Loops](https://realpython.com/python-while-loop/)

## Prompts IA

> *« Comment sécuriser une saisie utilisateur en Python dans une boucle while pour éviter les crashs ? »*

> *« Explique-moi la différence entre break et continue en Python avec des exemples clairs. »*

> *« Comment parcourir une grille 2D en Python et tester chaque case ? »*
