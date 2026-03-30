# CHANGELOG — drone-rescue-python

Toutes les modifications notables du projet sont documentées ici.
Format : [PR / commit] — Date — Description

---

## [PR #13] — 30 mars 2026 — Tests collision tempête + CHANGELOG

### Ajouté
- `tests/test_logique.py` : **5 nouveaux tests** couvrant la règle collision tempête (PR #11)
  - `test_tempete_bloque_drone_2_tours` : drone bloqué 2 tours après collision
  - `test_tempete_consomme_batterie_deplacement_normal` : coût = 1 sans survivant
  - `test_tempete_consomme_batterie_avec_survivant` : coût = COUT_TRANSPORT avec survivant
  - `test_tempete_zone_x_consomme_batterie_supplementaire` : coût = 1 + COUT_ZONE_X si case X
  - `test_tempete_batterie_zero_met_hors_service` : batterie 0 → hors_service=True ET bloque=2
- Total tests : **25** (20 existants + 5 tempête)

### Modifié
- `CHANGELOG.md` : PRs #11 et #12 ajoutées

---

## [PR #12] — 30 mars 2026 — Livret étudiant : intro rewrite + cours/README.md

### Ajouté
- `cours/README.md` : index du livret étudiant — tableau 9 modules (fiche / notebook / exercice / correction), guide Option A Colab et Option B local

### Modifié
- `cours/00_introduction.md` : refonte complète
  - Plan 6 semaines corrigé (plus de mention POO / classes)
  - Section « Structure du repo » avec arborescence commentée
  - Guide de démarrage pas à pas : Option A Google Colab + Option B VS Code local
  - Schéma progression 5 étapes par module
  - Structure des 8 cellules d'un notebook expliquée
  - Convention coordonnées B3 ↔ col/lig
  - Nouveau prompt IA dédié à Colab

---

## [PR #11] — 30 mars 2026 — Fix : batterie consommée lors d'une collision avec tempête

### Corrigé
- `jeu/logique.py` — `executer_mouvement()` : **bug de l'ordre des opérations**
  - **Avant** : la vérification tempête avait lieu avant la déduction batterie → batterie jamais consommée en cas de collision
  - **Après** : coût calculé et batterie déduite en premier, dans **tous** les cas (avec ou sans survivant, avec ou sans zone X)
  - Cas limite : batterie tombe à 0 après collision → `hors_service = True` + `bloque = 2` (label `HS+BLOQUE(T1)` dans le log)
- `ROADMAP.md` : synchronisé 100% (toutes tâches complètes)

---

## [PR #9] — 30 mars 2026 — Audit console.py

### Corrigé
- `drones_dispo` : ajout du filtre `batterie > 0` — un drone à 0 batterie n'apparaît plus dans la liste disponible
- `boucle_de_jeu` : `verifier_fin_partie()` ajouté après `deplacer_tempetes()`, avant `propager_zones_x()` — détecte les défaites causées par les tempêtes
- `_phase_drones` : suppression du `render_complet` doublon (double effacement écran inutile)

---

## [PR #8] — 30 mars 2026 — Fix propagation, batterie, nb_09, docs

### Corrigé
- `propager_zones_x` : retourne désormais **une seule ligne** de log condensée (`T06  [X] PROPAGATION  +3 → A2, B4, C1`) — suppression de la boucle multi-lignes
- `valider_mouvement` : calcul du **coût réel** (`COUT_TRANSPORT + COUT_ZONE_X`) effectué avant d'autoriser le mouvement — refus propre si `batterie < cout_reel`

### Ajouté
- `notebooks/nb_09_assemblage.ipynb` : notebook d'assemblage final — scénario complet init→drones→mouvements→sauvetages→propagation→résumé
- `ROADMAP.md` : synchronisé post-PR #8

---

## [PR #7] — 30 mars 2026 — Fix batterie, log propagation, archive prompt

### Corrigé
- `valider_mouvement` : garde-fou batterie insuffisante dans `executer_mouvement`
- `propager_zones_x` : ligne de résumé + marqueur `[X]` (base de la refonte terminée en PR #8)

### Modifié
- `prompt.md` déplacé dans `archive/prompt.md` (invisible pour les apprenants)

---

## [PR #6] — 30 mars 2026 — Log épinglé + synchro nb_01→nb_04 0-based

### Corrigé
- `render_log_col` : lignes `[X]` épinglées en bas du log, hors quota des lignes normales
- `propager_zones_x` : préfixe `[X]` sur toutes les lignes de propagation

### Modifié
- `nb_01` → `nb_04` : synchro convention 0-based complète (coords int, `pos_str`/`pos_depuis_chaine`, `random.randint(0, TAILLE-1)`)

---

## [PR #5] — 30 mars 2026 — Phase 9C assemblage

### Ajouté
- `exercices/ex_09_assemblage.py` : exercice final en 5 parties A→E (100% autoportant, sans import de `jeu/`)
- `corrections/corr_09_assemblage.py` : solutions complètes + `assert` exécutables

---

## [PR #4] — 30 mars 2026 — Phase 13 : notebooks nb_05→nb_08

### Ajouté
- `notebooks/nb_05_dicts_avances.ipynb`
- `notebooks/nb_06_grille_affichage.ipynb`
- `notebooks/nb_07_logique_jeu.ipynb`
- `notebooks/nb_08_console_log.ipynb`

### Supprimé
- `notebooks/nb_05_classes.ipynb` (remplacé par nb_05_dicts_avances)

---

## [PR #3] — 30 mars 2026 — Phase 10 : README + ROADMAP

### Modifié
- `README.md` : arborescence à jour, paramètres officiels, `modeles.py` retiré
- `ROADMAP.md` : tableau d'avancement phases 1→10, prompt de reprise IA

---

## [PR #1 / #2] — 2026 — Refonte complète

### Modifié
- Suppression complète de la POO — passage à 100% dictionnaires
- `creer_drone()`, `creer_tempete()`, `creer_survivant()` remplacent les classes
- Convention 0-based pour toutes les coordonnées internes
- Règles officielles appliquées : coûts, recharge, propagation zones X, blocage tempête
- Cours `00`→`09`, exercices `01`→`09`, corrections `01`→`09` refondus

---

*Voir `ROADMAP.md` pour l'état courant.*
