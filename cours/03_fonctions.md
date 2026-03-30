# Module 03 — Fonctions

## Concepts couverts

- Définir une fonction : `def`, paramètres, `return`
- Paramètres positionnels vs nommés
- Valeurs par défaut
- Portée des variables (locale vs globale)
- Docstrings
- Type hints (annotations)

## Lien avec le projet

La convention du projet pour les coordonnées :
- `colonne : str` — lettre majuscule `'A'`…`'L'`
- `ligne   : int` — entier 1-based `1`…`12`

```python
def distance_chebyshev(col1: str, lig1: int, col2: str, lig2: int) -> int:
    """
    Calcule la distance de Chebyshev entre deux positions.
    Autorise les déplacements diagonaux (diagonal = 1 pas).

    Args:
        col1, col2 : colonnes str 'A'-'L'
        lig1, lig2 : lignes int 1-12

    Returns:
        Distance entière >= 0
    """
    dc = abs(ord(col1) - ord(col2))   # différence entre colonnes
    dl = abs(lig1 - lig2)             # différence entre lignes
    return max(dc, dl)


def coord_valide(colonne: str, ligne: int, taille: int = 12) -> bool:
    """Vérifie qu'une coordonnée est dans les limites de la grille."""
    cols_valides = [chr(ord('A') + i) for i in range(taille)]
    return colonne in cols_valides and 1 <= ligne <= taille


def resumer_drone(drone: dict) -> str:
    """Retourne une ligne de résumé formatée pour le tableau de bord."""
    surv = drone['survivant'] if drone['survivant'] else '—'
    if drone['batterie'] == 0:
        blq = 'HS'
    elif drone['bloque'] > 0:
        blq = f"{drone['bloque']}t"
    else:
        blq = '—'
    return (
        f"  {drone['id']:<4} {drone['colonne']}{drone['ligne']:<3} "
        f"{drone['batterie']:>2}/{drone['batterie_max']:<2}   {surv:<5}  {blq}"
    )
```

## Erreurs classiques

**Erreur 1 — Oublier `return` (la fonction retourne `None` silencieusement)**
```python
# ❌ Pas de return → retourne None
def distance_chebyshev(col1, lig1, col2, lig2):
    dc = abs(ord(col1) - ord(col2))
    dl = abs(lig1 - lig2)
    max(dc, dl)   # ← résultat calculé mais jamais retourné !

d = distance_chebyshev('A', 1, 'B', 2)
print(d)  # None  ← piège classique

# ✅
def distance_chebyshev(col1, lig1, col2, lig2):
    return max(abs(ord(col1) - ord(col2)), abs(lig1 - lig2))
```

**Erreur 2 — Mutable comme valeur par défaut**
```python
# ❌ La liste par défaut est partagée entre tous les appels !
def ajouter_log(msg, historique=[]):
    historique.append(msg)
    return historique

# ✅ Utiliser None comme sentinelle
def ajouter_log(msg, historique=None):
    if historique is None:
        historique = []
    historique.append(msg)
    return historique
```

**Erreur 3 — `TypeError` : mauvais type passé en argument**
```python
# La fonction attend une str colonne et un int ligne
distance_chebyshev(0, 0, 1, 1)   # ❌ TypeError : ord() attend str, pas int
distance_chebyshev('A', 1, 'B', 2)  # ✅
```

## Exercice de compréhension

**Q1.** Pourquoi `taille=12` dans la signature de `coord_valide` est-il utile ?
<details><summary>Réponse</summary>

Cela permet d'utiliser la fonction avec n'importe quelle taille de grille sans changer le code. Par défaut, elle s'applique à la grille 12×12 du jeu.
</details>

**Q2.** Qu'est-ce qu'une docstring et à quoi sert-elle ?
<details><summary>Réponse</summary>

C'est une chaîne de texte placée juste après `def` entre `"""`. Elle documente ce que fait la fonction. On peut la lire avec `help(ma_fonction)` ou dans un IDE.
</details>

**Q3.** Que retourne `distance_chebyshev('A', 1, 'A', 1)` ?
<details><summary>Réponse</summary>

`0` — même case, différences nulles, `max(0, 0) = 0`.
</details>

## Exercices du module

Voir `exercices/ex_03_fonctions.py`

## Tips et best practices

- **Une fonction = une responsabilité** : si ta fonction fait plus d'une chose, découpe-la.
- **Toujours écrire une docstring** pour les fonctions non triviales.
- **Utilise les type hints** : ils documentent le code et aident les IDE.
- **Nomme avec verbe + nom** : `calculer_distance`, `valider_mouvement`, `afficher_grille`.
- **Évite les variables globales** : passe les données en paramètre.
- **Ne jamais utiliser un mutable comme valeur par défaut** : utilise `None` comme sentinelle.

## Références

- [Docs Python — Définir des fonctions](https://docs.python.org/fr/3/tutorial/controlflow.html#defining-functions)
- [PEP 257 — Docstrings](https://peps.python.org/pep-0257/)
- [PEP 484 — Type Hints](https://peps.python.org/pep-0484/)
- [Real Python — Python Type Checking](https://realpython.com/python-type-checking/)

## Prompts IA

> *« Explique-moi le principe de responsabilité unique appliqué aux fonctions Python, avec un exemple de jeu. »*

> *« Qu'est-ce que la portée des variables en Python ? Pourquoi faut-il éviter les variables globales ? »*

> *« Comment écrire une bonne docstring Python ? Montre-moi le format Google et le format NumPy. »*
