# Annexe — Formatage de chaînes (#9)

> Ce module court complète le Module 06. Il se concentre sur les f-strings
> et les outils d'alignement utilisés dans `affichage.py`.

---

## 1. F-strings — rappel

Une f-string (format string) permet d'insérer des variables dans une chaîne :

```python
nom = "D1"
bat = 8
print(f"Drone {nom} — batterie : {bat}")   # Drone D1 — batterie : 8
```

---

## 2. Aligner du texte

### Alignement à droite `:>N`

```python
print(f"{1:>3}")    #   1
print(f"{10:>3}")   #  10
print(f"{100:>3}")  # 100
```

Utile pour les numéros de ligne de grille.

### Alignement à gauche `:<N`

```python
print(f"{'D1':<6}")     # "D1    "
print(f"{'D12':<6}")    # "D12   "
```

Utile pour les identifiants dans un tableau de bord.

### Avec `rjust()` et `ljust()` (alternative)

```python
print(str(7).rjust(3))    #   7
print("D1".ljust(6))      # D1    
```

---

## 3. Nombres avec zéros initiaux `:0Nd`

```python
print(f"{1:02d}")    # 01
print(f"{12:02d}")   # 12
print(f"{3:04d}")    # 0003
```

Dans les logs du jeu :

```python
tour = 4
print(f"T{tour:02d}")   # T04
```

---

## 4. Largeur fixe dans un tableau

Pour que les colonnes restent alignées quelle que soit la longueur des valeurs :

```python
for drone in etat["drones"].values():
    pos = f"{drone['col']},{drone['lig']}"
    bat = f"{drone['batterie']}/{drone['batterie_max']}"
    print(f"{drone['id']:<4}  {pos:<7}  {bat:<7}")
```

Résultat aligné :

```
D1    0,5      8/20   
D2    3,2      10/20  
D3    7,1      5/20   
```

---

## 5. Cas particulier : séparateur de milliers

```python
print(f"{1500000:,}")    # 1,500,000  (séparateur anglais)
print(f"{1500000:_}")    # 1_500_000  (séparateur universel)
```

Peu utile dans ce projet, mais utile en général.

---

## 6. Exercice — Tableau de bord aligné

```python
drones = [
    {"id": "D1", "col": 0, "lig": 5, "batterie": 8, "batterie_max": 20},
    {"id": "D2", "col": 3, "lig": 2, "batterie": 15, "batterie_max": 20},
    {"id": "D3", "col": 11, "lig": 10, "batterie": 3, "batterie_max": 20},
]

print(f"{'ID':<4}  {'Position':<10}  {'Batterie'}")
print("-" * 28)
for d in drones:
    pos = f"({d['col']},{d['lig']})"
    bat = f"{d['batterie']}/{d['batterie_max']}"
    print(f"{d['id']:<4}  {pos:<10}  {bat}")

# Résultat attendu :
# ID    Position    Batterie
# ----------------------------
# D1    (0,5)       8/20
# D2    (3,2)       15/20
# D3    (11,10)     3/20
```

---

## Résumé

| Formatage | Exemple | Résultat |
|-----------|---------|----------|
| Aligné à droite | `f"{7:>4}"` | `"   7"` |
| Aligné à gauche | `f"{'D1':<6}"` | `"D1    "` |
| Zéros initiaux | `f"{4:02d}"` | `"04"` |
| `rjust` | `str(7).rjust(4)` | `"   7"` |
| `ljust` | `"D1".ljust(6)` | `"D1    "` |
