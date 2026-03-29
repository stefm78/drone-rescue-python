# Module 02 — Boucles et conditions

## Concepts couverts

- `if`, `elif`, `else` — conditions
- Opérateurs de comparaison et logiques : `==`, `!=`, `<`, `>`, `and`, `or`, `not`
- `for` sur une liste, un range, un dictionnaire
- `while` avec condition d'arrêt
- `break`, `continue`
- `enumerate()`, `range()`

## Lien avec le projet

```python
# Parcourir toute la grille pour afficher les cases
COLS = list('ABCDEFGHIJKL')
for row in range(12):
    for col_idx, col in enumerate(COLS):
        case = grille[row][col_idx]
        print(case, end='  ')
    print()  # saut de ligne en fin de rangée

# Boucle de saisie — répéter jusqu'à saisie valide
while True:
    commande = input('> ').strip().lower()
    if commande == 'next':
        break
    if commande in ('ok', 'annuler'):
        traiter(commande)
        break
    print('  Commande non reconnue. Tapez next, ok ou annuler.')

# Compter les survivants restants
survivants_restants = sum(
    1 for s in survivants if not s['sauve']
)
```

## Exercices du module

Voir `exercices/ex_02_boucles.py`

## Tips et best practices

- **Évite les boucles infinies non contrôlées** : toujours prévoir un `break` ou une condition de sortie claire.
- **`enumerate()` plutôt que `range(len(...))`** :
  ```python
  # Mauvais
  for i in range(len(drones)):
      print(drones[i])
  # Bon
  for i, drone in enumerate(drones):
      print(i, drone)
  ```
- **`any()` et `all()`** pour tester des conditions sur des collections :
  ```python
  tous_sauves = all(s['sauve'] for s in survivants)
  un_hs = any(d['batterie'] == 0 for d in drones)
  ```

## Références

- [Docs Python — Structures de contrôle](https://docs.python.org/fr/3/tutorial/controlflow.html)
- [Real Python — Python for Loops](https://realpython.com/python-for-loop/)
- [Real Python — Python while Loops](https://realpython.com/python-while-loop/)

## Prompts IA

> *« Comment sécuriser une saisie utilisateur en Python dans une boucle while pour éviter les crashs ? »*

> *« Explique-moi la différence entre break et continue en Python avec des exemples clairs. »*

> *« Comment parcourir une grille 2D en Python et tester chaque case ? »*
