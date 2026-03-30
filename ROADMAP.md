# ROADMAP — Complétion du cours drone-rescue-python

> **Ce fichier est destiné à toute IA reprenant le projet.**
> Il décrit l'état actuel du repo, les incohérences à corriger, et les tâches
> à réaliser dans l'ordre de priorité. Respecte scrupuleusement les conventions
> et le style décrits ci-dessous.

---

## 1. Contexte du projet

Projet pédagogique Python pour **débutant** (6 semaines).
Fil rouge : construire un jeu de simulation de sauvetage par drones en console.

- Repo : `https://github.com/stefm78/drone-rescue-python`
- Prompt de reprise complet : voir `prompt.md` à la racine
- Règles du jeu, structure et interface console : voir `README.md` et `prompt.md`

---

## 2. État actuel (30 mars 2026)

### ✅ Complet

| Dossier | Fichiers | État |
|---|---|---|
| `cours/` | `00` à `09` (10 fichiers `.md`) | ✅ présents |
| `exercices/` | `ex_01` à `ex_08` (8 fichiers `.py`) | ✅ présents |
| `corrections/` | `corr_01` à `corr_08` (8 fichiers `.py`) | ✅ présents |
| `jeu/` | `config.py`, `modeles.py`, `logique.py`, `affichage.py`, `console.py`, `logger.py`, `main.py` | ✅ présents |

### ❌ Absent

- Aucun notebook Jupyter (`.ipynb`) — prévu dans le `prompt.md`
- Pas de dossier `notebooks/`

### ⚠️ Incohérences à corriger

Voir section 4 ci-dessous.

---

## 3. Tâches par priorité

### 🔴 PRIORITÉ 1 — Harmoniser les conventions (avant tout le reste)

**Problème :** deux conventions de représentation des colonnes coexistent dans le repo :

| Convention | Fichiers concernés | Exemple |
|---|---|---|
| **Index entier 0-based** | `cours/01` à `05`, `jeu/modeles.py`, `jeu/logique.py` | `col=0` pour colonne A |
| **Lettre str** | `exercices/ex_05` à `ex_08`, `corrections/corr_05` à `corr_08` | `colonne="A"` |

**Décision à prendre (une seule, à tenir dans tout le repo) :**
La convention **lettre str** (ex. `"A"`) est plus lisible pour un débutant et plus
proche de l'interface console. **Elle doit devenir la convention unique.**

**Fichiers à mettre à jour :**
- `cours/01_structures_de_base.md` — remplacer `col: int (0-based)` par `colonne: str`
- `cours/05_classes_et_objets.md` — remplacer `col: int` / `'ABCDEFGHIJKL'[col]` par `colonne: str`
- `exercices/ex_03_fonctions.py` — les fonctions `distance_chebyshev`, `est_dans_grille`, `valider_mouvement_drone` utilisent des `int` → les réécrire avec lettres et conversion interne via `ord()`
- `corrections/corr_03_fonctions.py` — aligner sur le nouvel ex_03
- `jeu/modeles.py` — vérifier que toutes les classes utilisent `colonne: str`
- `jeu/logique.py` — vérifier les fonctions de déplacement

**Convention finale à utiliser partout :**
```python
# Bonne convention (lettre str)
colonne = "A"  # str, une lettre majuscule A-L
ligne   = 1    # int, 1-based (1 à 12)

# Conversion interne quand nécessaire
idx_col = ord(colonne) - ord('A')  # 0 à 11
idx_lig = ligne - 1                # 0 à 11
```

---

### 🔴 PRIORITÉ 2 — Créer les notebooks Jupyter

**Pourquoi :** le `prompt.md` spécifie explicitement « fiches, notebooks Jupyter ET exercices
interactifs ». Les notebooks sont indispensables pour les débutants qui veulent exécuter
le code cellule par cellule sans configurer un environnement complet.

**Créer le dossier `notebooks/` avec 5 fichiers `.ipynb` :**

```
notebooks/
├── nb_01_structures.ipynb
├── nb_02_boucles.ipynb
├── nb_03_fonctions.ipynb
├── nb_04_modules_io.ipynb
└── nb_05_classes.ipynb
```

**Structure type pour chaque notebook (à respecter) :**

```
Cellule 1 : Markdown — titre + objectifs du module
Cellule 2 : Markdown — concept expliqué (copié/adapté du cours .md)
Cellule 3 : Code     — exemple minimal exécutable
Cellule 4 : Markdown — lien avec Drone Rescue
Cellule 5 : Code     — exemple tiré du jeu (exécutable)
Cellule 6 : Markdown — «  À toi de jouer » (mini-exercice inline)
Cellule 7 : Code     — squelette de l'exercice (avec `pass` ou `...`)
Cellule 8 : Code     — solution masquée (cellule tagged `solution`)
```

**Compatibilité cible :** Google Colab (pas d'import externe, stdlib uniquement).
Ajouter en première cellule de chaque notebook :
```python
# Compatible Google Colab — aucune installation requise
```

---

### 🟡 PRIORITÉ 3 — Étoffer les fiches de cours

Les fiches actuelles font entre 1 900 et 4 700 octets.
Pour être vraiment utiles à un débutant autonome,
elles devraient au minimum **doubler de volume**.

**Pour chaque fichier `cours/0X_*.md`, ajouter :**

1. **Section `## Erreurs classiques`** (2 à 4 exemples)
   - Montrer le code faux + le message d'erreur Python exact
   - Montrer la correction
   - Exemple pour module 01 :
     ```python
     # ❌ Erreur fréquente — modifier une liste pendant une boucle for
     drones = ["D1", "D2", "D3"]
     for d in drones:
         if d == "D2":
             drones.remove(d)  # → comportement inattendu

     # ✅ Correct — itérer sur une copie
     for d in drones[:]:
         if d == "D2":
             drones.remove(d)
     ```

2. **Section `## Exercice de compréhension` (QCM ou vrai/faux)**
   - 3 questions à choix multiple directement dans le Markdown
   - Réponses en spoiler `<details><summary>Réponse</summary>...</details>`

3. **Enrichissement de la section `## Lien avec le projet`**
   - Ajouter un second exemple de code (plus complexe que l'actuel)
   - Montrer comment le concept est utilisé dans `jeu/` (référence au fichier exact)

**Modules à enrichir par ordre de priorité :**

| Module | Fichier | Lacune principale |
|---|---|---|
| 01 | `01_structures_de_base.md` | Erreurs classiques absentes |
| 02 | `02_boucles_et_conditions.md` | Exemple jeu trop simple |
| 03 | `03_fonctions.md` | Pas de section sur les erreurs TypeError/ValueError |
| 04 | `04_modules_et_io.md` | Pas d'exemple de `try/except` pour les fichiers |
| 05 | `05_classes_et_objets.md` | @property présent en cours mais absent des exercices |
| 06 | `06_grille_et_affichage.md` | Manque explication des codes ANSI |
| 07 | `07_logique_de_jeu.md` | Le plus complet — juste enrichir les erreurs |
| 08 | `08_console_et_log.md` | Manque section sur `re` (expressions régulières) |

---

### 🟡 PRIORITÉ 4 — Aligner corr_05 à corr_08 avec le style POO du cours 05

**Problème :** `corrections/corr_05_classes.py` définit des classes `Position`, `Drone`,
`Entite`, `Tempete` avec une convention lettre-str — mais `cours/05_classes_et_objets.md`
définit une hiérarchie `EntiteGrille` → `Drone` / `Tempete` / `Survivant` avec `@property`.
Un étudiant qui compare les deux sera déconcerté.

**Ce qu'il faut faire :**
- Après avoir appliqué la PRIORITÉ 1 (convention lettre-str),
  réécrire `corr_05_classes.py` pour utiliser `EntiteGrille` comme classe de base
  (exactement comme dans le cours), ajouter `@property est_hs` et `@property est_bloque`
  sur `Drone`.
- Vérifier que `corr_06`, `corr_07`, `corr_08` importent ou réutilisent ces classes
  harmonisées (ou redéfinissent localement de manière cohérente).

---

### 🟢 PRIORITÉ 5 — Ajouter un guide formateur

Créer `GUIDE_FORMATEUR.md` à la racine avec :
- Planning type semaine par semaine (déjà dans README, à détailler)
- Conseils d'animation : quand débloquer les corrections
- Comment évaluer l'apprenant (grille de compétences)
- Comment étendre le projet (nouvelles entités, nouvelles règles)
- Dépendances entre fichiers `jeu/` (reprendre le graphe de `09_assemblage_final.md`)

---

## 4. Récapitulatif des incohérences connues

| # | Fichier(s) | Problème | Correction |
|---|---|---|---|
| 1 | `cours/01`, `cours/05`, `ex_03`, `corr_03`, `jeu/modeles.py` | Convention col int vs str | Uniformiser sur str lettre (voir §3 P1) |
| 2 | `corr_05_classes.py` | Classes non alignées avec cours 05 | Réécrire avec `EntiteGrille` + `@property` |
| 3 | Tout le repo | Aucun notebook `.ipynb` | Créer `notebooks/` (voir §3 P2) |
| 4 | `cours/01` à `08` | Fiches trop courtes, pas d'erreurs classiques | Enrichir chaque fiche (voir §3 P3) |
| 5 | `cours/09_assemblage_final.md` | Options CLI (`--seed`, `--grille`, etc.) documentées mais non implémentées dans `jeu/main.py` | Soit implémenter `argparse` dans `main.py`, soit retirer de la doc |

---

## 5. Conventions de style à respecter

Tout nouveau contenu doit respecter ces conventions, sans exception.

### Fichiers `.md` (cours)

```
# Module XX — Titre
## Concepts couverts       ← liste bullet
## Lien avec le projet     ← exemple code Python
## Erreurs classiques      ← À AJOUTER (voir §3 P3)
## Exercice de compréhension ← À AJOUTER (voir §3 P3)
## Exercices du module     ← renvoi vers exercices/
## Tips et best practices  ← liste bullet
## Références              ← liens docs.python.org + realpython
## Prompts IA              ← 3 phrases copiables
```

### Fichiers `.py` (exercices)

```python
# ============================================================
# EXERCICE XX — Titre
# Module : cours/0X_*.md
# ============================================================
# Objectifs : liste bullet
# ============================================================

# ----------------------------------------------------------
# PARTIE A — Sous-thème
# ----------------------------------------------------------
# Énoncé détaillé en commentaire
# Squelette de fonction avec pass
# Tests assert + print("AX OK") à la fin
```

### Fichiers `.py` (corrections)

```python
# ============================================================
# CORRECTION XX — Titre
# ============================================================

# ----------------------------------------------------------
# CORRECTION X — Sous-thème
# ----------------------------------------------------------
# Commentaire expliquant le CHOIX (pas juste ce que fait le code)
# Code complet et fonctionnel
# Tests assert identiques à l'exercice
```

### Convention de coordonnées (définitive)

```python
colonne: str   # lettre majuscule "A" à "L"
ligne:   int   # entier 1-based, 1 à 12

# Conversion interne :
idx_col = ord(colonne) - ord('A')  # 0 à 11
idx_lig = ligne - 1                # 0 à 11
```

---

## 6. Prompt de reprise pour une IA

Colle ce bloc dans n'importe quelle IA pour reprendre le projet :

```
Tu reprends le projet pédagogique Python `drone-rescue-python`.
Lis d'abord ces fichiers dans l'ordre :
  1. README.md            — objectif, règles du jeu, structure
  2. prompt.md            — spécification complète originale
  3. ROADMAP.md           — état actuel + tâches priorisées

Conventions obligatoires :
  - Colonnes : str lettre "A"-"L" (jamais int 0-based)
  - Lignes   : int 1-based (1 à 12)
  - Style cours    : voir ROADMAP.md §5
  - Style exercices: voir ROADMAP.md §5
  - Style corrections: voir ROADMAP.md §5
  - Compatibilité : Python 3.10+, stdlib uniquement, Google Colab pour les .ipynb

Commence par la tâche de PRIORITÉ 1 (harmonisation des conventions),
puis PRIORITÉ 2 (notebooks), puis PRIORITÉ 3 (enrichissement des cours).
Ne tronque rien, ne mets pas de placeholder, chaque fichier doit être
prêt à être poussé directement dans le repo GitHub.
```

---

*Dernière mise à jour : 30 mars 2026 — généré après audit complet du repo.*
