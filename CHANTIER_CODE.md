# CHANTIER — Modifications identifiées à appliquer
> Dernière mise à jour : 2026-03-30
> Document de référence officiel : `Projet_Drones_G4.pdf`
> Branche de travail : `refonte/dicts-regles-officiel` (merge dans `main` à la fin)

---

## 🤖 Contexte de reprise — À LIRE EN PREMIER si tu reprends ce chantier

Ce projet est un **cours Python** basé sur un jeu (sauvetage de drones). Il y a deux niveaux :
- Le **code du jeu** dans `jeu/` (ce que les étudiants voient tourner)
- Les **modules de cours** dans `cours/` (ce qu'ils apprennent étape par étape)

Toutes les modifications se font sur la branche `refonte/dicts-regles-officiel`.
Le merge vers `main` n'a lieu qu'une fois TOUTES les phases terminées et validées.

### État des phases au 2026-03-30

| Phase | Contenu | Statut |
|-------|---------|--------|
| **1** | `config.py` → `config.json` + constantes lues via `json.load()` | ✅ Terminée |
| **2** | Suppression `modeles.py` → dicts dans `logique.py` | ✅ Terminée |
| **3** | Corrections règles de jeu (batterie, zones X, hôpital, météo 50%) | ✅ Terminée |
| **4** | `console.py` : 2 joueurs humains (J1=drones, J2=tempêtes) | ✅ Terminée |
| **5** | `affichage.py` : sans ANSI, sans `re`, sans ternaires | ✅ Terminée |
| **6** | `logger.py` : simplifié + `resultats.txt` | ✅ Terminée |
| **7** | `main.py` : sans argparse, sans sys.path | ✅ Terminée |
| **8** | Mise à jour cours, exercices, corrections, REFERENTIEL, prompt.md | 🔄 En cours |

### Ce qui a été fait (code)
- ✅ `jeu/config.json` créé
- ✅ `jeu/config.py` réécrit : lit `config.json` via `json.load()`
- ✅ `jeu/logique.py` réécrit : 100% dicts, `creer_drone/survivant/tempete()`, toutes règles officielles
- ✅ `jeu/affichage.py` réécrit : sans ANSI, sans `re`, travaille sur dicts
- ✅ `jeu/console.py` réécrit : 2 joueurs humains, architecture parser→valider→exécuter
- ✅ `jeu/logger.py` réécrit : `partie.log` + `resultats.txt`
- ✅ `jeu/main.py` réécrit : sans argparse, sans sys.path
- ✅ `jeu/modeles.py` supprimé

### Phase 8 — sous-étapes

| Sous-étape | Contenu | Statut |
|------------|---------|--------|
| 8A | `cours/05_classes_et_objets.md` → `cours/05_dictionnaires_avances.md` | ✅ Fait |
| 8B | Mise à jour des modules 01 à 04 (cohérence avec le nouveau code) | ⬜ À faire |
| 8C | Mise à jour des modules 06 à 09 (cohérence avec le nouveau code) | ⬜ À faire |
| 8D | Créer les nouveaux modules (#9, #17, #28, #33, #51, #61, #65) | ⬜ À faire |
| 8E | Mettre à jour `REFERENTIEL_ENSEIGNEMENTS.md` | ⬜ À faire |
| 8F | Mettre à jour `prompt.md` | ⬜ À faire |
| 8G | Merge `refonte/dicts-regles-officiel` → `main` | ⬜ Dernière étape |

### Comment reprendre après une coupure
1. Lire ce fichier jusqu'au tableau des phases
2. Identifier la dernière phase `🔄 En cours`
3. Lire les fichiers cours/ sur la branche `refonte/dicts-regles-officiel`
4. Reprendre là où ça s'est arrêté
5. Pusher sur la même branche — **jamais directement sur `main`**

---

## Légende
- 🔧 Modification du **code du jeu**
- 📚 **Module de cours** à créer ou enrichir
- ✅ Décision arrêtée / tâche terminée
- 🔄 En cours
- ⬜ À faire

---

## Architecture finale du code (état actuel ✅)

```
jeu/
  config.json        ← source de vérité de tous les paramètres
  config.py          ← lit config.json et expose les constantes
  logique.py         ← creer_*() + toutes les règles du jeu
  affichage.py       ← rendu console, sans ANSI couleur
  console.py         ← boucle de jeu, 2 joueurs
  logger.py          ← partie.log + resultats.txt
  main.py            ← point d'entrée unique, sans argparse
  # modeles.py       ← SUPPRIMÉ
cours/
  00_introduction.md
  01_structures_de_base.md
  02_boucles_et_conditions.md
  03_fonctions.md
  04_modules_et_io.md
  05_dictionnaires_avances.md    ← remplace 05_classes_et_objets.md
  06_grille_et_affichage.md
  07_logique_de_jeu.md
  08_console_et_log.md
  09_assemblage_final.md
REFERENTIEL_ENSEIGNEMENTS.md
CHANTIER_CODE.md
prompt.md
```

---

## Modules de cours à créer ou enrichir (Phase 8D)

| # réf. | Sujet du module | Fichier cible | Statut |
|--------|-----------------|---------------|--------|
| #9 | **Formatage de chaînes** : f-strings, `:<N`, `:02d` | `cours/annexe_formatage.md` | ⬜ |
| #17 | **Gestion des erreurs** : `try/except`, `ValueError` | intégrer dans `03_fonctions.md` | ⬜ |
| #28 | **List comprehension** : simple → avec condition | intégrer dans `01_structures_de_base.md` | ⬜ |
| #33 | **Sets** : module dédié, assimilation complète | intégrer dans `05_dictionnaires_avances.md` | ⬜ |
| #50 | **`if __name__ == '__main__'`** | intégrer dans `04_modules_et_io.md` | ⬜ |
| #51 | **Structure multi-fichiers** : graduel, questions à se poser | intégrer dans `04_modules_et_io.md` | ⬜ |
| #61 | **Distance de Chebyshev** : formule courte + exercice | intégrer dans `06_grille_et_affichage.md` | ⬜ |
| #65 | **Boucle interactive** : parser→valider→exécuter | intégrer dans `08_console_et_log.md` | ⬜ |

---

*Ce fichier fait référence — ne pas modifier manuellement sans aligner avec le sujet officiel `Projet_Drones_G4.pdf`.*
