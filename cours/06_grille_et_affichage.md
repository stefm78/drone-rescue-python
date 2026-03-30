# Module 06 — Grille et affichage ASCII

## Concepts couverts

- Rendu ASCII d'une grille 2D dans le terminal
- Formatage de chaînes : `ljust()`, `rjust()`, `center()`, f-strings avec spécificateurs
- Effacer l'écran : `os.system('clear')` / `os.system('cls')`
- Codes couleur ANSI : syntaxe, couleurs de base, reset
- Affichage des tableaux de bord sans cadres

## Lien avec le projet

```python
import os

COLS_LABEL = list('ABCDEFGHIJKL')

def effacer_ecran():
    os.system('cls' if os.name == 'nt' else 'clear')


def afficher_grille(grille: list) -> None:
    """
    Affiche la grille ASCII 12x12.
    grille : liste de listes de symboles str.
    Convention : grille[i_lig][i_col], i_lig = ligne-1, i_col = ord(col)-ord('A')
    """
    taille = len(grille)
    # En-tête colonnes : '      A   B   C ...'
    print('      ' + '   '.join(COLS_LABEL[:taille]))
    for i_lig in range(taille):
        label = f'{i_lig + 1:>3}  '   # numéro de ligne 1-based, aligné à droite
        cases = '   '.join(grille[i_lig])
        print(label + cases)
    print()


def afficher_tableau_drones(drones: list) -> None:
    """Affiche le tableau de bord des drones."""
    print(' ID   Pos    Bat     Surv   Blq')
    for d in drones:
        print(d.resumer())
    print()


def afficher_score(score: int, tour: int, tours_max: int,
                   surv_restants: int, nb_zones_x: int) -> None:
    print(f' Score {score}  ·  Surv. {surv_restants}  ·  Zones X {nb_zones_x}  ·  Tour {tour}/{tours_max}')
```

### Codes couleur ANSI — explication

Les codes ANSI sont des séquences d'échappement reconnues par la plupart des terminaux :

```
\033[  ← début séquence ESC
31m   ← couleur (31=rouge, 32=vert, 33=jaune, 34=bleu, 0=reset)
```

```python
class Couleur:
    ROUGE  = '\033[31m'
    VERT   = '\033[32m'
    JAUNE  = '\033[33m'
    BLEU   = '\033[34m'
    RESET  = '\033[0m'   # annule toute couleur

def colorier(texte: str, couleur: str) -> str:
    """Entoure le texte de codes ANSI."""
    return f"{couleur}{texte}{Couleur.RESET}"

# Usage dans la grille :
# '.' normal, 'X' en rouge, 'H' en vert, 'T' en jaune
def symbole_colore(sym: str) -> str:
    mapping = {
        'X': Couleur.ROUGE,
        'H': Couleur.VERT,
        'T': Couleur.JAUNE,
        'D': Couleur.BLEU,
    }
    couleur = mapping.get(sym, '')
    return colorier(sym, couleur) if couleur else sym
```

> **Note Windows** : les codes ANSI fonctionnent nativement sous Linux/macOS et
> sous Windows Terminal / PowerShell 7+. Pour les anciennes consoles Windows,
> utiliser `colorama.init()` (bibliothèque tierce).

## Erreurs classiques

**Erreur 1 — Oublier le `RESET` → tout le terminal reste coloré**
```python
# ❌ Le RESET manque : tout ce qui suit sera rouge
print(f'\033[31m{symbole}')

# ✅ Toujours terminer par RESET
print(f'\033[31m{symbole}\033[0m')
```

**Erreur 2 — Confondre index grille et coordonnées jeu**
```python
# ❌ Utilise ligne jeu directement comme index
grille[ligne][col]        # ligne=1 → accède à la 2e ligne !

# ✅ Convertir avant
i_lig = ligne - 1
i_col = ord(colonne) - ord('A')
grille[i_lig][i_col]
```

**Erreur 3 — Modifier la grille de rendu au lieu de l'état de jeu**
```python
# ❌ La grille d'affichage n'est qu'un snapshot : la modifier n'a aucun effet
grille_affichage[i][j] = 'D'

# ✅ Mettre à jour l'état (EtatJeu/Drone), puis reconstruire la grille d'affichage
drone.colonne = 'B'
drone.ligne   = 3
grille_affichage = construire_grille(etat)  # reconstruit depuis l'état
```

**Erreur 4 — `ljust`/`rjust` avec des codes ANSI (les codes comptent dans len)**
```python
# ❌ 'X' coloré en rouge = 14 caractères réels (codes inclus), ljust(3) ne fonctionne pas
print(colorier('X', Couleur.ROUGE).ljust(3))  # alignement brisé

# ✅ Appliquer la couleur APRES l'alignement
print(colorier('X'.ljust(3), Couleur.ROUGE))
```

## Exercice de compréhension

**Q1.** `\033[31m` — que signifie le `\033` ?
<details><summary>Réponse</summary>

C'est le caractère ESC (code ASCII 27) en notation octale. Il démarre une séquence d'échappement ANSI reconnue par le terminal pour changer la couleur ou le style du texte.
</details>

**Q2.** Pourquoi séparer `construire_grille()` de `afficher_grille()` ?
<details><summary>Réponse</summary>

Principe de séparation des responsabilités (MVC) : la construction calcule les symboles depuis l'état du jeu (logique), l'affichage ne fait qu'imprimer (vue). Cela permet de tester la construction sans afficher, et d'afficher n'importe quelle grille.
</details>

**Q3.** Comment afficher un nombre aligné à droite sur 3 caractères avec un f-string ?
<details><summary>Réponse</summary>

```python
print(f'{tour:>3}')   # '>3' = aligné à droite sur 3 caractères
```
</details>

## Exercices du module

Voir `exercices/ex_06_grille.py`

## Tips et best practices

- **`f'{valeur:>3}'` / `f'{valeur:<5}'`** pour aligner sans `ljust`/`rjust`.
- **Efface l'écran avant chaque affichage** pour simuler un rafraîchissement.
- **Sépare `construire_grille()` de `afficher_grille()`** : construction = logique, affichage = vue.
- **Applique la couleur ANSI après l'alignement** pour éviter les décalages.
- **Teste sur Windows ET Linux** : utilise `colorama.init()` si nécessaire.

## Références

- [Docs Python — print et formatage](https://docs.python.org/fr/3/library/functions.html#print)
- [Real Python — Python f-strings](https://realpython.com/python-f-strings/)
- [Codes couleur ANSI](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors)
- [colorama (Windows)](https://pypi.org/project/colorama/)

## Prompts IA

> *« Comment afficher du texte coloré dans un terminal Python avec les codes ANSI ? Est-ce que ça marche sur Windows ? »*

> *« Comment aligner des colonnes de texte en Python sans utiliser de bibliothèque externe ? »*

> *« Comment effacer l'écran dans un script Python pour simuler un affichage qui se rafraîchit ? »*
