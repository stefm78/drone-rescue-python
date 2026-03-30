# ROADMAP — drone-rescue-python

> Fichier de reprise pour toute IA. Lire dans l’ordre : `README.md` → `prompt.md` → ce fichier.

---

## État final (30 mars 2026 — 10h00)

| Priorité | Tâche | Statut |
|---|---|---|
| P1 | Harmonisation convention `colonne:str` / `ligne:int` | ✅ |
| P2 | 5 notebooks Jupyter (`notebooks/nb_01`…`nb_05`) | ✅ |
| P3 | Enrichissement cours 01–08 (Erreurs classiques + QCM) | ✅ |
| P4 | `corr_05` réécrit + `corr_06/07/08` vérifiés/corrigés | ✅ |
| P5 | `GUIDE_FORMATEUR.md` | ✅ |
| P6 | `argparse` dans `jeu/main.py` + `cours/09` aligné | ✅ |

**✅ Projet complet — aucune incohérence connue.**

---

## Conventions (immuables)

```python
colonne: str   # 'A'..'L' — JAMAIS int 0-based dans cours/exercices/corrections/notebooks
ligne:   int   # 1..12 (1-based)
# Conversion interne : ord(colonne)-ord('A') → 0-based ; ligne-1 → 0-based
```

### Styles attendus

**`.md` (cours)** : `Concepts couverts` / `Lien avec le projet` / `Erreurs classiques` (3-4 blocs ❌/✅) / `Exercice de compréhension` (3 QCM `<details>`) / `Exercices du module` / `Tips` / `Références` / `Prompts IA`

**`.py` (exercices)** : en-tête `===` + convention ; sections `---` PARTIE A/B/C ; squelette `pass` ; `assert` + `print("AX OK")`

**`.py` (corrections)** : même structure ; commentaires sur les CHOIX ; `assert` identiques à l’exercice

**`.ipynb` (notebooks)** : Colab-compatible stdlib ; 8 cellules (titre→concepts→exemples→lien projet→exemple jeu→à toi→squelette→solution tag `solution`)

**`jeu/main.py`** : `parse_args()` → `appliquer_args()` patche `config` AVANT `initialiser_partie()`

---

## Prompt de reprise IA

```
Projet : drone-rescue-python (pédagogique Python débutant) — COMPLET.
Lire : README.md → prompt.md → ROADMAP.md
Convention : colonne str 'A'-'L', ligne int 1-based. Jamais int 0-based.
Aucune tâche ouverte. Si extension demandée : voir GUIDE_FORMATEUR.md §4.
Règles : pas de placeholder, pas de troncature, chaque fichier prêt à être poussé.
```

*MAJ : 30 mars 2026 09h55 CEST — P1✅ P2✅ P3✅ P4✅ P5✅ P6✅ — PROJET COMPLET*
