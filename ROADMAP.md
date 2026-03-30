# ROADMAP — drone-rescue-python

> Fichier de reprise pour toute IA. Lire dans l’ordre : `README.md` → `prompt.md` → ce fichier.

---

## État (30 mars 2026 — 10h00)

| Priorité | Tâche | Statut |
|---|---|---|
| P1 | Harmonisation convention `colonne:str` / `ligne:int` | ✅ |
| P2 | 5 notebooks Jupyter (`notebooks/nb_01`…`nb_05`) | ✅ |
| P3 | Enrichissement cours 01-02-03-05 (Erreurs classiques + QCM) | ✅ |
| P3 | Enrichissement cours 04-06-07-08 | ✅ |
| P4 | `corr_05` réécrit (EntiteGrille + @property) | ✅ |
| P4 | Vérification `corr_06`, `corr_07`, `corr_08` | ⚠️ à vérifier |
| P5 | `GUIDE_FORMATEUR.md` | ❌ |
| P6 | `argparse` dans `jeu/main.py` (ou retirer de la doc cours/09) | ❌ |

### Incohérences restantes

| # | Fichier | Problème | Action |
|---|---|---|---|
| 1 | `corr_06`, `corr_07`, `corr_08` | Convention + cohérence POO à vérifier | Lire, corriger si besoin |
| 2 | `cours/07` | Code utilise encore `col: int` (0-based) dans les exemples | Harmoniser → `colonne: str` |
| 3 | `cours/08` | Code log utilise `COLS[ancien_col]` (index int) | Harmoniser → colonne directement |
| 4 | `jeu/main.py` | Options `--seed`, `--grille`… documentées dans cours/09 mais non implémentées | Implémenter `argparse` ou retirer de cours/09 |

---

## Conventions (immuables)

```python
colonne: str   # 'A'..'L' — JAMAIS int 0-based dans cours/exercices/corrections/notebooks
ligne:   int   # 1..12  (1-based)
# Conversion interne : ord(colonne)-ord('A') → 0-based ; ligne-1 → 0-based
```

### Style `.md` (cours)
```
# Module XX — Titre
## Concepts couverts  ## Lien avec le projet  ## Erreurs classiques
## Exercice de compréhension  ## Exercices du module
## Tips et best practices  ## Références  ## Prompts IA
```
### Style `.py` (exercices)
```python
# ===... EXERCICE XX — Titre / Module : cours/0X_*.md / Objectifs / Convention colonne str
# ---... PARTIE A — Sous-thème / énoncé commentaire / squelette pass / assert + print("AX OK")
```
### Style `.py` (corrections)
```python
# ===... CORRECTION XX / Convention colonne str
# ---... CORRECTION X / commentaire CHOIX / code complet / assert identiques à l’exercice
```
### Style `.ipynb` (notebooks)
- Colab-compatible (stdlib uniquement)
- Structure 8 cellules : titre→concepts→exemples→lien projet→exemple jeu→à toi→squelette→solution tagée `solution`

---

## P4 — Vérifier corr_06/07/08

Lire chaque fichier. Vérifier :
1. Convention `colonne: str`, `ligne: int` partout
2. Classes basées sur `EntiteGrille` (ou redéfinies localement de manière cohérente avec cours/05)
3. Aucun `col: int` ni `row: int` ni `'ABCDEFGHIJKL'[col]` résiduel

## P5 — GUIDE_FORMATEUR.md

Créer à la racine :
- Planning 6 semaines détaillé (depuis README)
- Quand débloquer les corrections
- Grille d’évaluation compétences (tableau)
- Comment étendre le projet
- Graphe dépendances `jeu/` (depuis cours/09)

## P6 — argparse dans jeu/main.py

Implémenter :
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--seed',   type=int, default=None)
parser.add_argument('--grille', type=int, default=12)
parser.add_argument('--drones', type=int, default=6)
parser.add_argument('--log',    type=str, default='partie.log')
args = parser.parse_args()
```
Passer `args` à la fonction d’initialisation de `EtatJeu`.

---

## Prompt de reprise IA

```
Projet : drone-rescue-python (pédagogique Python débutant).
Lire : README.md → prompt.md → ROADMAP.md
Convention : colonne str 'A'-'L', ligne int 1-based. Jamais int 0-based dans cours/exos/corr/notebooks.
Priorités restantes :
  P4 : vérifier/corriger corr_06, corr_07, corr_08 (convention + POO EntiteGrille)
  P5 : créer GUIDE_FORMATEUR.md
  P6 : implémenter argparse dans jeu/main.py
Règles : pas de placeholder, pas de troncature, chaque fichier prêt à être poussé.
```

*MAJ : 30 mars 2026 10h00 CEST — P1✅ P2✅ P3✅ P4partial⚠️ P5❌ P6❌*
