# ROADMAP — drone-rescue-python

> Fichier de reprise pour toute IA. Lire dans l'ordre : `README.md` → `prompt.md` → ce fichier.

---

## État au 30 mars 2026 — 18h00

### ✅ Phases terminées

| Phase | Description | Statut |
|-------|-------------|--------|
| 1–7 | Refonte complète du code `jeu/` (dicts, sans POO, règles officielles) | ✅ |
| 8A | `05_dictionnaires_avances.md` créé, `05_classes_et_objets.md` supprimé | ✅ |
| 8B | `01`, `03`, `04` enrichis (list comprehension, try/except, json.load) | ✅ |
| 8C | `06`, `07`, `08` réécrits (Chebyshev, règles officielles, boucle #65) | ✅ |
| 8D | `annexe_formatage.md` + `09_assemblage_final.md` réécrits | ✅ |
| 8E | `REFERENTIEL_ENSEIGNEMENTS.md` mis à jour (sans POO) | ✅ |
| 8F | `prompt.md` réécrit | ✅ |
| 9A | Exercices `ex_05` (dicts) à `ex_08` refondus, `ex_05_classes.py` supprimé | ✅ |
| 9B | Corrections `corr_05` (dicts) à `corr_08` refondues, `corr_05_classes.py` supprimé | ✅ |
| 9C-merge | Merge `refonte/dicts-regles-officiel` → `main` (commit `d747b0d`) | ✅ |
| Audit | `AUDIT.md` créé sur `main` | ✅ |
| 10 | `README.md` + `ROADMAP.md` mis à jour | ✅ |

### 🟡 Phases restantes

| Phase | Description | Priorité |
|-------|-------------|----------|
| 13 | Créer notebooks `nb_05_dicts_avances.ipynb`, `nb_06`, `nb_07`, `nb_08` | 🟡 |
| 9C | Créer `ex_09_assemblage.py` + `corr_09_assemblage.py` | 🟡 |
| — | Supprimer `notebooks/nb_05_classes.ipynb` (POO — obsolète) | 🟡 |
| — | Mettre à jour `notebooks/nb_01` à `nb_04` (synchro cours refondus) | 🟢 |
| — | Mettre à jour `GUIDE_FORMATEUR.md` | 🟢 |

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
Lire : README.md → prompt.md → ROADMAP.md
Architecture : 100% dictionnaires, ZÉRO POO, règles officielles appliquées.
Coord. internes : col/lig int 0-based. Affichage : lettre (A-J) + numéro 1-based.
Phases 1-10 terminées. Restant : Phase 13 (notebooks nb_05 à nb_08).
Règles : pas de placeholder, pas de troncature, chaque fichier prêt à être poussé.
```

*MAJ : 30 mars 2026 18h00 CEST — Phases 1-10 ✅ — Phase 13 (notebooks) à venir*
