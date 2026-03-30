# Module 05 — Dictionnaires, sets et structures de données avancées

> **Fil rouge :** Dans le jeu Drone Rescue, chaque drone est un dictionnaire.
> À la fin de ce module, tu sauras créer, lire, modifier et utiliser des dicts et des sets
> exactement comme le fait le code du jeu.

---

## 1. Rappel : qu'est-ce qu'un dictionnaire ?

Un dictionnaire associe des **clés** à des **valeurs**.
Pense-y comme une fiche de renseignements : chaque champ a un nom (la clé) et un contenu (la valeur).

```python
drone = {
    "id"          : "D1",
    "col"         : 0,
    "lig"         : 5,
    "batterie"    : 10,
    "batterie_max": 20,
    "survivant"   : None,
    "bloque"      : 0,
    "hors_service": False
}
```

- Les clés sont des chaînes de caractères (`"id"`, `"col"`, …)
- Les valeurs peuvent être de n'importe quel type : `int`, `str`, `bool`, `None`
- On accède à une valeur avec `drone["batterie"]`
- On la modifie avec `drone["batterie"] -= 1`

---

## 2. Opérations essentielles

### Lire une valeur

```python
print(drone["id"])          # D1
print(drone["batterie"])    # 10
```

### Modifier une valeur

```python
drone["batterie"] -= 1      # consommer 1 unité
drone["bloque"] = 2         # bloquer le drone 2 tours
```

### Ajouter une clé

```python
drone["mission"] = "secours"   # nouvelle clé
```

### Vérifier si une clé existe

```python
if "survivant" in drone:
    print("Le drone a une clé survivant")
```

### Valeur par défaut avec `.get()`

```python
mission = drone.get("mission", "aucune")   # "aucune" si la clé n'existe pas
```

---

## 3. Dictionnaire de dictionnaires

Dans le jeu, **tous les drones** sont regroupés dans un seul dictionnaire :

```python
drones = {
    "D1": {"id": "D1", "col": 0, "lig": 5, "batterie": 10,
           "batterie_max": 20, "survivant": None, "bloque": 0, "hors_service": False},
    "D2": {"id": "D2", "col": 3, "lig": 2, "batterie": 8,
           "batterie_max": 20, "survivant": None, "bloque": 0, "hors_service": False},
    "D3": {"id": "D3", "col": 7, "lig": 1, "batterie": 10,
           "batterie_max": 20, "survivant": None, "bloque": 0, "hors_service": False},
}
```

Pour accéder au drone D2 :

```python
d2 = drones["D2"]
print(d2["batterie"])    # 8
```

Pour modifier la batterie de D2 directement :

```python
drones["D2"]["batterie"] -= 1
```

### Parcourir tous les drones

```python
for identifiant, drone in drones.items():
    print(identifiant, "→ batterie :", drone["batterie"])
```

`items()` retourne des paires (clé, valeur). C'est la façon standard de parcourir un dict.

---

## 4. Fonctions de création

Plutôt que de recopier le dictionnaire à chaque fois, on crée une **fonction** qui retourne un dict prêt à l'emploi :

```python
def creer_drone(identifiant, col, lig):
    """Retourne un dictionnaire représentant un drone."""
    return {
        "id"          : identifiant,
        "col"         : col,
        "lig"         : lig,
        "batterie"    : 10,
        "batterie_max": 20,
        "survivant"   : None,
        "bloque"      : 0,
        "hors_service": False,
    }

# Utilisation
d1 = creer_drone("D1", 0, 5)
d2 = creer_drone("D2", 3, 2)
```

**Avantage :** si tu veux ajouter un champ à tous les drones, tu ne modifies qu'un seul endroit.

> 💡 C'est le même raisonnement qu'une classe `__init__` — mais sans la syntaxe de classe.
> Pour ce projet, les dictionnaires suffisent et restent plus lisibles pour un débutant.

---

## 5. Exercice A — Créer un survivant

Écris la fonction `creer_survivant(identifiant, col, lig)` qui retourne un dictionnaire avec :
- `"id"` : l'identifiant
- `"col"` et `"lig"` : la position
- `"etat"` : `"en_attente"` par défaut

```python
# À compléter
def creer_survivant(identifiant, col, lig):
    return {
        # ...
    }

# Test
s1 = creer_survivant("S1", 4, 7)
print(s1["etat"])   # doit afficher : en_attente
```

---

## 6. Sets — ensembles de valeurs uniques

Un **set** est une collection **sans ordre** et **sans doublons**.
Dans le jeu, les positions occupées sont stockées dans un set :

```python
occupees = set()
occupees.add((0, 5))    # position du drone D1
occupees.add((3, 2))    # position du drone D2
occupees.add((0, 5))    # déjà présent → ignoré silencieusement

print(len(occupees))    # 2, pas 3
```

### Pourquoi des tuples comme éléments ?

Un set ne peut contenir que des valeurs **immuables** (qu'on ne peut pas modifier).
Un tuple `(col, lig)` est immuable — contrairement à une liste `[col, lig]`.

```python
occupees.add((3, 5))    # ✅ tuple : OK
occupees.add([3, 5])    # ❌ liste : TypeError
```

### Tester la présence d'une position

```python
if (3, 5) in occupees:
    print("Case occupée")
```

La recherche dans un set est **très rapide** (O(1)), même avec beaucoup d'éléments.
C'est pour ça qu'on préfère un set à une liste pour les positions occupées.

### Opérations courantes

```python
zones_x = {(1, 2), (3, 4), (5, 6)}

zones_x.add((7, 8))          # ajouter une position
zones_x.discard((1, 2))      # supprimer (sans erreur si absent)
print(len(zones_x))          # nombre de zones

# Parcourir
for pos in zones_x:
    col, lig = pos
    print(f"Zone X en colonne {col}, ligne {lig}")
```

---

## 7. Exercice B — Positions occupées

```python
# Données
drones = {
    "D1": {"col": 0, "lig": 5},
    "D2": {"col": 3, "lig": 2},
    "D3": {"col": 7, "lig": 1},
}

# Question : construire le set des positions occupées par les drones
occupees = set()
for drone in drones.values():
    occupees.add((drone["col"], drone["lig"]))

print(occupees)
# {(0, 5), (3, 2), (7, 1)}

# Vérifier si la case (3, 2) est libre
if (3, 2) in occupees:
    print("Occupée")   # → Occupée
```

---

## 8. L'état du jeu — un grand dictionnaire

Toutes les données du jeu sont regroupées dans un seul dictionnaire `etat` :

```python
etat = {
    "tour"        : 1,
    "score"       : 0,
    "partie_finie": False,
    "victoire"    : False,
    "grille"      : [['.'] * 8 for _ in range(8)],
    "hopital"     : (0, 7),              # tuple (col, lig)
    "batiments"   : [(2, 3), (5, 1)],   # liste de tuples
    "drones"      : {"D1": {...}, "D2": {...}},
    "tempetes"    : {"T1": {...}},
    "survivants"  : {"S1": {...}, "S2": {...}},
    "zones_x"     : {(1, 4), (6, 2)},   # set de tuples
    "historique"  : [],                  # liste de lignes de log
}
```

Passer ce dictionnaire à une fonction permet de lui donner accès à tout l'état du jeu :

```python
def verifier_fin_partie(etat):
    """Retourne True si tous les survivants sont sauvés."""
    for s in etat["survivants"].values():
        if s["etat"] != "sauve":
            return False
    return True
```

---

## 9. Exercice C — Compter les drones actifs

Écris la fonction `compter_drones_actifs(etat)` qui retourne le nombre de drones
qui ne sont pas hors service.

```python
def compter_drones_actifs(etat):
    nb = 0
    for drone in etat["drones"].values():
        if not drone["hors_service"]:
            nb += 1
    return nb
```

---

## Résumé des points clés

| Concept | Syntaxe | À retenir |
|---------|---------|----------|
| Lire une valeur | `drone["batterie"]` | Clé entre guillemets |
| Modifier | `drone["batterie"] -= 1` | Comme une variable |
| Valeur par défaut | `drone.get("x", 0)` | Évite le KeyError |
| Parcourir | `for k, v in d.items()` | Clé ET valeur |
| Set — ajouter | `s.add((col, lig))` | Tuple immuable |
| Set — tester | `if pos in s` | Rapide |
| Passer à une fonction | `f(etat)` | Un seul paramètre = tout l'état |

---

## Pour aller plus loin (lecture seule)

La **Programmation Orientée Objet (POO)** permet de regrouper données et fonctions
dans une `class`. C'est une alternative aux dictionnaires que tu rencontreras en
Java, C++ ou dans des projets Python plus avancés.

Exemple minimal (ne pas écrire, juste lire) :

```python
class Drone:
    def __init__(self, identifiant, col, lig):
        self.id = identifiant
        self.col = col
        self.lig = lig
        self.batterie = 10

d = Drone("D1", 0, 5)
print(d.batterie)   # 10
```

La syntaxe `d.batterie` correspond à `drone["batterie"]` dans notre approche.
Les deux sont valides — pour ce projet, les dictionnaires suffisent.
