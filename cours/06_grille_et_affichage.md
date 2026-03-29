# Module 06 — Grille et affichage ASCII

## Concepts couverts

- Rendu ASCII d'une grille 2D dans le terminal
- Formatage de chaînes : `ljust()`, `rjust()`, `center()`, f-strings
- Effacer l'écran : `os.system('clear')` / `os.system('cls')`
- Codes couleur ANSI (optionnel)
- Affichage des tableaux de bord sans cadres

## Lien avec le projet

```python
import os

COLS_LABEL = list('ABCDEFGHIJKL')

def effacer_ecran():
    os.system('cls' if os.name == 'nt' else 'clear')


def afficher_grille(etat: dict) -> None:
    """
    Affiche la grille ASCII.
    etat contient 'grille', 'drones', 'tempetes', 'survivants'.
    """
    grille = etat['grille']  # liste de listes de symboles
    taille = len(grille)
    
    # En-tête colonnes
    header = '      ' + '   '.join(COLS_LABEL[:taille])
    print(header)
    
    for row_idx in range(taille):
        row_label = f'{row_idx + 1:>3}  '
        cases = '   '.join(grille[row_idx])
        print(row_label + cases)
    print()


def afficher_drones(drones: list) -> None:
    print(' ID   Pos    Bat     Surv   Blq')
    for d in drones:
        print(d.resumer())
    print()


def afficher_tempetes(tempetes: list) -> None:
    print(' ID   Pos')
    for t in tempetes:
        print(f'  {t.id:<4} {t.position_str}')
    print()


def afficher_score(score: int, tour: int, tours_max: int,
                   surv_restants: int, nb_zones_x: int) -> None:
    print(f' Score {score}  ·  Surv. rest. {surv_restants}  ·  Zones X {nb_zones_x}  ·  Tour {tour}/{tours_max}')
    print()
```

### Couleurs ANSI (optionnel)

```python
class Couleur:
    ROUGE  = '\033[31m'
RESET  = '\033[0m'
    JAUNE  = '\033[33m'
    VERT   = '\033[32m'
    BLEU   = '\033[34m'
    RESET  = '\033[0m'

def colorier(texte: str, couleur: str) -> str:
    return f"{couleur}{texte}{Couleur.RESET}"

# Exemple : zone dangereuse en rouge
print(colorier('X', Couleur.ROUGE))
```

## Exercices du module

Voir `exercices/ex_06_grille.py`

## Tips et best practices

- **`str.ljust(n)` et `str.rjust(n)`** pour aligner les colonnes du tableau de bord.
- **Efface l'écran avant chaque affichage** pour simuler un rafraîchissement.
- **Sépare `afficher_grille()` de `construire_grille()`** : la construction calcule les symboles, l'affichage ne fait qu'imprimer.
- **Teste sur Windows ET Linux** : les codes ANSI fonctionnent nativement sous Linux/Mac, nécessitent `colorama` sous Windows.

## Références

- [Docs Python — print et formatage](https://docs.python.org/fr/3/library/functions.html#print)
- [Real Python — Python f-strings](https://realpython.com/python-f-strings/)
- [Codes couleur ANSI](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors)
- [colorama (Windows)](https://pypi.org/project/colorama/)

## Prompts IA

> *« Comment afficher du texte coloré dans un terminal Python avec les codes ANSI ? Est-ce que ça marche sur Windows ? »*

> *« Comment aligner des colonnes de texte en Python sans utiliser de bibliothèque externe ? »*

> *« Comment effacer l'écran dans un script Python pour simuler un affichage qui se rafraîchit ? »*
