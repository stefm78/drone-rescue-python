# CHANTIER — Modifications identifiées à appliquer
> Dernière mise à jour : 30 mars 2026 19h00
> Document de référence officiel : `Projet_Drones_G4.pdf`
> Branche de travail courante : `main` (toutes les PRs mergées)

---

## 🤖 Contexte de reprise — À LIRE EN PREMIER

Ce projet est un **cours Python** basé sur un jeu (sauvetage de drones). Deux niveaux :
- Le **code du jeu** dans `jeu/` (ce que les étudiants voient tourner)
- Les **modules de cours** dans `cours/`, `exercices/`, `corrections/`, `notebooks/`

Architecture : **100% dictionnaires, zéro POO, règles officielles appliquées**.
Coord. internes : `col/lig` int 0-based. Affichage : lettre (A-J) + numéro 1-based.

---

## État des phases — 30 mars 2026 19h00

| Phase | Contenu | Statut |
|-------|---------|--------|
| **1** | `config.py` + `config.json` | ✅ |
| **2** | `logique.py` — 100% dicts, sans POO | ✅ |
| **3** | Règles officielles (batterie, zones X, hôpital, météo 50%) | ✅ |
| **4** | `console.py` — 2 joueurs (J1=drones, J2=tempêtes) | ✅ |
| **5** | `affichage.py` — sans ANSI, sans `re` | ✅ |
| **6** | `logger.py` — simplifié | ✅ |
| **7** | `main.py` — sans argparse | ✅ |
| **8** | Cours, exercices, corrections, REFERENTIEL | ✅ |
| **9A/B** | Exercices + corrections 05→08 refondus | ✅ |
| **9C** | `ex_09_assemblage.py` + `corr_09_assemblage.py` | ✅ |
| **10** | `README.md` + `ROADMAP.md` | ✅ |
| **13** | Notebooks `nb_05` → `nb_08` créés | ✅ |
| **PR #6** | Fix log épinglé + synchro `nb_01`→`nb_04` 0-based | ✅ |
| **PR #7** | Fix batterie insuffisante + propagation 1 ligne + archive `prompt.md` | ✅ |
| **PR #8** | Fix `propager_zones_x` 1 ligne stricte + `valider_mouvement` coût réel + `nb_09` + docs | ✅ |

---

## Tâches restantes

### 🟡 Priorité moyenne

| # | Action | Fichier(s) |
|---|---|---|
| 1 | Audit `console.py` (7,9 Ko) | `jeu/console.py` |
| 2 | Vérifier convention 0-based sur `nb_05`→`nb_08` | `notebooks/` |

### 🟢 Priorité basse (améliorations futures)

| # | Action | Fichier(s) |
|---|---|---|
| 3 | `GUIDE_FORMATEUR.md` — sans POO, module 5 = dicts | racine |
| 4 | `tests/test_logique.py` — pytest batterie, propagation, mouvement invalide | `tests/` (nouveau) |
| 5 | `CHANGELOG.md` — historique pour les formateurs | racine |

---

## Architecture courante (stable)

```
drone-rescue-python/
├── archive/prompt.md
├── cours/00_introduction.md → 09_assemblage_final.md + annexe_formatage.md
├── exercices/ex_01 → ex_09
├── corrections/corr_01 → corr_09
├── jeu/config.json + config.py + logique.py + affichage.py
├── jeu/console.py + logger.py + main.py
└── notebooks/nb_01 → nb_09
```

---

## Conventions immuables

```python
# Coord. internes
col: int   # 0-based (0 = colonne A)
lig: int   # 0-based (0 = ligne 1)

# Affichage
# Ex: (1, 2) → B3
# Conversion : col = LETTRES.index(lettre) ; lig = num - 1
```

**Styles des fichiers :**
- `.md` (cours) : Concepts couverts / Lien projet / Erreurs classiques (3-4 blocs) / QCM `<details>` / Exercices / Tips
- `.py` (exercices) : en-tête `===` ; sections `---` PARTIE A/B/C ; squelette `pass` ; `assert` + `print("AX OK")`
- `.py` (corrections) : même structure + commentaires sur les CHOIX + `assert` identiques
- `.ipynb` (notebooks) : Colab-compatible stdlib ; 8 cellules (titre→concepts→exemples→lien projet→exemple jeu→à toi→squelette→solution)

---

*Ce fichier fait référence — ne pas modifier sans aligner avec `Projet_Drones_G4.pdf`.*
