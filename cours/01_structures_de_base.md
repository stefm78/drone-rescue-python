# Module 01 — Structures de base

> **Fil rouge :** Dans le jeu, un drone est un dictionnaire, une grille est une liste
> de listes, une position est un tuple. À la fin de ce module, tu sauras
> manipuler ces trois structures fondamentales.

---

## 1. Variables et types

```python
batterie = 10          # int
identifiant = "D1"    # str
hors_service = False  # bool
survivant = None      # absence de valeur
```

- `int` : entier, utilisé pour les positions, la batterie, le score
- `str` : chaîne, utilisée pour les identifiants (`"D1"`, `"S3"`)
- `bool` : vrai/faux, utilisé pour les états (`hors_service`, `partie_finie`)
- `None` : absence de valeur (le drone ne porte pas de survivant)

---

## 2. Listes — séquences modifiables

```python
batiments = [(1, 2), (3, 4), (5, 6)]   # liste de tuples

batiments.append((7, 8))    # ajouter en fin
batiments.pop()             # retirer le dernier
print(len(batiments))       # 3
print(batiments[0])         # (1, 2)
```

La grille du jeu est une **liste de listes** :

```python
GRILLE_TAILLE = 4
grille = []
for lig in range(GRILLE_TAILLE):
    ligne = []
    for col in range(GRILLE_TAILLE):
        ligne.append('.')
    grille.append(ligne)

grille[1][2] = 'D'   # drone en colonne 2 (index), ligne 1 (index)
```

---

## 3. Dictionnaires — clés et valeurs

Un drone est représenté par un dictionnaire :

```python
drone = {
    "id"          : "D1",
    "col"         : 0,       # entier (index)
    "lig"         : 5,       # entier (index)
    "batterie"    : 10,
    "batterie_max": 20,
    "survivant"   : None,
    "bloque"      : 0,
    "hors_service": False,
}

# Lire
print(drone["batterie"])    # 10

# Modifier
drone["batterie"] -= 1
drone["col"] = 1

# Vérifier l'absence
if drone["survivant"] is None:
    print("Drone libre")
```

---

## 4. Tuples — valeurs immuables

Une position est un tuple `(col, lig)` :

```python
hopital = (0, 7)   # colonne 0, ligne 7
col, lig = hopital   # déstructuration
print(f"Hôpital en col {col}, lig {lig}")
```

Un tuple ne peut pas être modifié après création.
C'est utile pour des positions fixes (hôpital, zones X) qu'on ne doit pas changer par erreur.

```python
hopital[0] = 3   # ❌ TypeError : tuple ne peut pas être modifié
```

---

## 5. List comprehension (#28)

Une **list comprehension** est une façon compacte de construire une liste.

### De la boucle classique à la comprehension

```python
# Avec une boucle classique
carres = []
for n in range(6):
    carres.append(n * n)
# carres = [0, 1, 4, 9, 16, 25]

# Équivalent avec une comprehension
carres = [n * n for n in range(6)]
```

Même chose avec une condition :

```python
# Avec une boucle + condition
survivants_restants = []
for s in survivants:
    if s["etat"] != "sauve":
        survivants_restants.append(s)

# Avec une comprehension + condition
survivants_restants = [s for s in survivants if s["etat"] != "sauve"]
```

Dans le jeu, les cases libres sont calculées ainsi :

```python
toutes_cases = [(col, lig) for col in range(taille) for lig in range(taille)]
cases_libres = [c for c in toutes_cases if c not in batiments]
```

> 💡 Règle pratique : si la comprehension fait plus d'une ligne, utilise une boucle classique.
> Lisibilité avant tout.

---

## 6. Index 0-basé vs affichage 1-basé

Dans le code, les positions sont des entiers **0-basés** (de 0 à taille-1).
Dans l'affichage, on montre des positions **1-basées** (de 1 à taille).

```python
lig_interne = 0         # index en Python
lig_affichee = lig_interne + 1   # 0 -> 1

lig_saisie = 3          # le joueur tape "3"
lig_interne = lig_saisie - 1     # 3 -> 2
```

---

## 7. Exercice A — Manipuler un dict drone

```python
drone = {
    "id": "D1", "col": 0, "lig": 0,
    "batterie": 10, "batterie_max": 20,
    "survivant": None, "bloque": 0, "hors_service": False
}

# 1. Afficher la batterie
print(drone["batterie"])   # 10

# 2. Déplacer le drone en (2, 3)
drone["col"] = 2
drone["lig"] = 3

# 3. Consommer 1 batterie
drone["batterie"] -= 1

# 4. Vérifier si le drone est libre
if drone["survivant"] is None:
    print("Libre")
```

---

## 8. Exercice B — List comprehension

```python
survivants = [
    {"id": "S1", "etat": "sauve"},
    {"id": "S2", "etat": "en_attente"},
    {"id": "S3", "etat": "sauve"},
    {"id": "S4", "etat": "en_attente"},
]

# Construire la liste des survivants non encore sauvés
restants = [s for s in survivants if s["etat"] != "sauve"]
print(len(restants))   # 2
```

---

## Erreurs classiques

**Erreur 1 — Modifier une liste pendant qu'on l'itère**
```python
# ❌ Résultat imprévisible
for d in drones:
    if d == "D2":
        drones.remove(d)

# ✅ Itérer sur une copie
for d in drones[:]:
    if d == "D2":
        drones.remove(d)
```

**Erreur 2 — Comparer `None` avec `==`**
```python
# ❌ Fonctionne souvent, mais déconseillé
if drone["survivant"] == None:
    ...

# ✅ Toujours utiliser `is`
if drone["survivant"] is None:
    ...
```

**Erreur 3 — `grille[col][lig]` au lieu de `grille[lig][col]`**
```python
# ❌ Inverse les coordonnées
grille[col][lig] = 'D'

# ✅
grille[lig][col] = 'D'
```

---

## Résumé des points clés

| Structure | Exemple | Modifiable ? |
|-----------|---------|-------------|
| Liste | `['.', 'D', '.']` | Oui |
| Dictionnaire | `{"id": "D1", "bat": 10}` | Oui |
| Tuple | `(0, 7)` | Non |
| Set | `{(1, 2), (3, 4)}` | Oui (add/discard) |

---

## Exercices du module

Voir `exercices/ex_01_structures.py`

## Prompts IA utiles

> *« Quelle différence entre une liste et un tuple en Python ? Quand utiliser l'un plutôt que l'autre ? »*

> *« Comment construire une liste avec une condition en Python (list comprehension) ? »*

> *« Comment représenter une grille de jeu en Python avec une liste de listes ? »*
