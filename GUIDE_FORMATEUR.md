# Guide formateur — Drone Rescue Python

> Mise à jour : 30 mars 2026 — post-PR #9

---

## Présentation du projet

Drone Rescue est un **jeu de plateau pédagogique en Python**.
Deux joueurs s'affrontent : J1 déplace des drones de secours, J2 déplace des tempêtes.
Le but de J1 est de sauver tous les survivants avant la fin du nombre de tours.

### Principes pédagogiques fondamentaux

- **Zéro POO** : toutes les entités sont des **dictionnaires** (drone, tempête, survivant, état global)
- **Fonctions fabriquantes** à la place de classes : `creer_drone()`, `creer_tempete()`, `creer_survivant()`
- **Coordonnées 0-based en interne** : `col` et `lig` sont des entiers commençant à 0
- **Notation affichage 1-based** : `A1` = `(col=0, lig=0)`, `B3` = `(col=1, lig=2)`
- Stdlib Python uniquement — compatible Google Colab sans installation

---

## Architecture du repo

```
drone-rescue-python/
├── jeu/                  Moteur du jeu (ne pas modifier sans raison)
│   ├── config.py         Paramètres officiels (TAILLE, COUT, NB_DRONES…)
│   ├── config.json       Même paramètres au format JSON
│   ├── logique.py        Règles : validation, exécution, propagation, fin de partie
│   ├── affichage.py      Rendu ASCII 3 colonnes (grille | statuts | log)
│   ├── console.py        Boucle de jeu, saisie J1/J2, architecture parser→valider→exécuter
│   ├── logger.py         Journalisation fichier (partie.log, resultats.txt)
│   └── main.py           Point d'entrée : python main.py
├── cours/                10 fichiers .md (00_introduction → 09_assemblage_final + annexe)
├── exercices/            ex_01.py → ex_09_assemblage.py  (squelettes à compléter)
├── corrections/          corr_01.py → corr_09_assemblage.py  (solutions commentées)
├── notebooks/            nb_01 → nb_09  (Jupyter/Colab, 8 cellules par notebook)
└── tests/                test_logique.py  (pytest — validation du moteur)
```

---

## Progression pédagogique recommandée

| Module | Notebook | Cours | Exercice | Concepts clés |
|--------|----------|-------|----------|---------------|
| 01 | nb_01 | 01_structures | ex_01 | listes, tuples, dicts simples |
| 02 | nb_02 | 02_boucles | ex_02 | for, while, break, continue |
| 03 | nb_03 | 03_fonctions | ex_03 | def, return, docstring |
| 04 | nb_04 | 04_modules_io | ex_04 | import, random, json, open |
| 05 | nb_05 | 05_dictionnaires_avances | ex_05 | dicts imbriqués, sets, .items() |
| 06 | nb_06 | 06_grille_affichage | ex_06 | grille ASCII, Chebyshev, ljust/rjust |
| 07 | nb_07 | 07_logique_jeu | ex_07 | validation, coûts, all() |
| 08 | nb_08 | 08_console_log | ex_08 | parser→valider→exécuter, open() |
| 09 | nb_09 | 09_assemblage_final | ex_09 | assemblage de tout le projet |

---

## Paramètres officiels du jeu

| Paramètre | Valeur | Fichier |
|-----------|--------|---------|
| Taille grille | 10×10 | `config.py` |
| Nombre de drones | 3 | `config.py` |
| Nombre de tempêtes | 2 | `config.py` |
| Batterie initiale | 10 | `config.py` |
| Batterie max | 20 | `config.py` |
| Coût déplacement normal | 1 | `config.py` |
| Coût transport survivant | 2 | `config.py` |
| Coût zone X (supplément) | 2 | `config.py` |
| Recharge hôpital | 3 | `config.py` |
| Nombre de tours max | 20 | `config.py` |
| Déplacements J1/tour | 3 | `config.py` |
| Déplacements J2/tour | 2 | `config.py` |
| Hôpital | aléatoire | `logique.py` |

---

## Convention coordonnées — point critique

C'est le point le plus source de confusion pour les apprenants :

```python
# INTERNE (code) — entiers 0-based
col: int   # 0 = colonne A,  9 = colonne J
lig: int   # 0 = ligne 1,   9 = ligne 10

# AFFICHAGE (cours, exercices, log) — lettre + numéro 1-based
# Exemples :
#   (col=0, lig=0) → 'A1'
#   (col=1, lig=2) → 'B3'
#   (col=9, lig=9) → 'J10'

# Conversion :
col = LETTRES.index(lettre)   # 'B' → 1
lig = num - 1                 # 3   → 2
```

> ⚠️ Dans les exercices et notebooks, toujours utiliser la notation affichage (`B3`).
> Le moteur gère la conversion en interne.

---

## Lancer le jeu

```bash
cd jeu
python main.py
```

### Commandes en jeu

| Saisie | Effet |
|--------|-------|
| `D1` puis `B3` | Déplace le drone D1 vers la case B3 |
| `T1` puis `E5` | Déplace la tempête T1 vers E5 |
| `next` | Passe à la phase suivante |
| `q` | Quitte la partie |

---

## Lancer les tests

```bash
pip install pytest
pytest tests/test_logique.py -v
```

Ou sans pytest (assertions directes) :

```bash
python tests/test_logique.py
```

---

## Points d'attention pour les formateurs

### ❌ À ne pas faire
- Ne pas introduire de classes (`class Drone`) — le projet est volontairement sans POO
- Ne pas utiliser `ord()`/`chr()` pour les conversions de colonnes — utiliser `LETTRES.index()` et `LETTRES[col]`
- Ne pas mélanger coordonnées 0-based et 1-based dans les exemples

### ✅ Bonnes pratiques à montrer
- Fonctions fabriquantes avec `return {…}` (pattern dict-as-object)
- `all()` / `any()` sur des générateurs dict
- `f"{LETTRES[col]}{lig + 1}"` pour l'affichage
- Architecture parser → valider → exécuter dans les boucles de saisie

### Erreurs classiques des apprenants
- Confondre `grille[lig][col]` avec `grille[col][lig]` (lignes d'abord !)
- Oublier le `+ 1` dans l'affichage ou le `- 1` dans le parsing
- Modifier un dict sans vérifier la validité du mouvement d'abord

---

## Fichiers à ne pas modifier sans raison

- `jeu/config.py` et `jeu/config.json` — les paramètres officiels sont figés
- `jeu/logique.py` — le moteur est validé par les tests
- `corrections/` — référence pour l'évaluation

*MAJ : 30 mars 2026 — PRs 1→9 mergées. Projet complet 100%.*
