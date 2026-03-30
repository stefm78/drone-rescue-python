# CHANTIER — Modifications identifiées à appliquer
> Dernière mise à jour : 2026-03-30
> Document de référence officiel : `Projet_Drones_G4.pdf`

---

## Légende
- 🔧 Modification du **code du jeu** à appliquer
- 📚 **Module de cours** à créer ou enrichir
- ✅ Décision arrêtée
- 🔄 En cours

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

### `modeles.py` → ❌ **Supprimé**
- Toutes les classes disparaissent
- Remplacé par des fonctions `creer_drone()`, `creer_survivant()`, `creer_tempete()` dans `logique.py`
- `LETTRES` et `_DIRECTIONS` déplacées dans `config.py` comme constantes

### `config.py` → 🔧 **Transformé en `config.json`** ✅
- Fichier JSON externe lu au démarrage (contrainte officielle du sujet)
- `config.py` remplacé par une fonction `charger_config()` dans `logique.py`
- Structure JSON cible :
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
  "MAX_DEPL_DRONE": 3,
  "MAX_DEPL_TEMPETE": 2,
  "NB_TOURS_MAX": 20,
  "NB_ZONES_DANGER": 2
}
```

### `logique.py` → 🔧 **Refonte complète**
- Toutes les méthodes d'objet deviennent des fonctions avec le dict en paramètre
- Fonctions de création : `creer_drone()`, `creer_survivant()`, `creer_tempete()`
- `depuis_chaine(texte, config)` → fonction libre (remplace `Position.depuis_chaine`)
- `distance_chebyshev(col1, lig1, col2, lig2)` → fonction libre
- `voisins_ortho(col, lig, taille)` et `voisins_diag(col, lig, taille)` → fonctions libres

### `affichage.py` → 🔧 **Adaptation**
- `drone.batterie` → `drone["batterie"]` partout
- **#12** — Remplacer les expressions ternaires par `if/else` classiques ✅
- **#29** — Remplacer list comprehension double par deux boucles `for` imbriquées ✅
- **#30** — Remplacer slicing négatif par calcul d'index explicite ✅
- **#49 + #55** — Supprimer tous les codes couleur ANSI et `re`/`_strip_ansi()` ✅
  → Conserver uniquement l'effacement d'écran `\033[2J\033[H` avec commentaire

### `console.py` → 🔧 **Adaptation + règle 2 joueurs**
- **2 joueurs humains ✅** : J1 pilote les drones, J2 pilote les tempêtes
  - Phase 1 : J1 déplace jusqu'à 3 drones
  - Phase 2 : J2 déplace jusqu'à 2 tempêtes
  - Phase 3 : tempêtes restantes bougent aléatoirement (50% de chance chacune)
- **#18** — Supprimer `EOFError` et `KeyboardInterrupt` ✅

### `logger.py` → 🔧 **Simplification**
- **#57** — Supprimer logique d'écriture temps réel, garder uniquement `sauvegarder_log()` ✅
- **#58** — Supprimer `try/except OSError` ✅
- Ajouter `sauvegarder_resultats()` → fichier `resultats.txt` avec score final ✅
  (contrainte officielle : "le score final doit être enregistré dans un fichier de résultats")

### `main.py` → 🔧 **Adaptation légère**
- **#48** — Supprimer `argparse` entièrement ✅
- **#52** — Supprimer `sys.path.insert(...)`, lancer depuis `jeu/` ✅

---

## Règles du jeu — corrections vs sujet officiel

| Règle | Sujet officiel | Ancien code | Action |
|-------|---------------|-------------|--------|
| Modélisation | Dictionnaires | Classes | 🔧 Refonte complète ✅ |
| Config | Fichier externe | `config.py` | 🔧 → `config.json` ✅ |
| Fichier résultats | `resultats.txt` requis | Absent | 🔧 Ajouter ✅ |
| Joueurs | 2 joueurs humains | 1 joueur | 🔧 Adapter `console.py` ✅ |
| Tempêtes phase météo | 50% de chance de bouger | Systématique | 🔧 Corriger ✅ |
| Zone X : perte batterie | −2 si drone entre dans zone X | Non implémenté | 🔧 Ajouter ✅ |
| Transport survivant | Consomme 2 unités/dépl. | Consomme 1 | 🔧 Corriger ✅ |
| Hôpital recharge | +3 par tour passé sur place | Recharge totale | 🔧 Corriger ✅ |
| Fin de partie | Tous sauvés OU tous HS | Idem + nb tours max | ✅ Tours max = bonus acceptable |

---

## Modules de cours à créer ou enrichir

| # réf. | Sujet du module | Statut |
|--------|-----------------|--------|
| #9 | **Formatage de chaînes** : f-strings, `:<N`, `:>N`, `:02d`, `.rjust()` | ✅ À créer |
| #17 | **Gestion des erreurs** : `try/except`, `ValueError`, `finally` | ✅ À créer |
| #19 | **Fonctions** : sans param → avec param → return → valeur défaut → retour multiple | ✅ À créer |
| #24 | **Annotations de type** simples (`: int`, `-> bool`) uniquement | ✅ Décidé |
| #28 | **List comprehension** : liste classique → simple → avec condition → #29 en lecture | ✅ À créer |
| #33 | **Sets** : module dédié, assimilation complète requise | ✅ À créer |
| #50 | **`if __name__ == '__main__':`** — 1 slide dédiée | ✅ À créer |
| #51 | **Structure multi-fichiers** — approche graduelle : questions à se poser, 1 fichier → N | ✅ À créer |
| #61 | **Distance de Chebyshev** — sujet court : formule + explication intuitive + exercice | ✅ À créer |
| #63 | **Propagation sur grille** — exercice de synthèse du module structures de données | ✅ Décidé |
| #65 | **Architecture boucle interactive** : parser → valider → exécuter, schéma + exercice | ✅ À créer |
| POO  | **Retiré du jeu** — mentionné en "pour aller plus loin" uniquement | ✅ Décidé |

---

## Phases de travail prévues

1. **Phase 1** — Refonte `modeles.py` → suppression, migration vers dictionnaires dans `logique.py`
2. **Phase 2** — `config.py` → `config.json` + fonction `charger_config()`
3. **Phase 3** — Corrections des règles de jeu (batterie, zones X, recharge hôpital, 2 joueurs)
4. **Phase 4** — `affichage.py` : retraits ANSI, ternaires, simplifications
5. **Phase 5** — `logger.py` : simplification + ajout `resultats.txt`
6. **Phase 6** — `main.py` : retraits argparse, sys.path
7. **Phase 7** — Mise à jour `prompt.md` pour aligner sur les décisions
8. **Phase 8** — Création des modules de cours

---

*Ce fichier fait référence — ne pas modifier manuellement sans aligner avec le sujet officiel `Projet_Drones_G4.pdf`.*
