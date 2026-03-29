# 🚁 Drone Rescue — Cours Python débutant

> Projet pédagogique sur 6 semaines · Python 3.10+ · Console ASCII

## Présentation

Drone Rescue est un jeu de plateau en console où des drones doivent secourir des survivants dispersés sur une grille, en évitant des tempêtes et des zones dangereuses.

Ce repo contient :
- **Un cours progressif** (9 modules + annexe) du niveau débutant jusqu'au projet complet
- **Des exercices** par module avec énoncés, références et corrigés séparés
- **Le jeu complet** prêt à jouer

## Prérequis

```
Python 3.10 ou supérieur
Aucune bibliothèque externe requise (stdlib uniquement)
```

## Lancer le jeu

```bash
cd jeu
python main.py
```

## Structure du repo

```
drone-rescue-python/
│
├── README.md
├── cours/
│   ├── 00_introduction.md
│   ├── 01_structures_de_base.md
│   ├── 02_boucles_et_conditions.md
│   ├── 03_fonctions.md
│   ├── 04_modules_et_io.md
│   ├── 05_classes_et_objets.md
│   ├── 06_grille_et_affichage.md
│   ├── 07_logique_de_jeu.md
│   ├── 08_console_et_log.md
│   └── 09_assemblage_final.md
│
├── exercices/
│   ├── ex_01_structures.py
│   ├── ex_02_boucles.py
│   ├── ex_03_fonctions.py
│   ├── ex_04_io.py
│   ├── ex_05_classes.py
│   ├── ex_06_grille.py
│   ├── ex_07_logique.py
│   └── ex_08_console.py
│
├── corrections/
│   ├── corr_01_structures.py
│   ├── corr_02_boucles.py
│   ├── corr_03_fonctions.py
│   ├── corr_04_io.py
│   ├── corr_05_classes.py
│   ├── corr_06_grille.py
│   ├── corr_07_logique.py
│   └── corr_08_console.py
│
└── jeu/
    ├── config.py
    ├── modeles.py
    ├── affichage.py
    ├── console.py
    ├── logique.py
    ├── logger.py
    └── main.py
```

## Feuille de route 6 semaines

| Semaine | Modules | Objectif |
|---------|---------|----------|
| 1 | 00 + 01 | Prise en main Python, structures de données |
| 2 | 02 + 03 | Boucles, conditions, fonctions |
| 3 | 04 + 05 | Modules, I/O fichiers, classes |
| 4 | 06 + 07 | Grille ASCII, logique de jeu |
| 5 | 08 | Console interactive, historique |
| 6 | 09 | Assemblage final, tests, rendu |

## Règles du jeu (résumé)

- **Drones** (D1–D6) : se déplacent en diagonal, transportent des survivants vers l'hôpital
- **Tempêtes** (T1–T4) : bloquent les drones 2 tours, se déplacent (pas sur l'hôpital)
- **Zones dangereuses** : se propagent tous les 2 tours (pas en diagonal, pas sur bâtiment/hôpital)
- **Batterie** : max paramétrable (défaut 20), charge initiale paramétrable (défaut 10)
- **Fin de partie** : tous les survivants secourus OU drones tous HS

## Licence

MIT — usage libre pour apprentissage et enseignement.
