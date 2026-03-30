# CHANGELOG — drone-rescue-python

Toutes les modifications notables du projet sont documentées ici.
Format : [PR / commit] — Date — Description

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

*Voir `ROADMAP.md` pour l'état courant et les tâches restantes.*
