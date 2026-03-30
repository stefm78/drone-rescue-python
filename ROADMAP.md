# ROADMAP — drone-rescue-python

> Fichier de reprise pour toute IA. Lire dans l'ordre : `README.md` → `archive/prompt.md` → ce fichier.

---

## État au 30 mars 2026 — 19h00

### ✅ Phases terminées

| Phase | Description | Statut |
|-------|-------------|--------|
| 1–7 | Refonte complète du code `jeu/` (dicts, sans POO, règles officielles) | ✅ |
| 8A | `05_dictionnaires_avances.md` créé, `05_classes_et_objets.md` supprimé | ✅ |
| 8B | `01`, `03`, `04` enrichis | ✅ |
| 8C | `06`, `07`, `08` réécrits (Chebyshev, règles officielles) | ✅ |
| 8D | `annexe_formatage.md` + `09_assemblage_final.md` | ✅ |
| 8E | `REFERENTIEL_ENSEIGNEMENTS.md` mis à jour | ✅ |
| 8F | `archive/prompt.md` archivé (PR #7) | ✅ |
| 9A | Exercices `ex_05`→`ex_08` refondus | ✅ |
| 9B | Corrections `corr_05`→`corr_08` refondues | ✅ |
| 9C | `ex_09_assemblage.py` + `corr_09_assemblage.py` créés (PR #5) | ✅ |
| 10 | `README.md` + `ROADMAP.md` réécrits | ✅ |
| 13 | `nb_05` dicts, `nb_06` grille, `nb_07` logique, `nb_08` console | ✅ |
| PR #6 | Fix log épinglé + synchro `nb_01`→`nb_04` 0-based | ✅ |
| PR #7 | Fix batterie insuffisante + propagation 1 ligne + archive prompt | ✅ |
| PR #8 | `propager_zones_x` 1 ligne stricte + `valider_mouvement` coût réel + `nb_09` + docs | ✅ |

### 🟡 Tâches restantes (optionnelles)

| Priorité | Action |
|----------|--------|
| 🟡 | Audit `console.py` (7,9 Ko) — cohérence log + batterie |
| 🟡 | Vérifier `nb_05`→`nb_08` : convention 0-based |
| 🟢 | `GUIDE_FORMATEUR.md` — mise à jour (sans POO) |
| 🟢 | `tests/test_logique.py` — pytest basique |
| 🟢 | `CHANGELOG.md` — historique versions |

---

## Conventions (immuables)

```python
# Coordonnées INTERNES (code jeu) :
col: int   # 0-based (0 = colonne A)
lig: int   # 0-based (0 = ligne 1)

# Coordonnées AFFICHAGE (cours/exercices/corrections) :
col_str: str  # 'A'..'J' — lettre
lig_num: int  # 1-based
# Ex: case B3 → col=1, lig=2 en interne
# Conversion : col = LETTRES.index(lettre) ; lig = num - 1
```

### Styles attendus

**`.md` (cours)** : `Concepts couverts` / `Lien avec le projet` / `Erreurs classiques` (3-4 blocs ❌/✅) / `Exercice de compréhension` (3 QCM `<details>`) / `Exercices du module` / `Tips` / `Références` / `Prompts IA`

**`.py` (exercices)** : en-tête `===` + convention ; sections `---` PARTIE A/B/C ; squelette `pass` ; `assert` + `print("AX OK")`

**`.py` (corrections)** : même structure ; commentaires sur les CHOIX ; `assert` identiques à l'exercice

**`.ipynb` (notebooks)** : Colab-compatible stdlib ; 8 cellules (titre→concepts→exemples→lien projet→exemple jeu→à toi→squelette→solution tag `solution`)

---

## Prompt de reprise IA

```
Projet : drone-rescue-python (pédagogique Python débutant).
Lire : README.md → archive/prompt.md → ROADMAP.md
Architecture : 100% dictionnaires, ZÉRO POO, règles officielles appliquées.
Coord. internes : col/lig int 0-based. Affichage : lettre (A-J) + numéro 1-based.
Toutes les PRs (1→8) mergées. Restant (optionnel) : audit console.py, nb_05-08 0-based, GUIDE_FORMATEUR, tests, CHANGELOG.
Règles : pas de placeholder, pas de troncature, chaque fichier prêt à être poussé.
```

*MAJ : 30 mars 2026 19h00 CEST — PRs 1→8 terminées ✅ — Projet à ~95%*
