# CHANTIER — Modifications identifiées à appliquer
> Généré le 2026-03-30 — suivi des décisions issues de la revue pédagogique du référentiel.

---

## Légende
- 🔧 Modification du **code du jeu** à appliquer
- 📚 **Module de cours** à créer ou enrichir
- ✅ Décision arrêtée
- 🔄 En discussion

---

## Modifications du code du jeu (à appliquer)

### `affichage.py`
- 🔧 **#12** — Remplacer les expressions ternaires par des `if/else` classiques ✅
- 🔧 **#29** — Remplacer la list comprehension double `[['.' for _] for _]` par deux boucles `for` imbriquées explicites ✅
- 🔧 **#30** — Remplacer le slicing `historique[-(max(1, n-1)):]` par un calcul d'index explicite ✅
- 🔧 **#49** — Supprimer `re` et `_strip_ansi()` (lié au retrait #55 ci-dessous) ✅
- 🔧 **#55** — Retirer tous les codes couleur ANSI ; conserver uniquement l'effacement d'écran `\033[2J\033[H` avec commentaire explicatif ✅

### `modeles.py`
- 🔧 **#23** — Extraire `_cible_libre(pos)` hors de `deplacer_tempetes()` (supprimer la fonction imbriquée) ✅
- 🔧 **POO #38** — Supprimer `__eq__` → remplacer les comparaisons de `Position` par comparaison explicite `.col` et `.lig` 🔄 *(voir impact sur logique.py et sets)*
- 🔧 **POO #39** — Supprimer `__hash__` → remplacer les sets de `Position` par des sets de tuples `(col, lig)` 🔄 *(refonte partielle de logique.py)*
- 🔧 **POO #40** — Supprimer `@classmethod` sur `depuis_chaine` → transformer en fonction autonome dans `logique.py` 🔄
- 🔧 **POO #42/#43** — Supprimer les annotations union `Drone | None` et les références circulaires `"Position"` → annotations simples ou supprimées ✅

### `logique.py`
- 🔧 **#64** — Remplacer la logique de rebond directionnel des tempêtes par `random.choice(voisins_libres)` pur ✅
- 🔧 **#58** — Supprimer les `try/except OSError` dans `logger.py` (contexte pédagogique : disque supposé OK) ✅

### `console.py`
- 🔧 **#18** — Supprimer la capture de `EOFError` et `KeyboardInterrupt` dans `_prompt()` ✅

### `logger.py`
- 🔧 **#57** — Simplifier : supprimer la logique d'écriture temps réel (`_fichier_ouvert`, `_ecrire_fichier`, `fermer_log`) ; ne conserver que `sauvegarder_log()` avec `with open(...)` ✅
- 🔧 **#58** — Supprimer le `try/except OSError` (cf. ci-dessus) ✅

### `main.py`
- 🔧 **#48** — Supprimer `argparse` entièrement (`parse_args`, `appliquer_args`) ; les paramètres sont lus depuis `config.py` ✅
- 🔧 **#52** — Supprimer `sys.path.insert(...)` ; restructurer le lancement depuis le dossier `jeu/` ✅

---

## Modules de cours à créer ou enrichir

| # réf. | Sujet du module | Statut |
|--------|-----------------|--------|
| #9  | **Formatage de chaînes** : f-strings, `:<N`, `:>N`, `:02d`, `.rjust()` — module dédié avec exercices | ✅ À créer |
| #17 | **Gestion des erreurs** : `try/except`, exceptions nommées (`ValueError`, `OSError`), `finally` | ✅ À créer |
| #19 | **Fonctions** : module dédié avec progression (sans param → avec param → return → valeur par défaut → retour multiple) | ✅ À créer |
| #24 | **Annotations de type** : conserver les annotations simples (`: int`, `-> bool`) ; retirer les complexes du code | ✅ Décidé |
| #28 | **List comprehension** : module dédié — liste classique → comprehension simple → avec condition → intro #29 en lecture | ✅ À créer |
| #33 | **Sets** : module dédié après listes et dicts — création, `.add()`, `in`, union `\|` — objectif : assimilation complète | ✅ À créer |
| #50 | **`if __name__ == '__main__':`** — 1 slide dédiée dans le module Modules & organisation | ✅ À créer |
| #51 | **Structure multi-fichiers** — approche graduelle avec les questions à se poser : *Pourquoi découper ? Quand ? Comment nommer les responsabilités ? Quels avantages ?* Architecture progressive : 1 fichier → 2 → N | ✅ À créer |
| #61 | **Distance de Chebyshev** — sujet court dans le cours algo : formule, explication intuitive, exercice rapide | ✅ À créer |
| #65 | **Architecture boucle interactive** : pattern parser → valider → exécuter ; schéma de flux + exercice guidé | ✅ À créer |

---

## Points encore en discussion 🔄

| # réf. | Sujet | Question ouverte |
|--------|-------|-----------------|
| POO #34-#41 | **Portée de la POO dans le cours** | Quels concepts garder en écriture vs lecture ? Impact du retrait de `__eq__`/`__hash__` sur l'architecture des sets ? |
| #63 | **Propagation sur grille** | Objectif : les élèves doivent pouvoir écrire 100% du code — comment rendre ce concept accessible ? Découpage en étapes ? |

---

*Ce fichier est mis à jour au fil des décisions — ne pas modifier manuellement sans aligner avec REFERENTIEL_ENSEIGNEMENTS.md.*
