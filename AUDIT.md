# AUDIT DU REPO — drone-rescue-python

> Audit mis à jour le 30 mars 2026 après le merge de PR #8.
> État référence : commit `a5d2f87` (PR #6) + PR #7 + PR #8 (en cours).

---

## Vue d'ensemble du repo

```
drone-rescue-python/
├── .gitignore
├── README.md                          ✅ à jour (Phase 10)
├── REFERENTIEL_ENSEIGNEMENTS.md       ✅ à jour (Phase 8E)
├── ROADMAP.md                         ✅ synchronisé (ce commit)
├── CHANTIER_CODE.md                   ✅ synchronisé (ce commit)
├── GUIDE_FORMATEUR.md                 ⚠️ à mettre à jour (sans POO)
├── AUDIT.md                           ✅ ce fichier
├── archive/
│   └── prompt.md                      ✅ archivé (PR #7)
├── cours/                             10 fichiers .md + annexe ✅
├── exercices/                         9 fichiers .py ex_01→ex_09 ✅
├── corrections/                       9 fichiers .py corr_01→corr_09 ✅
├── jeu/                               7 fichiers Python (moteur) ✅
└── notebooks/                         9 fichiers .ipynb nb_01→nb_09 ✅
```

---

## 1. Racine du repo

| Fichier | Verdict | Motif |
|---|---|---|
| `.gitignore` | ✅ **Conserver** | Standard |
| `README.md` | ✅ **Conforme** | Refondu Phase 10 |
| `REFERENTIEL_ENSEIGNEMENTS.md` | ✅ **Conforme** | Refondu Phase 8E |
| `ROADMAP.md` | ✅ **Conforme** | Synchronisé ce commit |
| `CHANTIER_CODE.md` | ✅ **Conforme** | Synchronisé ce commit |
| `GUIDE_FORMATEUR.md` | ⚠️ **À mettre à jour** | Créé avant la refonte — progression à aligner sur dicts (sans POO) |
| `archive/prompt.md` | ✅ **Archivé** | Déplacé hors racine (PR #7) |

---

## 2. Dossier `cours/`

Tous les fichiers cours sont conformes et à jour.

| Fichier | Verdict |
|---|---|
| `00_introduction.md` → `09_assemblage_final.md` | ✅ **Conformes** |
| `annexe_formatage.md` | ✅ **Conforme** |

---

## 3. Dossiers `exercices/` & `corrections/`

Séries complètes et symétriques ex_01→ex_09 / corr_01→corr_09.

| Fichier | Verdict |
|---|---|
| `ex_01` → `ex_09` | ✅ **Conformes** — 100% dicts, sans POO, `assert` exécutables |
| `corr_01` → `corr_09` | ✅ **Conformes** — solutions complètes + `assert` |

---

## 4. Dossier `jeu/`

| Fichier | Verdict | Motif |
|---|---|---|
| `logique.py` | ✅ **Conforme** | 100% dicts, règles officielles, zones X fixées (PR #6+8) |
| `affichage.py` | ✅ **Conforme** | Log épinglé fixé (PR #6) |
| `config.py` + `config.json` | ✅ **Conformes** | Paramètres stables |
| `logger.py` | ✅ **Conforme** | Stable |
| `main.py` | ✅ **Conforme** | Stable |
| `console.py` | ⚠️ **À auditer** | Dernier gros fichier (7,9 Ko) non relu en profondeur |

---

## 5. Dossier `notebooks/`

| Fichier | Verdict | Motif |
|---|---|---|
| `nb_01` → `nb_04` | ✅ **Conformes** | Convention 0-based appliquée (PR #6) |
| `nb_05` → `nb_08` | ⚠️ **À vérifier** | Convention 0-based probablement non encore appliquée |
| `nb_09_assemblage.ipynb` | ✅ **Créé** | Scénario complet, autoportant (ce commit) |

---

## Tâches restantes

| Priorité | Action |
|---|---|
| 🟡 | Audit `console.py` (7,9 Ko) — cohérence avec les correctifs log + convention batterie |
| 🟡 | Vérifier `nb_05` → `nb_08` : convention 0-based + syntaxe |
| 🟢 | `GUIDE_FORMATEUR.md` — mise à jour (sans POO, module 5 = dicts) |
| 🟢 | `tests/` : créer `test_logique.py` (batterie, propagation, mouvement invalide) |
| 🟢 | `CHANGELOG.md` : historique des versions pour les formateurs |

---

*Audit régénéré le 30 mars 2026 18h30 — à relire et valider par le mainteneur.*
