# Module 03 — Fonctions

> **Fil rouge :** `logique.py` est entièrement composé de fonctions.
> À la fin de ce module, tu sauras définir des fonctions claires,
> gérer les erreurs de saisie et retourner plusieurs valeurs.

---

## 1. Définir une fonction

```python
def saluer(prenom):
    """Affiche un message de bienvenue."""
    print(f"Bonjour {prenom} !")

saluer("Lena")   # Bonjour Lena !
```

Une fonction :
- commence par `def`
- a un nom en minuscules avec des `_`
- peut avoir des **paramètres** (variables reçues)
- peut **retourner** une valeur avec `return`

---

## 2. Retourner une valeur

```python
def distance_chebyshev(col1, lig1, col2, lig2):
    """Distance entre deux cases, diagonale = 1 déplacement."""
    return max(abs(col2 - col1), abs(lig2 - lig1))

d = distance_chebyshev(0, 0, 2, 1)
print(d)   # 2
```

Sans `return`, la fonction retourne `None` — c'est une erreur classique.

---

## 3. Retourner plusieurs valeurs (tuple)

Dans le jeu, `valider_mouvement()` retourne à la fois un booléen ET un message :

```python
def valider_mouvement(etat, drone, cible):
    """Retourne (True, '') ou (False, message d'erreur)."""
    if drone["hors_service"]:
        return False, f"{drone['id']} est hors service"
    if drone["bloque"] > 0:
        return False, f"{drone['id']} est bloqué"
    # ... autres vérifications ...
    return True, ""

# Utilisation
ok, raison = valider_mouvement(etat, drone, cible)
if not ok:
    print(f"Refusé : {raison}")
```

La syntaxe `ok, raison = ...` s'appelle la **déstructuration** : elle décompose
automatiquement le tuple retourné en plusieurs variables.

---

## 4. Paramètres par défaut

```python
def creer_drone(identifiant, col, lig, batterie=10):
    """Crée un drone avec batterie par défaut = 10."""
    return {
        "id"       : identifiant,
        "col"      : col,
        "lig"      : lig,
        "batterie" : batterie,
    }

d1 = creer_drone("D1", 0, 0)         # batterie = 10 (défaut)
d2 = creer_drone("D2", 3, 2, 5)      # batterie = 5  (spécifié)
```

> ⚠️ Ne jamais utiliser une liste ou un dict comme valeur par défaut.
> Utiliser `None` comme sentinelle à la place.

```python
# ❌ Danger : la liste est partagée entre tous les appels
def ajouter(item, liste=[]):
    liste.append(item)
    return liste

# ✅
def ajouter(item, liste=None):
    if liste is None:
        liste = []
    liste.append(item)
    return liste
```

---

## 5. Gérer les erreurs de saisie avec `try/except` (#17)

Quand l'utilisateur tape quelque chose d'inattendu, Python peut lever une exception.
On la capture avec `try/except` pour éviter le crash.

### `ValueError` — conversion impossible

```python
def lire_entier(message):
    """Demande un entier à l'utilisateur. Retourne None si invalide."""
    saisie = input(message)
    try:
        return int(saisie)
    except ValueError:
        print(f"'{saisie}' n'est pas un entier valide.")
        return None

n = lire_entier("Combien de drones ? ")
if n is not None:
    print(f"Lancement avec {n} drones")
```

`int("abc")` lève une `ValueError`. En la capturant, on évite le crash
et on peut afficher un message lisible.

### Dans `position_depuis_chaine()`

```python
def position_depuis_chaine(texte):
    texte = texte.strip().upper()
    if len(texte) < 2:
        return None
    lettre = texte[0]
    try:
        lig = int(texte[1:]) - 1   # "3" -> 2, "abc" -> ValueError
    except ValueError:
        return None                 # saisie invalide, on retourne None
    ...
```

### Structure générale

```python
try:
    # Code qui peut échouer
    valeur = int(saisie)
except ValueError:
    # Ce qui se passe si int() échoue
    print("Entier attendu")
    valeur = 0
```

---

## 6. Docstrings et lisibilité

```python
def creer_survivant(identifiant, col, lig):
    """
    Retourne un dictionnaire représentant un survivant.

    Args:
        identifiant : str  ex. 'S1'
        col         : int  colonne (0-basé)
        lig         : int  ligne (0-basé)

    Returns:
        dict avec clés id, col, lig, etat
    """
    return {
        "id"  : identifiant,
        "col" : col,
        "lig" : lig,
        "etat": "en_attente",
    }
```

Une bonne docstring répond à : *Que fait cette fonction ? Que reçoit-elle ? Que retourne-t-elle ?*

---

## 7. Exercice A — Fonction avec `try/except`

```python
# Écris la fonction lire_position() qui :
# - demande une saisie (ex: "B3")
# - retourne le tuple (col_entier, lig_entier) si valide
# - retourne None si invalide
# - utilise try/except pour gérer l'erreur de conversion

LETTRES = ["A", "B", "C", "D", "E", "F", "G", "H"]

def lire_position():
    saisie = input("Position : ").strip().upper()
    if len(saisie) < 2 or saisie[0] not in LETTRES:
        return None
    try:
        lig = int(saisie[1:]) - 1
    except ValueError:
        return None
    col = LETTRES.index(saisie[0])
    return (col, lig)
```

---

## 8. Exercice B — Retour multiple

```python
# La fonction vérifie si une case est dans la grille.
# Elle retourne (True, "") ou (False, message).

def case_valide(col, lig, taille=8):
    if not (0 <= col < taille):
        return False, f"Colonne {col} hors grille (0-{taille-1})"
    if not (0 <= lig < taille):
        return False, f"Ligne {lig} hors grille (0-{taille-1})"
    return True, ""

ok, msg = case_valide(3, 10)
print(ok, msg)   # False  Ligne 10 hors grille (0-7)
```

---

## Erreurs classiques

**Erreur 1 — Oublier `return`**
```python
# ❌ Retourne None silencieusement
def distance(col1, lig1, col2, lig2):
    max(abs(col2 - col1), abs(lig2 - lig1))   # calculé mais jamais retourné !

# ✅
def distance(col1, lig1, col2, lig2):
    return max(abs(col2 - col1), abs(lig2 - lig1))
```

**Erreur 2 — Capturer toutes les exceptions**
```python
# ❌ Cache les vraies erreurs (bugs, typos, ...)
try:
    valeur = int(saisie)
except Exception:
    valeur = 0

# ✅ Capturer uniquement l'erreur attendue
try:
    valeur = int(saisie)
except ValueError:
    valeur = 0
```

**Erreur 3 — Mutable comme valeur par défaut**
```python
# ❌ La liste est partagée entre tous les appels
def log(msg, historique=[]):
    historique.append(msg)
    return historique

# ✅
def log(msg, historique=None):
    if historique is None:
        historique = []
    historique.append(msg)
    return historique
```

---

## Résumé des points clés

| Concept | Syntaxe | À retenir |
|---------|---------|----------|
| Définir | `def nom(params):` | Verbe + nom |
| Retourner | `return valeur` | Obligatoire si on veut le résultat |
| Retour multiple | `return a, b` | Déstructuré avec `a, b = f()` |
| Défaut | `def f(x, n=10):` | Jamais `[]` ou `{}` en défaut |
| Erreur saisie | `try: int(s) except ValueError:` | Capturer précisément |

---

## Exercices du module

Voir `exercices/ex_03_fonctions.py`

## Prompts IA utiles

> *« Comment gérer les erreurs de saisie utilisateur en Python avec try/except ? »*

> *« Comment retourner plusieurs valeurs depuis une fonction Python ? »*

> *« Qu'est-ce qu'une valeur par défaut dangereuse en Python ? »*
