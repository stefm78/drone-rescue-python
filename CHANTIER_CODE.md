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
| **1** | `config.py` → `config.json` + `charger_config()` dans `logique.py` | 🔄 En cours (A fait, B à faire) |
| **2** | Suppression `modeles.py` → dicts dans `logique.py` | ⬜ À faire |
| **3** | Corrections règles de jeu (batterie, zones X, hôpital, 2 joueurs) | ⬜ À faire |
| **4** | `console.py` : 2 joueurs humains | ⬜ À faire |
| **5** | `affichage.py` : simplifications (ANSI, ternaires, slicing) | ⬜ À faire |
| **6** | `logger.py` : simplification + `resultats.txt` | ⬜ À faire |
| **7** | `main.py` : retrait argparse + sys.path | ⬜ À faire |
| **8** | Mise à jour cours, exercices, corrections, prompt.md | ⬜ À faire |

### Ce qui a été fait
- ✅ Branche `refonte/dicts-regles-officiel` créée depuis `main`
- ✅ `jeu/config.json` créé (Phase 1A)
- ⬜ `jeu/config.py` à supprimer (Phase 1B — après que `logique.py` l'utilise)
- ⬜ `charger_config()` à ajouter dans `logique.py` (Phase 1B)

### Dépendances entre phases
```
Phase 1 (config.json) → bloque Phase 2 (dicts) → bloque Phase 3 (règles) → bloque Phase 4 (console)
                                                                           → bloque Phase 5 (affichage)
Phase 6 (logger) → indépendant, peut se faire après Phase 2
Phase 7 (main.py) → en dernier sur le code
Phase 8 (cours) → tout à la fin, reflète l'état final du code
```

### Rappel architecture cible
```
jeu/
  config.json        ← remplace config.py
  logique.py         ← charger_config() + creer_drone/survivant/tempete + toutes les règles
  affichage.py       ← adapté aux dicts, sans ANSI couleur
  console.py         ← 2 joueurs humains (J1=drones, J2=tempêtes)
  logger.py          ← sauvegarder_log() + sauvegarder_resultats()
  main.py            ← sans argparse, sans sys.path
  # modeles.py       ← SUPPRIMÉ
  # config.py        ← SUPPRIMÉ
cours/
  01_...
  02_...
  ...  (modules à ajuster en Phase 8)
prompt.md            ← contexte IA complet du projet (à mettre à jour en Phase 8)
```

### Comment reprendre après une coupure
1. Lire ce fichier jusqu'au tableau des phases
2. Identifier la dernière phase `🔄 En cours`
3. Lire le fichier concerné sur la branche `refonte/dicts-regles-officiel`
4. Reprendre là où ça s'est arrêté
5. Pusher sur la même branche — **jamais directement sur `main`**

---

## Légende
- 🔧 Modification du **code du jeu** à appliquer
- 📚 **Module de cours** à créer ou enrichir
- ✅ Décision arrêtée / tâche terminée
- 🔄 En cours
- ⬜ À faire

---

## Principe directeur — Architecture des données

> **Décision définitive ✅**
> Les drones, survivants et tempêtes sont modélisés avec des **dictionnaires Python**.
> La POO (classes) est **intégralement retirée** du jeu.
> Structure de référence imposée par le sujet officiel :

```python
# Drones
drones = {
    "D1": {"col": 0, "lig": 0, "batterie": 10, "batterie_max": 20,
           "survivant": None, "bloque": 0, "hors_service": False},
    ...
}

# Survivants
survivants = {
    "S1": {"col": 3, "lig": 7, "etat": "en_attente"},  # etat : en_attente | porte | sauve
    ...
}

# Tempêtes
tempetes = {
    "T1": {"col": 8, "lig": 3},
    ...
}

# Zones dangereuses (structure imposée par le sujet)
zones_dangereuses = {
    "X1": {"position": (3, 5)},
    "X2": {"position": (7, 8)}
}

# Positions = tuples (col, lig) partout, y compris dans les sets
occupees = {(0, 0), (3, 5), ...}  # set de tuples
```

---

## Fichiers — plan de refonte

### `config.py` → 🔧 **Transformé en `config.json`** ✅
- Fichier JSON externe lu au démarrage (contrainte officielle du sujet)
- `config.py` remplacé par une fonction `charger_config()` dans `logique.py`
- `jeu/config.json` ✅ CRÉÉ
- `jeu/config.py` ⬜ À SUPPRIMER (après que `logique.py` utilise `charger_config()`)
- Structure JSON cible (déjà dans le fichier) :
```json
{
  "GRILLE_TAILLE": 12,
  "NB_DRONES": 6,
  "NB_TEMPETES": 4,
  "NB_BATIMENTS": 20,
  "NB_SURVIVANTS": 10,
  "BATTERIE_MAX": 20,
  "BATTERIE_INIT": 10,
  "PROBA_PROPAGATION": 0.3,
  "PROPAGATION_FREQUENCE": 2,
  "MAX_DEPL_DRONE": 3,
  "MAX_DEPL_TEMPETE": 2,
  "NB_TOURS_MAX": 20,
  "NB_ZONES_DANGER": 2,
  "HOPITAL_COL": 0,
  "HOPITAL_LIG": 11,
  "LOG_FICHIER": "partie.log",
  "LETTRES": "ABCDEFGHIJKL"
}
```

### `modeles.py` → ❌ **Supprimé** ⬜
- Toutes les classes disparaissent
- Remplacé par des fonctions `creer_drone()`, `creer_survivant()`, `creer_tempete()` dans `logique.py`
- `LETTRES` et `_DIRECTIONS` déplacées dans `config.json`

### `logique.py` → 🔧 **Refonte complète** ⬜
- Ajouter `charger_config()` en haut du fichier (Phase 1B)
- Toutes les méthodes d'objet deviennent des fonctions avec le dict en paramètre
- Fonctions de création : `creer_drone()`, `creer_survivant()`, `creer_tempete()`
- `depuis_chaine(texte, config)` → fonction libre (remplace `Position.depuis_chaine`)
- `distance_chebyshev(col1, lig1, col2, lig2)` → fonction libre
- `voisins_ortho(col, lig, taille)` et `voisins_diag(col, lig, taille)` → fonctions libres

### `affichage.py` → 🔧 **Adaptation** ⬜
- `drone.batterie` → `drone["batterie"]` partout
- **#12** — Remplacer les expressions ternaires par `if/else` classiques
- **#29** — Remplacer list comprehension double par deux boucles `for` imbriquées
- **#30** — Remplacer slicing négatif par calcul d'index explicite
- **#49 + #55** — Supprimer tous les codes couleur ANSI et `re`/`_strip_ansi()`
  → Conserver uniquement l'effacement d'écran `\033[2J\033[H` avec commentaire

### `console.py` → 🔧 **Adaptation + règle 2 joueurs** ⬜
- **2 joueurs humains ✅** : J1 pilote les drones, J2 pilote les tempêtes
  - Phase 1 : J1 déplace jusqu'à 3 drones
  - Phase 2 : J2 déplace jusqu'à 2 tempêtes
  - Phase 3 : tempêtes restantes bougent aléatoirement (50% de chance chacune)
- **#18** — Supprimer `EOFError` et `KeyboardInterrupt`

### `logger.py` → 🔧 **Simplification** ⬜
- **#57** — Supprimer logique d'écriture temps réel, garder uniquement `sauvegarder_log()`
- **#58** — Supprimer `try/except OSError`
- Ajouter `sauvegarder_resultats()` → fichier `resultats.txt` avec score final
  (contrainte officielle : "le score final doit être enregistré dans un fichier de résultats")

### `main.py` → 🔧 **Adaptation légère** ⬜
- **#48** — Supprimer `argparse` entièrement
- **#52** — Supprimer `sys.path.insert(...)`, lancer depuis `jeu/`

---

## Règles du jeu — corrections vs sujet officiel

| Règle | Sujet officiel | Ancien code | Action |
|-------|---------------|-------------|--------|
| Modélisation | Dictionnaires | Classes | 🔧 Refonte complète ⬜ |
| Config | Fichier externe | `config.py` | 🔧 → `config.json` ✅ créé, `config.py` ⬜ à supprimer |
| Fichier résultats | `resultats.txt` requis | Absent | 🔧 Ajouter ⬜ |
| Joueurs | 2 joueurs humains | 1 joueur | 🔧 Adapter `console.py` ⬜ |
| Tempêtes phase météo | 50% de chance de bouger | Systématique | 🔧 Corriger ⬜ |
| Zone X : perte batterie | −2 si drone entre dans zone X | Non implémenté | 🔧 Ajouter ⬜ |
| Transport survivant | Consomme 2 unités/dépl. | Consomme 1 | 🔧 Corriger ⬜ |
| Hôpital recharge | +3 par tour passé sur place | Recharge totale | 🔧 Corriger ⬜ |
| Fin de partie | Tous sauvés OU tous HS | Idem + nb tours max | ✅ Tours max = bonus acceptable |

---

## Modules de cours à créer ou enrichir

| # réf. | Sujet du module | Statut |
|--------|-----------------|--------|
| #9 | **Formatage de chaînes** : f-strings, `:<N`, `:>N`, `:02d`, `.rjust()` | ⬜ Phase 8 |
| #17 | **Gestion des erreurs** : `try/except`, `ValueError`, `finally` | ⬜ Phase 8 |
| #19 | **Fonctions** : sans param → avec param → return → valeur défaut → retour multiple | ⬜ Phase 8 |
| #24 | **Annotations de type** simples (`: int`, `-> bool`) uniquement | ⬜ Phase 8 |
| #28 | **List comprehension** : liste classique → simple → avec condition → #29 en lecture | ⬜ Phase 8 |
| #33 | **Sets** : module dédié, assimilation complète requise | ⬜ Phase 8 |
| #50 | **`if __name__ == '__main__':`** — 1 slide dédiée | ⬜ Phase 8 |
| #51 | **Structure multi-fichiers** — approche graduelle : questions à se poser, 1 fichier → N | ⬜ Phase 8 |
| #61 | **Distance de Chebyshev** — sujet court : formule + explication intuitive + exercice | ⬜ Phase 8 |
| #63 | **Propagation sur grille** — exercice de synthèse du module structures de données | ⬜ Phase 8 |
| #65 | **Architecture boucle interactive** : parser → valider → exécuter, schéma + exercice | ⬜ Phase 8 |
| POO  | **Retiré du jeu** — mentionné en "pour aller plus loin" uniquement | ✅ Décidé |

---

## Phases de travail — détail

### Phase 1 — `config.json` + `charger_config()` 🔄
**Objectif :** Remplacer `config.py` par un fichier JSON externe, lu au démarrage via `charger_config()`.
**Fichiers impactés :** `jeu/config.json` (créer), `jeu/logique.py` (ajouter `charger_config()`), `jeu/config.py` (supprimer), tout appel à `config.CONSTANTE` dans les autres modules.
**Cours impacté :** Module 04 (I/O fichiers) → exercice sur `json.load()`

Sous-étapes :
- [x] 1A — Créer `jeu/config.json` avec tous les paramètres
- [ ] 1B — Ajouter `charger_config()` dans `logique.py` + remplacer tous les `import config` par `config = charger_config()`
- [ ] 1C — Supprimer `jeu/config.py`

### Phase 2 — Suppression `modeles.py` → dicts dans `logique.py` ⬜
**Objectif :** Retirer toute la POO. Remplacer les classes par des fonctions retournant des dicts.
**Fichiers impactés :** `jeu/modeles.py` (supprimer), `jeu/logique.py` (ajouter fonctions de création), tous les autres fichiers qui importent `modeles`.
**Cours impacté :** Module 05 → renommer en `05_dictionnaires_avances.md`

Sous-étapes :
- [ ] 2A — Ajouter `creer_drone()`, `creer_survivant()`, `creer_tempete()`, `creer_zone_x()` dans `logique.py`
- [ ] 2B — Migrer `position_depuis_chaine()`, `distance_chebyshev()`, `voisins_ortho()`, `voisins_diag()` en fonctions libres
- [ ] 2C — Migrer `LETTRES` et `_DIRECTIONS` dans `config.json`
- [ ] 2D — Mettre à jour tous les imports et appels dans `affichage.py`, `console.py`, `main.py`
- [ ] 2E — Supprimer `jeu/modeles.py`

### Phase 3 — Corrections des règles de jeu ⬜
**Objectif :** Aligner le code sur le sujet officiel.
**Fichiers impactés :** `jeu/logique.py` (principalement)
**Cours impacté :** Module 07 (logique de jeu) → exercices mis à jour

- [ ] 3A — Transport survivant → 2 unités de batterie par déplacement
- [ ] 3B — Zone X → drone perd 2 unités en entrant
- [ ] 3C — Hôpital → recharge +3 par tour passé sur place (pas recharge totale)
- [ ] 3D — Phase météo → 50% de chance par tempête (pas systématique)

### Phase 4 — `console.py` : 2 joueurs humains ⬜
**Objectif :** Séparer les tours J1 (drones) et J2 (tempêtes).
**Fichiers impactés :** `jeu/console.py`
**Cours impacté :** Module 08 (console) → flux de jeu à 2 joueurs

- [ ] 4A — Phase 1 : J1 déplace jusqu'à 3 drones
- [ ] 4B — Phase 2 : J2 déplace jusqu'à 2 tempêtes
- [ ] 4C — Phase 3 : tempêtes restantes → aléatoire 50%
- [ ] 4D — Supprimer `EOFError` / `KeyboardInterrupt`

### Phase 5 — `affichage.py` : simplifications ⬜
**Objectif :** Rendre le code accessible niveau débutant.
- [ ] 5A — Retrait codes ANSI + `re` + `_strip_ansi()`
- [ ] 5B — Remplacer ternaires par `if/else`
- [ ] 5C — Remplacer list comprehension double par boucles
- [ ] 5D — Remplacer slicing négatif par index explicite

### Phase 6 — `logger.py` + `resultats.txt` ⬜
- [ ] 6A — Supprimer écriture temps réel, garder `sauvegarder_log()`
- [ ] 6B — Supprimer `try/except OSError`
- [ ] 6C — Ajouter `sauvegarder_resultats()` → `resultats.txt`

### Phase 7 — `main.py` : nettoyage ⬜
- [ ] 7A — Supprimer `argparse`
- [ ] 7B — Supprimer `sys.path.insert()`
- [ ] 7C — Vérifier `python main.py` depuis `jeu/`

### Phase 8 — Cours, exercices, corrections ⬜
- [ ] 8A — Mettre à jour `cours/05_classes_et_objets.md` → `05_dictionnaires_avances.md`
- [ ] 8B — Mettre à jour exercices et corrections des modules 04, 05, 06, 07, 08, 09
- [ ] 8C — Créer les nouveaux modules (#9, #17, #19, #28, #33, #51, #61, #65)
- [ ] 8D — Mettre à jour `prompt.md`
- [ ] 8E — Mettre à jour ce fichier CHANTIER_CODE.md (toutes cases cochées)
- [ ] 8F — **Merge `refonte/dicts-regles-officiel` → `main`**

---

*Ce fichier fait référence — ne pas modifier manuellement sans aligner avec le sujet officiel `Projet_Drones_G4.pdf`.*
