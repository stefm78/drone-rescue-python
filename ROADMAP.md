# ROADMAP — drone-rescue-python

> Fichier de reprise pour toute IA. Lire dans l’ordre : `README.md` → `prompt.md` → ce fichier.

---

## État (30 mars 2026 — 10h00)

| Priorité | Tâche | Statut |
|---|---|---|
| P1 | Harmonisation convention `colonne:str` / `ligne:int` | ✅ |
| P2 | 5 notebooks Jupyter (`notebooks/nb_01`…`nb_05`) | ✅ |
| P3 | Enrichissement cours 01–08 (Erreurs classiques + QCM) | ✅ |
| P4 | `corr_05` réécrit + `corr_06/07/08` vérifiés/corrigés | ✅ |
| P5 | `GUIDE_FORMATEUR.md` | ✅ |
| P6 | `argparse` dans `jeu/main.py` | ❌ |

### Seule incohérence restante

| # | Fichier | Problème | Action |
|---|---|---|---|
| 1 | `jeu/main.py` | Options `--seed`, `--grille`… documentées dans `cours/09` mais non implémentées | Implémenter `argparse` (voir §P6 ci-dessous) |

---

## Conventions (immuables)

```python
colonne: str   # 'A'..'L' — JAMAIS int 0-based dans cours/exercices/corrections/notebooks
ligne:   int   # 1..12 (1-based)
# Conversion interne : ord(colonne)-ord('A') → 0-based ; ligne-1 → 0-based
```

### Styles attendus

**`.md` (cours)** : sections `Concepts couverts` / `Lien avec le projet` / `Erreurs classiques` (3-4 blocs ❌/✅) / `Exercice de compréhension` (3 QCM `<details>`) / `Exercices du module` / `Tips` / `Références` / `Prompts IA`

**`.py` (exercices)** : en-tête `===` avec module + objectifs + convention ; sections `---` PARTIE A/B/C ; squelette `pass` ; `assert` + `print("AX OK")`

**`.py` (corrections)** : même structure ; commentaires expliquant les CHOIX (pas juste le code) ; `assert` identiques à l’exercice

**`.ipynb` (notebooks)** : Colab-compatible stdlib ; 8 cellules (titre→concepts→exemples→lien projet→exemple jeu→à toi→squelette→solution tag `solution`)

---

## P6 — argparse dans jeu/main.py (dernière tâche)

Implémenter dans `jeu/main.py` :
```python
import argparse
parser = argparse.ArgumentParser(description='Drone Rescue — jeu de simulation console')
parser.add_argument('--seed',   type=int, default=None,        help='Graine aléatoire (reproductibilité)')
parser.add_argument('--grille', type=int, default=12,          help='Taille de la grille (défaut: 12)')
parser.add_argument('--drones', type=int, default=6,           help='Nombre de drones (défaut: 6)')
parser.add_argument('--log',    type=str, default='partie.log',help='Fichier de log')
args = parser.parse_args()
```
Passer `args.seed`, `args.grille`, `args.drones`, `args.log` à la fonction d’initialisation de `EtatJeu`.
Mise à jour correspondante dans `cours/09_assemblage_final.md` pour aligner la doc avec le code.

---

## Prompt de reprise IA

```
Projet : drone-rescue-python (pédagogique Python débutant).
Lire : README.md → prompt.md → ROADMAP.md
Convention : colonne str 'A'-'L', ligne int 1-based. Jamais int 0-based dans cours/exos/corr/notebooks.
Seule tâche restante :
  P6 : implémenter argparse dans jeu/main.py + aligner cours/09
Règles : pas de placeholder, pas de troncature, chaque fichier prêt à être poussé.
```

*MAJ : 30 mars 2026 09h52 CEST — P1✅ P2✅ P3✅ P4✅ P5✅ P6❌*
