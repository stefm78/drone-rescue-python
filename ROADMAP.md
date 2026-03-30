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

## 2. État actuel (30 mars 2026 — mis à jour 09h42)

### ✅ Complet

| Dossier | Fichiers | État |
|---|---|---|
| `cours/` | `00` à `09` (10 fichiers `.md`) | ✅ présents + enrichis (01-03-05) |
| `exercices/` | `ex_01` à `ex_08` (8 fichiers `.py`) | ✅ présents — ex_03 harmonisé |
| `corrections/` | `corr_01` à `corr_08` (8 fichiers `.py`) | ✅ présents — corr_03 + corr_05 réécrites |
| `jeu/` | `config.py`, `modeles.py`, `logique.py`, `affichage.py`, `console.py`, `logger.py`, `main.py` | ✅ présents |
| `notebooks/` | `nb_01` à `nb_05` (5 fichiers `.ipynb`) | ✅ créés (30 mars 2026) |

### ❌ Absent / À faire

- `cours/04`, `06`, `07`, `08` : pas encore enrichis (sections Erreurs classiques + QCM manquantes)
- `corrections/corr_06`, `corr_07`, `corr_08` : à vérifier cohérence POO avec cours 05
- `GUIDE_FORMATEUR.md` : non créé
- `argparse` dans `jeu/main.py` : documenté dans cours/09 mais non implémenté

### ✅ Incohérences corrigées

| # | Problème | Statut |
|---|---|---|
| 1 | Convention col int vs str | ✅ Corrigé — cours/01, 03, 05 + ex_03 + corr_03 + corr_05 |
| 2 | corr_05 non aligné avec cours 05 | ✅ Corrigé — réécriture complète avec EntiteGrille + @property |
| 3 | Aucun notebook .ipynb | ✅ Corrigé — notebooks/nb_01 à nb_05 créés |
| 4 | Fiches 01-03-05 trop courtes | ✅ Corrigé — Erreurs classiques + QCM ajoutés |

### ⏳ Incohérences restantes

| # | Fichier(s) | Problème | Correction |
|---|---|---|---|
| 4b | `cours/04`, `06`, `07`, `08` | Fiches sans Erreurs classiques ni QCM | Enrichir (voir §3 P3) |
| 5 | `cours/09_assemblage_final.md` | Options CLI documentées mais non implémentées dans `jeu/main.py` | Implémenter `argparse` ou retirer de la doc |
| 6 | `corr_06`, `corr_07`, `corr_08` | À vérifier cohérence convention + POO | Revoir après P3 |

---

## 3. Tâches par priorité

### ✅ PRIORITÉ 1 — Harmoniser les conventions — TERMINÉE

Convention définitive appliquée partout :
```python
colonne: str   # lettre majuscule "A" à "L"
ligne:   int   # entier 1-based, 1 à 12
# Conversion interne : ord(colonne) - ord('A')  →  index 0-based
```
Fichiers modifiés : `cours/01`, `cours/03`, `cours/05`, `exercices/ex_03`, `corrections/corr_03`, `corrections/corr_05`.

---

### ✅ PRIORITÉ 2 — Créer les notebooks Jupyter — TERMINÉE

5 notebooks créés dans `notebooks/` :

```
notebooks/
├── nb_01_structures.ipynb
├── nb_02_boucles.ipynb
├── nb_03_fonctions.ipynb
├── nb_04_modules_io.ipynb
└── nb_05_classes.ipynb
```

Compatibles Google Colab (stdlib uniquement, pas d'installation requise).

Structure de chaque notebook :
```
Cellule 1 : Markdown — titre + objectifs
Cellule 2 : Markdown — concepts expliqués
Cellule 3 : Code     — exemples exécutables
Cellule 4 : Markdown — lien avec Drone Rescue
Cellule 5 : Code     — exemple jeu exécutable
Cellule 6 : Markdown — «À toi de jouer»
Cellule 7 : Code     — squelette (pass)
Cellule 8 : Code     — solution (tag: solution)
```

---

### 🟡 PRIORITÉ 3 — Étoffer les fiches de cours — PARTIELLE

✅ Fait : `cours/01`, `cours/02`, `cours/03`, `cours/05`
⏳ Reste : `cours/04`, `cours/06`, `cours/07`, `cours/08`

**Pour chaque fichier restant, ajouter :**

1. **Section `## Erreurs classiques`** (3-4 exemples ❌/✅ avec message d'erreur Python réel)
2. **Section `## Exercice de compréhension`** (3 QCM avec `<details>` spoiler)
3. **Enrichissement `## Lien avec le projet`** (second exemple + référence fichier `jeu/`)

| Module | Fichier | Lacune principale |
|---|---|---|
| 04 | `04_modules_et_io.md` | Pas d'exemple `try/except` pour fichiers |
| 06 | `06_grille_et_affichage.md` | Manque explication codes ANSI |
| 07 | `07_logique_de_jeu.md` | Enrichir les erreurs |
| 08 | `08_console_et_log.md` | Manque section sur `re` |

---

### 🟡 PRIORITÉ 4 — Aligner corr_06 à corr_08 avec le style POO du cours 05

✅ `corr_05` réécrit (EntiteGrille + @property + convention str).
⏳ Vérifier que `corr_06`, `corr_07`, `corr_08` :
- Utilisent `colonne: str`, `ligne: int` (convention définitive)
- Réutilisent ou redéfinissent `EntiteGrille` / `Drone` / `Tempete` / `Survivant` de manière cohérente
- Ne mélangent pas les deux conventions

---

### 🟢 PRIORITÉ 5 — Ajouter un guide formateur

Créer `GUIDE_FORMATEUR.md` à la racine avec :
- Planning type semaine par semaine (détailler depuis README)
- Conseils d'animation : quand débloquer les corrections
- Grille d'évaluation des compétences apprenant
- Comment étendre le projet (nouvelles entités, nouvelles règles)
- Graphe de dépendances `jeu/` (depuis `09_assemblage_final.md`)

---

## 4. Conventions de style à respecter

Tout nouveau contenu doit respecter ces conventions, sans exception.

### Fichiers `.md` (cours)

```
# Module XX — Titre
## Concepts couverts          ← liste bullet
## Lien avec le projet        ← exemple code Python
## Erreurs classiques         ← 3-4 blocs ❌/✅
## Exercice de compréhension  ← 3 QCM avec <details>
## Exercices du module        ← renvoi vers exercices/
## Tips et best practices     ← liste bullet
## Références                 ← liens docs.python.org + realpython
## Prompts IA                 ← 3 phrases copiables
```

### Fichiers `.py` (exercices)

```python
# ============================================================
# EXERCICE XX — Titre
# Module : cours/0X_*.md
# ============================================================
# Objectifs : liste bullet
# Convention : colonne str 'A'..'L', ligne int 1-based 1..12
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
# Convention : colonne str 'A'..'L', ligne int 1-based 1..12
# ============================================================

# ----------------------------------------------------------
# CORRECTION X — Sous-thème
# ----------------------------------------------------------
# Commentaire expliquant le CHOIX (pas juste ce que fait le code)
# Code complet et fonctionnel
# Tests assert identiques à l'exercice
```

### Fichiers `.ipynb` (notebooks)

- Compatibles Google Colab (stdlib uniquement)
- Première cellule code : `# Compatible Google Colab — aucune installation requise`
- Structure 8 cellules (voir §3 P2)
- Cellule solution : metadata `{"tags": ["solution"]}`

### Convention de coordonnées (définitive)

```python
colonne: str   # lettre majuscule "A" à "L"
ligne:   int   # entier 1-based, 1 à 12

# Conversion interne :
idx_col = ord(colonne) - ord('A')  # 0 à 11
idx_lig = ligne - 1                # 0 à 11
```

---

## 5. Prompt de reprise pour une IA

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
  - Style cours       : voir ROADMAP.md §4
  - Style exercices   : voir ROADMAP.md §4
  - Style corrections : voir ROADMAP.md §4
  - Style notebooks   : voir ROADMAP.md §4
  - Compatibilité : Python 3.10+, stdlib uniquement, Google Colab pour les .ipynb

Priorités restantes :
  - PRIORITÉ 3 : enrichir cours/04, 06, 07, 08 (Erreurs classiques + QCM)
  - PRIORITÉ 4 : vérifier corr_06, corr_07, corr_08 (convention + POO)
  - PRIORITÉ 5 : créer GUIDE_FORMATEUR.md

Ne tronque rien, ne mets pas de placeholder, chaque fichier doit être
prêt à être poussé directement dans le repo GitHub.
```

---

*Dernière mise à jour : 30 mars 2026 09h42 CEST — P1 ✅ P2 ✅ P3 partielle ✅*
