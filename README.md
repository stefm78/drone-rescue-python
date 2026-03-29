# 🚁 Drone Rescue — Cours Python

> Projet pédagogique : apprendre Python en construisant un jeu de simulation de sauvetage par drones, jouable en console.

## Présentation

Drone Rescue est un jeu au tour par tour en console. Des drones doivent secourir des survivants dispersés sur une grille, malgré des tempêtes et des zones dangereuses.

Ce repository contient **le cours complet** (9 modules), **les exercices** (avec références et prompts IA), **les corrections** et **le code final jouable**.

## Structure

```
drone-rescue-python/
├── cours/                  ← fiches de cours Markdown (modules 00 à 09)
├── exercices/              ← énoncés Python commentés
├── corrections/            ← corrigés (à ouvrir seulement après avoir essayé)
├── jeu/                    ← code final complet et jouable
└── README.md
```

## Prérequis

- Python 3.10 ou supérieur
- Terminal (PowerShell, bash, zsh…)
- Aucune bibliothèque externe — stdlib uniquement (`random`, `os`, `re`, `pathlib`)

## Lancer le jeu

```bash
cd jeu
python main.py
```

## Plan du cours (6 semaines)

| Semaine | Module | Thème |
|---------|--------|-------|
| 1 | 01 | Structures de base — variables, listes, dicts |
| 1 | 02 | Boucles et conditions |
| 2 | 03 | Fonctions |
| 2 | 04 | Modules et I/O fichiers |
| 3 | 05 | Classes et objets |
| 3 | 06 | Grille et affichage ASCII |
| 4 | 07 | Logique de jeu |
| 5 | 08 | Console et log |
| 6 | 09 | Assemblage final (annexe) |

## Conventions du repo

- Les **énoncés** sont dans `exercices/` — ils contiennent les instructions mais pas les solutions.
- Les **corrections** sont dans `corrections/` — ne les ouvrir qu'après avoir tenté l'exercice.
- Chaque fichier de cours contient des **tips**, **best practices**, **références** et **prompts IA** pour aller plus loin.

## Règles du jeu (résumé)

| Paramètre | Valeur par défaut | Modifiable |
|-----------|-------------------|------------|
| Taille grille | 12×12 | `config.py` |
| Drones | 6 | `config.py` |
| Tempêtes | 4 | `config.py` |
| Bâtiments | 20 | `config.py` |
| Batterie max | 20 | `config.py` |
| Batterie initiale | 10 | `config.py` |
| Déplacements/tour (drone) | 3 max | `config.py` |
| Déplacements/tour (tempête) | 2 max | `config.py` |
| Probabilité propagation | 0.3 | `config.py` |
| Tours max | 20 | `config.py` |

**Fin de partie :** tous les survivants sauvés OU nombre de tours épuisé.
