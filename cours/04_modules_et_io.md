# Module 04 — Modules et I/O fichiers

## Concepts couverts

- `import` — bibliothèques standard
- `random` : `choice`, `randint`, `sample`, `random`, `seed`
- Lecture/écriture de fichiers : `open()`, `with`, modes `'r'`, `'w'`, `'a'`
- `pathlib.Path` pour les chemins portables
- `try/except` pour les fichiers manquants
- `json` : sérialiser/désérialiser un état de jeu
- Créer ses propres modules importables

## Lien avec le projet

```python
import random
from pathlib import Path

# Convention : colonne str 'A'..'L', ligne int 1-based
def placer_entites(nb: int, cases_libres: list, seed=None) -> list:
    """
    Choisit nb positions aléatoires uniques parmi cases_libres.
    cases_libres : liste de tuples (colonne: str, ligne: int)
    Retourne la liste des (colonne, ligne) choisis.
    """
    if seed is not None:
        random.seed(seed)
    return random.sample(cases_libres, nb)


# Écriture du log (mode 'a' = append — on ne perd pas l'historique)
def ecrire_log(message: str, chemin_log: Path) -> None:
    """Ajoute une ligne à la fin du fichier log."""
    with open(chemin_log, 'a', encoding='utf-8') as f:
        f.write(message + '\n')


# Lire les N dernières lignes avec gestion d'absence de fichier
def lire_dernieres_lignes(chemin_log: Path, n: int = 10) -> list:
    """Retourne les n dernières lignes du fichier log."""
    try:
        with open(chemin_log, 'r', encoding='utf-8') as f:
            lignes = f.readlines()
        return [l.rstrip('\n') for l in lignes[-n:]]
    except FileNotFoundError:
        return []   # fichier pas encore créé : normal au 1er tour


# Sérialiser l'état pour sauvegarde
def sauvegarder_etat(etat: dict, chemin: Path) -> None:
    import json
    with open(chemin, 'w', encoding='utf-8') as f:
        json.dump(etat, f, indent=2, ensure_ascii=False)


def charger_etat(chemin: Path) -> dict:
    import json
    try:
        with open(chemin, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
```

## Erreurs classiques

**Erreur 1 — Oublier `with` → fichier non fermé**
```python
# ❌ Si une exception survient, le fichier reste ouvert
f = open('partie.log', 'w')
f.write('Tour 1')   # si ça plante ici, le fichier n'est jamais fermé
f.close()

# ✅ with garantit la fermeture même en cas d'erreur
with open('partie.log', 'w', encoding='utf-8') as f:
    f.write('Tour 1')
```

**Erreur 2 — `FileNotFoundError` sur un fichier absent**
```python
# ❌ Plante si le fichier n'existe pas encore
with open('partie.log', 'r') as f:
    data = f.read()   # FileNotFoundError !

# ✅ Gérer l'absence explicitement
try:
    with open('partie.log', 'r', encoding='utf-8') as f:
        data = f.read()
except FileNotFoundError:
    data = ''   # log vide = début de partie
```

**Erreur 3 — Mode `'w'` efface le fichier existant**
```python
# ❌ Écrase tout l'historique à chaque tour !
with open('partie.log', 'w') as f:
    f.write(f'Tour {tour}')

# ✅ Mode 'a' (append) préserve l'historique
with open('partie.log', 'a', encoding='utf-8') as f:
    f.write(f'Tour {tour}\n')
```

**Erreur 4 — `random.sample` avec n > len(population)**
```python
# ❌ ValueError si on demande plus de cases qu'il n'y en a de libres
positions = random.sample(cases_libres, 20)  # si len(cases_libres) < 20

# ✅ Vérifier avant
assert nb <= len(cases_libres), f'Pas assez de cases libres ({len(cases_libres)} < {nb})'
positions = random.sample(cases_libres, nb)
```

## Exercice de compréhension

**Q1.** Quelle différence entre les modes `'w'` et `'a'` ?
<details><summary>Réponse</summary>

`'w'` (write) crée ou **écrase** le fichier. `'a'` (append) crée si absent, sinon **ajoute** à la fin. Pour un log de partie, toujours utiliser `'a'`.
</details>

**Q2.** Pourquoi utiliser `random.seed(42)` dans les tests ?
<details><summary>Réponse</summary>

Cela fixe le générateur aléatoire : même seed = même séquence de nombres. Les tests sont donc reproductibles et prédictibles.
</details>

**Q3.** Que se passe-t-il si on fait `json.dump(etat, f)` avec `etat` contenant un objet Python (ex. une instance de `Drone`) ?
<details><summary>Réponse</summary>

`TypeError: Object of type Drone is not JSON serializable`. JSON ne gère que les types de base : `dict`, `list`, `str`, `int`, `float`, `bool`, `None`. Il faut d'abord convertir en dict.
</details>

## Exercices du module

Voir `exercices/ex_04_io.py`

## Tips et best practices

- **Toujours utiliser `with open(...):`** — fermeture automatique même en cas d'erreur.
- **`'a'` pour les logs**, `'w'` pour réécrire, `'r'` pour lire.
- **`pathlib.Path` plutôt que les chaînes** — portable Windows/Linux/Mac :
  ```python
  from pathlib import Path
  LOG = Path('parties') / 'partie_01.log'
  LOG.parent.mkdir(exist_ok=True)  # crée le dossier si absent
  ```
- **`try/except FileNotFoundError`** sur toute lecture de fichier optionnel.
- **`random.seed()` pour les tests reproductibles**.

## Références

- [Docs Python — random](https://docs.python.org/fr/3/library/random.html)
- [Docs Python — pathlib](https://docs.python.org/fr/3/library/pathlib.html)
- [Real Python — Working With Files in Python](https://realpython.com/working-with-files-in-python/)
- [Real Python — Python import system](https://realpython.com/python-import/)

## Prompts IA

> *« Comment utiliser random.seed() pour rendre mes tests Python reproductibles ? »*

> *« Explique-moi la différence entre les modes open() en Python : r, w, a, r+, x. »*

> *« Comment utiliser pathlib en Python pour manipuler des chemins de fichiers de façon portable ? »*
