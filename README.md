# 🚁 Drone Rescue — Cours Python par projet

> Projet pédagogique : développer un jeu de simulation de sauvetage par drones, en Python console, sur 6 semaines.

## Objectif

Apprendre Python de manière progressive en construisant un jeu complet :
- Grille ASCII 12×12
- Drones (D1–D6) et Tempêtes (T1–T4) avec identifiants
- Console de pilotage type ligne de commande
- Tableau de bord, historique, fichier de log

## Prérequis

- Python 3.10 ou supérieur
- Un terminal (PowerShell, bash, zsh…)
- Aucune bibliothèque externe (stdlib uniquement)

## Lancer le jeu

```bash
cd jeu
python main.py
```

## Structure du repo

```
drone-rescue-python/
├── README.md
├── cours/               ← fiches de cours (Markdown)
│   ├── 00_introduction.md
│   ├── 01_structures_de_base.md
│   ├── 02_boucles_et_conditions.md
│   ├── 03_fonctions.md
│   ├── 04_modules_et_io.md
│   ├── 05_classes_et_objets.md
│   ├── 06_grille_et_affichage.md
│   ├── 07_logique_de_jeu.md
│   ├── 08_console_et_log.md
│   └── 09_assemblage_final.md  ← annexe notice d'assemblage
├── exercices/           ← énoncés d'exercices par module
├── corrections/         ← corrigés (à consulter après avoir essayé)
└── jeu/                 ← code final complet jouable
    ├── config.py
    ├── modeles.py
    ├── logique.py
    ├── affichage.py
    ├── console.py
    ├── logger.py
    └── main.py
```

## Feuille de route (6 semaines)

| Semaine | Module | Thème |
|---------|--------|-------|
| 1 | 01 + 02 | Variables, boucles, conditions |
| 2 | 03 | Fonctions |
| 3 | 04 + 05 | Modules, I/O, Classes |
| 4 | 06 | Grille ASCII et affichage |
| 5 | 07 + 08 | Logique de jeu + Console/Log |
| 6 | 09 | Assemblage final et tests |

## Règles du jeu (résumé)

- **Plateau** : grille 12×12 (paramétrable), coordonnées colonne (A–L) × ligne (1–12)
- **Hôpital** : case A12, destination de livraison des survivants
- **Drones** : 6 drones (D1–D6), batterie max 20 (défaut init 10), déplacement diagonal autorisé, 3 déplacements max par tour
- **Tempêtes** : 4 tempêtes (T1–T4), 2 déplacements max par tour, bloquent les drones 2 tours
- **Zones dangereuses** : propagation tous les 2 tours (pas en diagonal, pas sur bâtiment/hôpital/survivant)
- **Fin de partie** : tous les survivants secourus OU tous les drones HS

## Convention de log

```
T[nn] P[n] [D|T]  [ID] [départ]→[arrivée]  bat:x→y  surv:x  [ÉVÈNEMENT]
```

Exemple :
```
T04 P1 D  D3 B7→E6    bat:6→5    surv:—
T04 P1 D  D2 D5→D5    BLOQUÉ(T2) bat:—      surv:S3
T05 P1 D  D4 E7→A12   bat:5→4    surv:S3    LIVRAISON +1pt
```
