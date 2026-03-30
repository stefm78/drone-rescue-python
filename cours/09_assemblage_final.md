# Module 09 (Annexe) — Notice d’assemblage global

Ce module est la **notice d’assemblage** : il ne t’apprend pas de nouveau concept Python, il t’explique comment connecter tous les modules pour obtenir le jeu complet.

## Structure finale du dossier `jeu/`

```
jeu/
├── config.py       ← Paramètres globaux (modifiables par argparse)
├── modeles.py      ← Classes Drone, Tempete, Survivant, Batiment, Hopital, EtatJeu
├── logique.py      ← Règles métier (déplacements, propagation, fin de partie)
├── affichage.py    ← Rendu ASCII (grille, tableaux de bord, historique)
├── console.py      ← Boucle de saisie, parsing des commandes
├── logger.py       ← Écriture log fichier + historique écran
└── main.py         ← Point d’entrée — argparse + init + boucle
```

## Graphe des dépendances

```
main.py
  └── config.py          ← patché par argparse en premier
  └── console.py
        ├── affichage.py
        │     └── modeles.py
        ├── logique.py
        │     ├── modeles.py
        │     └── config.py
        └── logger.py
              └── config.py
```

**Règle d’or** : aucun fichier ne doit importer `console.py` ou `main.py` — ce sont les feuilles du graphe.

## Ordre d’intégration recommandé

1. **`config.py`** — aucune dépendance
2. **`modeles.py`** — classes pures, dépend de `config.py`
3. **`affichage.py`** — utilise les modèles
4. **`logique.py`** — règles, utilise modèles + config
5. **`logger.py`** — entrée/sortie fichier
6. **`console.py`** — assemble tout
7. **`main.py`** — point d’entrée final

## Lancer le jeu

```bash
cd jeu
python main.py
```

### Options de lancement (implémentées avec `argparse`)

```bash
python main.py --seed 42           # partie reproductible (même seed = même partie)
python main.py --grille 15         # grille 15×15 (min 6, max 26)
python main.py --drones 4          # 4 drones au lieu de 6 (1 à 9)
python main.py --log partie.log    # chemin du fichier journal

# Combinaisons possibles
python main.py --seed 42 --grille 8 --drones 3
```

Ces options surchargent les constantes de `config.py` au lancement. La valeur par défaut de chaque option est la valeur de `config.py`.

### Comment fonctionne le patch argparse

```python
# Dans main.py (simplifié)
args = parse_args()           # lit sys.argv
config.GRILLE_TAILLE = args.grille   # surcharge la constante
config.NB_DRONES     = args.drones   # tous les modules qui importent config
config.LOG_FICHIER   = args.log      # verront la nouvelle valeur
if args.seed is not None:
    random.seed(args.seed)           # fixe l'aléatoire AVANT initialiser_partie()
```

## Checklist de rendu étudiant

- [ ] Le jeu se lance avec `python main.py` sans erreur
- [ ] La grille s’affiche correctement (12×12 par défaut)
- [ ] Les drones sont pilotables (D1..D6, coordonnées, ok, next)
- [ ] Les tempêtes se déplacent automatiquement chaque tour
- [ ] Le fichier `.log` est créé et lisible
- [ ] L’historique des 10 dernières lignes est visible dans l’interface
- [ ] La fin de partie (victoire ou défaite) est détectée et affichée
- [ ] `--seed 42` produit la même partie à chaque lancement
- [ ] `--grille N` change effectivement la taille de la grille
- [ ] `--drones N` change effectivement le nombre de drones

## Étendre le jeu (idées bonus)

- Mode 2 joueurs (alternance des tours)
- Obstacles dynamiques (nouvelles tempêtes qui apparaissent)
- IA pour les drones non pilotés
- Sauvegarde et reprise de partie (JSON)
- Système de scoring avec classement

## Prompts IA

> *« Comment organiser un projet Python en plusieurs fichiers qui s’importent entre eux sans créer de dépendances circulaires ? »*

> *« Comment ajouter des arguments en ligne de commande à un script Python avec argparse ? »*

> *« Comment sauvegarder l’état d’un jeu Python dans un fichier JSON pour pouvoir le reprendre plus tard ? »*
