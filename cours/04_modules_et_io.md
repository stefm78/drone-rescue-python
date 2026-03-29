# Module 04 — Modules et I/O fichiers

## Concepts couverts

- `import` — bibliothèques standard
- `random` : `random.choice`, `random.randint`, `random.sample`, `random.random`, `random.seed`
- Lecture/écriture de fichiers : `open()`, `with`, modes `'r'`, `'w'`, `'a'`
- `pathlib.Path` pour les chemins de fichiers
- Créer ses propres modules (fichiers `.py` importables)

## Lien avec le projet

```python
import random
from pathlib import Path

# Placement aléatoire des survivants sans collision
def placer_entites(grille: list, nb: int, symbole: str, cases_libres: list) -> list:
    """
    Place nb entités aléatoirement sur des cases libres de la grille.
    Retourne la liste des positions utilisées.
    """
    positions = random.sample(cases_libres, nb)
    for (col_idx, row_idx) in positions:
        grille[row_idx][col_idx] = symbole
    return positions


# Écriture du log (mode 'a' = append — on ne perd pas l'historique)
def ecrire_log(ligne: str, chemin_log: Path) -> None:
    """Ajoute une ligne à la fin du fichier log."""
    with open(chemin_log, 'a', encoding='utf-8') as f:
        f.write(ligne + '\n')


# Lire les N dernières lignes du log
def lire_dernieres_lignes(chemin_log: Path, n: int = 10) -> list:
    """Retourne les n dernières lignes du fichier log."""
    if not chemin_log.exists():
        return []
    with open(chemin_log, 'r', encoding='utf-8') as f:
        lignes = f.readlines()
    return [l.rstrip('\n') for l in lignes[-n:]]


# Reproductibilité pour les tests
random.seed(42)  # même résultat à chaque exécution avec ce seed
```

## Exercices du module

Voir `exercices/ex_04_io.py`

## Tips et best practices

- **Toujours utiliser `with open(...):`** — fermeture automatique même en cas d'erreur.
- **`'a'` pour les logs**, `'w'` pour réécrire, `'r'` pour lire.
- **`pathlib.Path` plutôt que les chaînes** pour les chemins — portable Windows/Linux/Mac :
  ```python
  from pathlib import Path
  LOG = Path('parties') / 'partie_01.log'
  LOG.parent.mkdir(exist_ok=True)  # crée le dossier si absent
  ```
- **`random.seed()` pour les tests reproductibles** : fixe le générateur aléatoire.

## Références

- [Docs Python — random](https://docs.python.org/fr/3/library/random.html)
- [Docs Python — pathlib](https://docs.python.org/fr/3/library/pathlib.html)
- [Real Python — Working With Files in Python](https://realpython.com/working-with-files-in-python/)
- [Real Python — Python import system](https://realpython.com/python-import/)

## Prompts IA

> *« Comment utiliser random.seed() pour rendre mes tests Python reproductibles ? »*

> *« Explique-moi la différence entre les modes open() en Python : r, w, a, r+, x. »*

> *« Comment utiliser pathlib en Python pour manipuler des chemins de fichiers de façon portable ? »*
