# Module 06 — Grille et affichage console

> **Fil rouge :** `affichage.py` construit l'interface du jeu uniquement avec `print()` et
> du formatage de chaînes. À la fin de ce module, tu sauras afficher une grille 2D,
> aligner des colonnes et organiser un affichage multi-zones dans le terminal.

---

## 1. La grille — une liste de listes

La grille du jeu est une liste de lignes, chaque ligne étant une liste de caractères :

```python
# Grille vide 4x4 (exemple réduit)
grille = [
    ['.', '.', '.', '.'],   # ligne 0 (= ligne 1 en jeu)
    ['.', '.', '.', '.'],   # ligne 1
    ['.', '.', '.', '.'],
    ['.', '.', '.', '.'],
]

# Accès : grille[lig][col]  — attention à l'ordre !
grille[1][2] = 'D'   # drone en colonne 2, ligne 1
```

> ⚠️ L'index s'appelle `grille[lig][col]`, pas `grille[col][lig]`.
> La ligne (lig) est le premier index, la colonne (col) le second.

---

## 2. Créer une grille vide

Deux boucles `for` imbriquées permettent de créer une grille remplie de `.` :

```python
GRILLE_TAILLE = 8
grille = []
for lig in range(GRILLE_TAILLE):
    ligne = []
    for col in range(GRILLE_TAILLE):
        ligne.append('.')
    grille.append(ligne)
```

Résultat : une grille 8×8 entièrement remplie de `'.'`.

---

## 3. Afficher la grille

Le code de `affichage.py` produit un rendu comme ceci :

```
      A  B  C  D  E  F  G  H
    ------------------------
 1 |  .  .  .  .  .  .  .  .
 2 |  .  .  D  .  .  .  .  .
 3 |  .  .  .  .  T  .  .  .
```

La fonction correspondante :

```python
def render_grille(etat):
    """Retourne la grille sous forme de liste de lignes texte."""
    taille = len(etat["grille"])
    LETTRES = ["A", "B", "C", "D", "E", "F", "G", "H"]
    lignes = []

    # En-tête des colonnes
    entete = "      " + "  ".join(LETTRES[:taille])
    lignes.append(entete)
    lignes.append("    " + "---" * taille)

    # Chaque ligne de la grille
    for lig_idx in range(taille):
        num = str(lig_idx + 1).rjust(2)   # "1" -> " 1", "10" -> "10"
        cases = "  ".join(etat["grille"][lig_idx])   # ". . D . T ..."
        lignes.append(f"{num} |  {cases}")

    return lignes
```

---

## 4. Aligner les colonnes avec `rjust()` et `ljust()`

Pour des tableaux lisibles, on aligne les textes à une largeur fixe :

```python
# Aligner à droite sur N caractères
print(str(1).rjust(2))    #  1
print(str(10).rjust(2))   # 10

# Aligner à gauche sur N caractères
print("D1".ljust(4))      # "D1  "
print("D12".ljust(4))     # "D12 "
```

Dans les f-strings, même résultat avec `:>N` et `:<N` :

```python
print(f"{1:>2}")     #  1
print(f"{'D1':<4}")  # D1  
```

---

## 5. Afficher les statuts (tableau de bord)

La fonction `render_statuts(etat)` affiche les informations de chaque drone
en accédant directement aux dictionnaires :

```python
def render_statuts(etat):
    lignes = []
    lignes.append(f"{'ID':<4} {'Pos':<5} {'Bat':<9} {'Surv':<6} Blq")
    lignes.append("-" * 32)

    for drone in etat["drones"].values():
        pos = f"{LETTRES[drone['col']]}{drone['lig'] + 1}"
        bat = f"{drone['batterie']}/{drone['batterie_max']}"
        surv = drone["survivant"] if drone["survivant"] else "--"
        blq = str(drone["bloque"]) + "t" if drone["bloque"] > 0 else ""
        etat_str = "[HS]" if drone["hors_service"] else ""
        lignes.append(f"{drone['id']:<4} {pos:<5} {bat:<9} {surv:<6} {blq} {etat_str}")

    return lignes
```

Remarques :
- `drone['col']` est un entier (index) → on accède à `LETTRES[drone['col']]` pour avoir `"A"`, `"B"`...
- `drone['lig'] + 1` car les lignes sont 0-basées en interne, 1-basées pour l'affichage

---

## 6. Assembler plusieurs colonnes côte à côte

L'affichage du jeu place 3 zones horizontalement : grille | statuts | log.
Le principe : égaliser les listes, puis imprimer ligne par ligne.

```python
col1 = render_grille(etat)    # liste de str
col2 = render_statuts(etat)   # liste de str
col3 = render_log_col(etat)   # liste de str

nb_lignes = max(len(col1), len(col2), len(col3))

for i in range(nb_lignes):
    c1 = col1[i] if i < len(col1) else ""   # vide si hors limite
    c2 = col2[i] if i < len(col2) else ""
    c3 = col3[i] if i < len(col3) else ""
    print(f"{c1:<30}  |  {c2:<36}  |  {c3}")
```

La largeur fixe `:<30` assure que le séparateur `|` reste aligné quelle que soit
la longueur réelle des colonnes.

---

## 7. Effacer l'écran

Pour simuler un rafraîchissement entre chaque tour :

```python
import os

def effacer_ecran():
    """Efface le terminal (Windows et Linux/Mac)."""
    os.system('cls' if os.name == 'nt' else 'clear')
```

- `os.name == 'nt'` est vrai sur Windows → `cls`
- Sur Linux/macOS → `clear`

---

## 8. Distance de Chebyshev (#61)

Dans le jeu, un drone peut se déplacer d'une case en orthogonal ET en diagonale.
La **distance de Chebyshev** mesure exactement ça : le maximum des différences absolues
entre deux cases.

```
Formule : distance = max( |col2 - col1|, |lig2 - lig1| )
```

```python
def distance_chebyshev(col1, lig1, col2, lig2):
    """Distance en nombre de cases (1 case = 1 mouvement, diagonale incluse)."""
    return max(abs(col2 - col1), abs(lig2 - lig1))

# Exemples
print(distance_chebyshev(0, 0, 1, 1))  # 1  (diagonale = 1 mouvement)
print(distance_chebyshev(0, 0, 2, 1))  # 2  (2 cases de distance)
print(distance_chebyshev(3, 3, 3, 3))  # 0  (même case)
```

Pourquoi pas la distance euclidienne (√(dc² + dl²)) ?
Parce qu'en jeu sur grille, une diagonale coûte 1 déplacement, pas √2.
Chebyshev capture exactement cette règle.

---

## 9. Exercice A — Afficher une mini-grille

```python
# Données
grille = [
    ['.', '.', 'H', '.'],
    ['.', 'D', '.', '.'],
    ['.', '.', '.', 'S'],
    ['T', '.', '.', '.'],
]
LETTRES = ['A', 'B', 'C', 'D']

# Afficher avec numéros de lignes et lettres de colonnes
# Résultat attendu :
#       A  B  C  D
#     ------------
#  1 |  .  .  H  .
#  2 |  .  D  .  .
#  3 |  .  .  .  S
#  4 |  T  .  .  .
```

---

## 10. Exercice B — Distance de Chebyshev

```python
# Test de la fonction distance_chebyshev
print(distance_chebyshev(0, 0, 1, 0))  # 1  (déplacement ortho)
print(distance_chebyshev(0, 0, 1, 1))  # 1  (diagonale)
print(distance_chebyshev(0, 0, 2, 1))  # 2  (2 cases)
print(distance_chebyshev(3, 4, 3, 4))  # 0  (sur place)
```

---

## Erreurs classiques

**Erreur 1 — Confondre `grille[lig][col]` et `grille[col][lig]`**
```python
# ❌ Inverse les coordonnées → mauvaise case
grille[col][lig] = 'D'

# ✅ Toujours lig en premier
grille[lig][col] = 'D'
```

**Erreur 2 — Index 0-basé vs affichage 1-basé**
```python
# Le joueur voit "ligne 1" mais en Python c'est l'index 0
lig_interne = lig_affichage - 1     # 1 -> 0
lig_affichage = lig_interne + 1     # 0 -> 1
```

**Erreur 3 — Modifier la grille au lieu de l'état**
```python
# ❌ La grille est reconstruite chaque tour depuis l'état
# La modifier directement n'a aucun effet au tour suivant
grille[lig][col] = 'D'

# ✅ Modifier l'état (le dict du drone), pas la grille
etat["drones"]["D1"]["col"] = col
etat["drones"]["D1"]["lig"] = lig
# La grille est ensuite reconstruite par _mettre_a_jour_grille(etat)
```

---

## Résumé des points clés

| Concept | Exemple | À retenir |
|---------|---------|----------|
| Accès grille | `grille[lig][col]` | Lig avant col |
| Aligner à gauche | `f"{texte:<10}"` | Complète avec espaces |
| Aligner à droite | `str(n).rjust(2)` | Utile pour les numéros |
| Effacer l'écran | `os.system('cls' if os.name == 'nt' else 'clear')` | Windows/Linux |
| Distance Chebyshev | `max(abs(dc), abs(dl))` | Diagonale = 1 case |

---

## Exercices du module

Voir `exercices/ex_06_grille.py`

## Prompts IA utiles

> *« Comment afficher un tableau de bord console avec des colonnes alignées en Python ? »*

> *« Comment représenter une grille 2D en Python avec une liste de listes ? »*

> *« Comment effacer l'écran dans un script Python sur Windows et Linux ? »*
