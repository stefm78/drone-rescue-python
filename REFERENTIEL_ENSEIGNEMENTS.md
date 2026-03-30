# Référentiel des enseignements Python — Drone Rescue

> **Objectif de ce fichier**
> Lister tous les concepts Python qu'un apprenant débutant doit maîtriser
> pour lire, comprendre et écrire le code du jeu Drone Rescue.
> Ce référentiel sert de grille de vérification : chaque entrée correspond
> à un (ou plusieurs) module(s) de cours.
>
> **Mise à jour 2026-03-30** : refonte complète. La POO est retirée du jeu.
> `modeles.py` est supprimé. Toutes les entités sont des **dictionnaires**.
> Les règles officielles sont alignées sur `Projet_Drones_G4.pdf`.

---

## Comment utiliser ce fichier

```
- [x] Concept  — où il apparaît dans le jeu (fichier, fonction)
```

Case cochée = couvert par un module de cours.

---

## Module 1 — Fondamentaux du langage
### Cours : `01_structures_de_base.md`

### 1.1 Variables et types de base
- [x] Déclaration et affectation — `logique.py` (`batterie = 10`)
- [x] Types `int`, `float`, `str`, `bool` — `config.json` (toutes les constantes)
- [x] La valeur `None` — `logique.py` (`survivant: None` dans `creer_drone()`)
- [x] Constantes en MAJUSCULES (lecture depuis JSON) — `config.py`

### 1.2 Opérateurs
- [x] Arithmétiques (`+`, `-`, `*`, `//`, `%`) — `logique.py` (coûts batterie)
- [x] Comparaison (`==`, `!=`, `<`, `<=`, `>`, `>=`) — `logique.py` (`valider_mouvement`)
- [x] Logiques (`and`, `or`, `not`) — `logique.py` (conditions combinées)
- [x] `in` / `not in` — `logique.py` (`if cible in etat["zones_x"]`)
- [x] `max()`, `abs()` — `logique.py` (`distance_chebyshev`, `max(0, bat - cout)`)

### 1.3 Chaînes de caractères
- [x] F-strings — `affichage.py`, `logger.py` (tout le formatage)
- [x] `.strip()`, `.upper()`, `.lower()` — `console.py` (normalisation saisie)
- [x] Indexation `texte[0]`, `texte[1:]` — `logique.py` (`position_depuis_chaine`)
- [x] `len()` — `logique.py` (`if len(texte) < 2`)
- [x] `.index()` sur une liste — `logique.py` (`LETTRES.index(lettre)`)
- [x] Formatage aligné `rjust()`, `ljust()`, `:<N`, `:>N`, `:02d` — `affichage.py`

---

## Module 2 — Structures de contrôle
### Cours : `02_boucles_et_conditions.md`

### 2.1 Conditions
- [x] `if` / `elif` / `else` — `logique.py` (`valider_mouvement`, `executer_mouvement`)
- [x] Conditions imbriquées — `logique.py` (livraison + recharge simultanées)

### 2.2 Boucles
- [x] `for` sur un itérable — `logique.py` (`for drone in etat["drones"].values()`)
- [x] `for` avec `range()` — `logique.py` (initialisation de la grille)
- [x] `while` — `console.py` (`while nb_depl < MAX`)
- [x] `break` et `continue` — `console.py` (boucle de saisie)
- [x] `all()` sur un itérable — `logique.py` (`verifier_fin_partie`)

### 2.3 Gestion des erreurs
- [x] `try` / `except ValueError` — `logique.py` (`position_depuis_chaine : int(texte[1:])`)
- [x] `except FileNotFoundError` — `config.py` (lecture `config.json`)
- [ ] Bloc `finally` (concept à enseigner, peu présent dans le jeu)

---

## Module 3 — Fonctions
### Cours : `03_fonctions.md`

### 3.1 Définir et appeler
- [x] `def`, paramètres positionnels, `return` — tous les fichiers
- [x] Paramètres avec valeur par défaut — `logique.py` (`creer_drone(batterie=10)`)
- [x] Retour de plusieurs valeurs (tuple) — `logique.py` (`return False, "raison"`)
- [x] Déstructuration `ok, msg = f()` — `console.py`
- [x] Fonctions sans `return` explicite (retournent `None`) — `logger.py`

### 3.2 Robustesse
- [x] `try/except ValueError` sur saisie — `logique.py` (`position_depuis_chaine`)
- [x] Valeur par défaut mutable dangereuse : utiliser `None` comme sentinelle — cours 03
- [x] Docstrings — tous les fichiers

### 3.3 Fonctions de création (pattern dict-factory)
- [x] `creer_drone(id, col, lig)` → dict — `logique.py`
- [x] `creer_survivant(id, col, lig)` → dict — `logique.py`
- [x] `creer_tempete(id, col, lig)` → dict — `logique.py`

---

## Module 4 — Structures de données
### Cours : `01_structures_de_base.md` + `05_dictionnaires_avances.md`

### 4.1 Listes
- [x] Création, accès par index — `logique.py` (`LETTRES`, cases libres)
- [x] List comprehension simple — `logique.py` (`cases_libres = [c for c in toutes if ...]`)
- [x] List comprehension avec condition — `logique.py`
- [x] `.append()` — `affichage.py` (construction des lignes d'affichage)
- [x] `len()`, `range()` — partout
- [x] Copie pour itération sûre `list(etat["zones_x"])` — `logique.py` (`propager_zones_x`)
- [x] Grille 2D = liste de listes, `grille[lig][col]` — `logique.py`, `affichage.py`

### 4.2 Tuples
- [x] Création `(col, lig)` et déballage `col, lig = pos` — partout
- [x] Tuple comme valeur de retour — `logique.py` (`return True, ""`)
- [x] Tuple immuable : clé de set — `logique.py` (positions dans `zones_x`)
- [x] `(col, lig) == etat["hopital"]` — `logique.py`

### 4.3 Dictionnaires
- [x] Création `{"clé": valeur}` — `logique.py` (`creer_drone`)
- [x] Accès `drone["batterie"]` — partout
- [x] Modification `drone["batterie"] -= 1` — `logique.py`
- [x] `.get(cle, defaut)` — `logique.py`
- [x] `in` sur les clés — `console.py` (`if saisie in etat["drones"]`)
- [x] `.items()`, `.values()`, `.keys()` — partout
- [x] Dict de dicts `etat["drones"]["D1"]["batterie"]` — `logique.py`, `console.py`
- [x] Dict global `etat` comme paramètre unique — toutes les fonctions de `logique.py`

### 4.4 Ensembles (sets)
- [x] Création `set()` — `logique.py` (`zones_x`, positions occupées)
- [x] `.add()` — `logique.py` (`propager_zones_x`)
- [x] `.discard()` — `logique.py`
- [x] Test `in` — `logique.py` (`if cible in etat["zones_x"]`)
- [x] Itération sur copie `list(s)` — `logique.py`
- [x] Éléments immuables (tuples) obligatoires — cours 05

---

## Module 5 — Dictionnaires avancés et sets
### Cours : `05_dictionnaires_avances.md`

> La POO (classes) a été **retirée du jeu**. Le module 05 couvre les dicts
> avancés et les sets à la place. La POO est mentionnée en "pour aller plus loin".

- [x] Dict de dicts : structure `etat["drones"]["D1"]` — `logique.py`
- [x] Fonctions factory `creer_drone()` — `logique.py`
- [x] Sets de tuples pour positions — `logique.py` (`zones_x`, `occupees`)
- [x] Dict `etat` global passé en paramètre — toutes les fonctions
- [ ] POO : `class`, `__init__`, méthodes — **mention "pour aller plus loin" uniquement**

---

## Module 6 — Modules, I/O, JSON
### Cours : `04_modules_et_io.md`

### 6.1 Imports
- [x] `import random` — `logique.py` (phase météo, placement initial)
- [x] `import json` — `config.py` (`charger_config()`)
- [x] `import os` — `affichage.py` (`effacer_ecran()`)
- [x] `from module import f` — `console.py` (`from logique import valider_mouvement`)

### 6.2 Fichiers
- [x] `open()` modes `"r"`, `"w"`, `"a"` — `logger.py`, `config.py`
- [x] `with open(...) as f` — partout
- [x] `encoding="utf-8"` — `logger.py`
- [x] `json.load(f)` — `config.py`
- [x] `except FileNotFoundError` — `config.py`
- [x] `if __name__ == '__main__'` — `main.py` + conseil dans tous les modules

### 6.3 Multi-fichiers
- [x] Séparation des responsabilités : config / logique / affichage / console / logger / main
- [x] Règle de dépendance : main/console importent les autres, jamais l'inverse
- [ ] `sys.path` : **retiré du jeu**, non enseigné
- [ ] `argparse` : **retiré du jeu**, non enseigné

---

## Module 7 — Grille et affichage
### Cours : `06_grille_et_affichage.md` + `annexe_formatage.md`

- [x] Grille 2D `grille[lig][col]` — `affichage.py` (`render_grille`)
- [x] Boucles imbriquées pour construire la grille — `logique.py`
- [x] `rjust()`, `ljust()`, `:<N`, `:>N`, `:02d` — `affichage.py`
- [x] Assemblage multi-colonnes (grille | statuts | log) — `affichage.py`
- [x] Effacer l'écran `os.system('cls'/'clear')` — `affichage.py`
- [x] Distance de Chebyshev `max(|dc|, |dl|)` — `logique.py`
- [ ] Codes ANSI : **retirés du jeu**, non enseignés
- [ ] `re`, `shutil` : **retirés du jeu**, non enseignés

---

## Module 8 — Logique de jeu
### Cours : `07_logique_de_jeu.md`

- [x] Séparation validation / exécution — `logique.py` (`valider_mouvement` + `executer_mouvement`)
- [x] Règles batterie : −1 / −2 transport / −2 zone X / +3 hôpital — `logique.py`
- [x] Propagation zones X (set + copie + `random.random()`) — `logique.py`
- [x] Phase météo : 50% par tempête — `logique.py`
- [x] `all()` pour `verifier_fin_partie` — `logique.py`
- [x] Itérer sur copie `list(set)` pour éviter le RuntimeError — `logique.py`
- [x] `max(0, bat - cout)` pour éviter la batterie négative — `logique.py`

---

## Module 9 — Console, log et assemblage
### Cours : `08_console_et_log.md` + `09_assemblage_final.md`

- [x] Architecture parser → valider → exécuter — `console.py`
- [x] `input()` + `.strip().upper()` — `console.py`
- [x] `position_depuis_chaine()` : `texte[0]`, `int(texte[1:])`, `try/except` — `logique.py`
- [x] 2 joueurs : J1 (drones), J2 (tempêtes) — `console.py`
- [x] Écriture fichier `partie.log` (mode `"a"`) — `logger.py`
- [x] Écriture `resultats.txt` (mode `"w"`) — `logger.py`
- [x] `with open(..., encoding="utf-8")` — `logger.py`
- [x] Graphe de dépendances, ordre d'intégration — `09_assemblage_final.md`

---

## Bonnes pratiques transversales

- [x] Convention PEP 8 : snake_case, MAJUSCULES constantes
- [x] Commentaires et docstrings
- [x] Fonctions courtes et réutilisables (une fonction = une responsabilité)
- [x] Pas de valeurs magiques : tout dans `config.json`
- [x] DRY : fonctions factory pour éviter la duplication des dicts
- [x] `None` comme sentinelle plutôt que `0` ou `""`

---

## Récapitulatif par fichier du jeu

| Fichier | Concepts clés mis en œuvre |
|---------|----------------------------|
| `config.json` | JSON, source de vérité de toutes les constantes |
| `config.py` | `json.load()`, `FileNotFoundError`, constantes |
| `logique.py` | Fonctions factory, dicts, sets, `random`, règles officielles |
| `affichage.py` | Grille 2D, formatage, boucles, `os.system` |
| `console.py` | `input()`, boucle while, 2 joueurs, parser→valider→exécuter |
| `logger.py` | `open()` / `write()`, modes `"a"`/`"w"`, `with`, UTF-8 |
| `main.py` | `if __name__`, imports, appel `boucle_de_jeu()` |

---

*Référentiel mis à jour le 2026-03-30 suite à la refonte dicts + règles officielles.
Aligné sur `Projet_Drones_G4.pdf`.*
