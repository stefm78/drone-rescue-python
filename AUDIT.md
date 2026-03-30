# AUDIT DU REPO — drone-rescue-python

> Audit réalisé le 30 mars 2026 après le merge de la branche `refonte/dicts-regles-officiel`.

---

## Vue d'ensemble

```
drone-rescue-python/
├── .gitignore
├── README.md
├── REFERENTIEL_ENSEIGNEMENTS.md
├── ROADMAP.md
├── CHANTIER_CODE.md
├── GUIDE_FORMATEUR.md
├── prompt.md
├── cours/           (11 fichiers .md)
├── exercices/       (8 fichiers .py)
├── corrections/     (8 fichiers .py)
├── jeu/             (7 fichiers .py + .json)
└── notebooks/       (5 fichiers .ipynb)
```

---

## 1. Racine du repo

| Fichier | Verdict | Motif |
|---|---|---|
| `.gitignore` | ✅ **Conserver** | Standard, rien à changer |
| `README.md` | ⚠️ **Mettre à jour** | Mentionne encore les classes et l'ancienne structure (taille 2782 o) |
| `REFERENTIEL_ENSEIGNEMENTS.md` | ✅ **Conserver** | Refondu en Phase 8E — à jour |
| `prompt.md` | ✅ **Conserver** | Refondu en Phase 8F — à jour |
| `ROADMAP.md` | ⚠️ **Mettre à jour** | Étape POO encore visible, phases 1–8 à cocher comme terminées |
| `CHANTIER_CODE.md` | ⚠️ **Mettre à jour** | Concu pendant la refonte, certains blocs font encore référence aux classes |
| `GUIDE_FORMATEUR.md` | ⚠️ **Mettre à jour** | Créé avant la refonte ; progression pédagogique à aligner sur dicts/règles officielles |
| `AUDIT.md` | ✅ **Conserver** | Ce fichier — créé à l'issue de l'audit |

---

## 2. Dossier `cours/`

| Fichier | Verdict | Motif |
|---|---|---|
| `00_introduction.md` | ⚠️ **Mettre à jour** | Mentionne probablement l'ancienne architecture (classes au module 5) ; à vérifier |
| `01_structures_de_base.md` | ✅ **Conserver** | Refondu en Phase 8B |
| `02_boucles_et_conditions.md` | ✅ **Conserver** | Refondu en Phase 8B |
| `03_fonctions.md` | ✅ **Conserver** | Refondu en Phase 8B |
| `04_modules_et_io.md` | ✅ **Conserver** | Refondu en Phase 8B |
| `05_dictionnaires_avances.md` | ✅ **Conserver** | Créé en Phase 8A — module central de la refonte |
| `06_grille_et_affichage.md` | ✅ **Conserver** | Refondu en Phase 8C |
| `07_logique_de_jeu.md` | ✅ **Conserver** | Refondu en Phase 8C |
| `08_console_et_log.md` | ✅ **Conserver** | Refondu en Phase 8C |
| `09_assemblage_final.md` | ⚠️ **Mettre à jour** | Créé avant la refonte ; les exemples d'assemblage font référence à des classes et à des coordonnées lettre+chiffre |
| `annexe_formatage.md` | ✅ **Conserver** | Refondu en Phase 8D |

---

## 3. Dossier `exercices/`

| Fichier | Verdict | Motif |
|---|---|---|
| `ex_01_structures.py` | ✅ **Conserver** | Conforme — structures de base sans POO |
| `ex_02_boucles.py` | ✅ **Conserver** | Conforme |
| `ex_03_fonctions.py` | ✅ **Conserver** | Conforme |
| `ex_04_io.py` | ✅ **Conserver** | Conforme |
| `ex_05_dicts_avances.py` | ✅ **Conserver** | Créé en Phase 9A — remplace l'ancien `ex_05_classes.py` |
| `ex_06_grille.py` | ✅ **Conserver** | Refondu en Phase 9A — coordonnées entières, sans ANSI |
| `ex_07_logique.py` | ✅ **Conserver** | Refondu en Phase 9A — tout en dicts, règles officielles |
| `ex_08_console.py` | ✅ **Conserver** | Refondu en Phase 9A — sans `re` ni `class Logger` |

> **Manquant :** `ex_09_assemblage.py` — à créer en Phase 10 pour couvrir le module 09.

---

## 4. Dossier `corrections/`

| Fichier | Verdict | Motif |
|---|---|---|
| `corr_01_structures.py` | ✅ **Conserver** | Conforme |
| `corr_02_boucles.py` | ✅ **Conserver** | Conforme |
| `corr_03_fonctions.py` | ✅ **Conserver** | Conforme |
| `corr_04_io.py` | ✅ **Conserver** | Conforme |
| `corr_05_dicts_avances.py` | ✅ **Conserver** | Créé en Phase 9B — avec `assert` exécutables |
| `corr_06_grille.py` | ✅ **Conserver** | Refondu en Phase 9B |
| `corr_07_logique.py` | ✅ **Conserver** | Refondu en Phase 9B |
| `corr_08_console.py` | ✅ **Conserver** | Refondu en Phase 9B |

> **Manquant :** `corr_09_assemblage.py` — à créer en Phase 10.

---

## 5. Dossier `jeu/`

Le code source du jeu jouable. Créé avant la refonte.

| Fichier | Verdict | Motif |
|---|---|---|
| `main.py` | ⚠️ **Mettre à jour** | Point d'entrée ; à vérifier cohérence avec la nouvelle architecture dicts |
| `config.py` | ⚠️ **Mettre à jour** | Constantes de configuration ; coordonnées et structures probablement en ancien format |
| `config.json` | ⚠️ **Mettre à jour** | Idem — format des positions à aligner sur (col, lig) entiers 0-basés |
| `logique.py` | ⚠️ **Mettre à jour** | Fichier le plus lourd (20 Ko) — très probablement encore basé sur des classes |
| `affichage.py` | ⚠️ **Mettre à jour** | Utilise très certainement les codes ANSI et les coordonnées lettre+chiffre |
| `console.py` | ⚠️ **Mettre à jour** | Probablement `import re` + `class Logger` — à aligner sur le nouveau modèle |
| `logger.py` | ⚠️ **Mettre à jour** | Implante le logger en classe — à remplacer par les fonctions de `corr_08_console.py` |

> ⚠️ **Le dossier `jeu/` est l'héritier direct de l'ancienne architecture POO. C'est la zone de travail prioritaire de la Phase 10.**

---

## 6. Dossier `notebooks/`

Notebooks Jupyter/Colab pour les apprenants.

| Fichier | Verdict | Motif |
|---|---|---|
| `nb_01_structures.ipynb` | ⚠️ **Mettre à jour** | Contenu à aligner sur le cours refondu (01) |
| `nb_02_boucles.ipynb` | ⚠️ **Mettre à jour** | Idem (02) |
| `nb_03_fonctions.ipynb` | ⚠️ **Mettre à jour** | Idem (03) |
| `nb_04_modules_io.ipynb` | ⚠️ **Mettre à jour** | Idem (04) |
| `nb_05_classes.ipynb` | ❌ **Supprimer** | Nom et contenu basés sur la POO supprimée ; **à remplacer par** `nb_05_dicts_avances.ipynb` |

> **Manquants :** `nb_05_dicts_avances.ipynb`, `nb_06_grille.ipynb`, `nb_07_logique.ipynb`, `nb_08_console.ipynb`

---

## Synthèse des actions

### ❌ À supprimer (1 fichier)

| Fichier | Raison |
|---|---|
| `notebooks/nb_05_classes.ipynb` | POO supprimée du référentiel |

### ⚠️ À mettre à jour (priorités)

| Priorité | Fichier(s) | Travail à faire |
|---|---|---|
| 🔴 1 | `jeu/logique.py` | Refonte complète : classes → dicts, règles officielles |
| 🔴 2 | `jeu/affichage.py` | ANSI → texte brut, coordonnées lettre+chiffre → entiers |
| 🔴 3 | `jeu/console.py` | Aligner sur `corr_08_console.py` (sans `re`, sans `class Logger`) |
| 🔴 4 | `jeu/logger.py` | Remplacer par les fonctions `demarrer_log` / `enregistrer_log` |
| 🔴 5 | `jeu/config.py` + `config.json` | Coordonnées (col, lig) entiers 0-basés |
| 🟡 6 | `README.md` | Architecture, modules 01-08 + règles officielles |
| 🟡 7 | `ROADMAP.md` | Cocher phases 1-9 terminées, ajouter Phase 10 (jeu) et Phase 11 (notebooks) |
| 🟡 8 | `CHANTIER_CODE.md` | Retirer les blocs devenus obsolètes |
| 🟡 9 | `GUIDE_FORMATEUR.md` | Progression pédagogique à aligner (module 5 = dicts, pas classes) |
| 🟡 10 | `cours/00_introduction.md` | Retirer la mention « module 5 = classes » |
| 🟡 11 | `cours/09_assemblage_final.md` | Exemples à relier aux dicts et aux nouvelles fonctions |
| 🟡 12 | `notebooks/nb_01` à `nb_04` | Synchronisation avec les cours refondus |

### 🟢 À créer (manquants)

| Fichier | Contenu |
|---|---|
| `exercices/ex_09_assemblage.py` | Exercice final d'intégration (module 09) |
| `corrections/corr_09_assemblage.py` | Correction avec `assert` |
| `notebooks/nb_05_dicts_avances.ipynb` | Remplace `nb_05_classes.ipynb` |
| `notebooks/nb_06_grille.ipynb` | Nouveau |
| `notebooks/nb_07_logique.ipynb` | Nouveau |
| `notebooks/nb_08_console.ipynb` | Nouveau |

---

## Phases restantes proposées

| Phase | Périmètre | Priorité |
|---|---|---|
| **Phase 10** | Refonte `jeu/` (logique, affichage, console, logger, config) | 🔴 Haute |
| **Phase 11** | Mise à jour + création notebooks (nb_01 à nb_08) | 🟡 Moyenne |
| **Phase 12** | ex_09 + corr_09 + cours/09 revu | 🟡 Moyenne |
| **Phase 13** | Mise à jour README, ROADMAP, GUIDE_FORMATEUR, CHANTIER_CODE | 🟢 Basse |

---

*Audit généré automatiquement — à relire et valider par le mainteneur.*
