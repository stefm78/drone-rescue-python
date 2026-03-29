# 🚁 Drone Rescue — Cours Python

> Projet pédagogique pour apprendre Python en construisant un jeu de simulation de sauvetage par drones, en console.

## 🗺️ Vue d'ensemble

Drone Rescue est un jeu au tour par tour en console. Des drones doivent secourir des survivants dispersés sur une grille, en gérant leur batterie, les tempêtes et les zones dangereuses.

## 📅 Planning 6 semaines

| Semaine | Modules | Objectif |
|---------|---------|----------|
| 1 | 01 + 02 | Structures de base, boucles, conditions |
| 2 | 03 + 04 | Fonctions, modules, fichiers I/O |
| 3 | 05 | Classes et objets |
| 4 | 06 | Grille et affichage ASCII |
| 5 | 07 + 08 | Logique de jeu, console et log |
| 6 | Assemblage | Notice finale, rendu |

## 📁 Structure du repo

```
drone-rescue-python/
├── README.md
├── cours/                  ← fiches de cours Markdown
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
├── exercices/              ← énoncés d'exercices
│   ├── ex_01_structures.py
│   ├── ex_02_boucles.py
│   ├── ex_03_fonctions.py
│   ├── ex_04_io.py
│   ├── ex_05_classes.py
│   ├── ex_06_grille.py
│   ├── ex_07_logique.py
│   └── ex_08_console.py
├── corrections/            ← corrigés (séparés)
│   ├── corr_01_structures.py
│   ├── corr_02_boucles.py
│   ├── corr_03_fonctions.py
│   ├── corr_04_io.py
│   ├── corr_05_classes.py
│   ├── corr_06_grille.py
│   ├── corr_07_logique.py
│   └── corr_08_console.py
└── jeu/                    ← code final du jeu
    ├── config.py
    ├── modeles.py
    ├── affichage.py
    ├── logique.py
    ├── console.py
    ├── logger.py
    └── main.py
```

## ▶️ Lancer le jeu

```bash
cd jeu
python main.py
```

Requiert **Python 3.10+**. Aucune dépendance externe.

## 🎮 Règles du jeu (résumé)

- Grille 12×12 avec colonnes A–L et lignes 1–12
- **Drones D1–D6** : batterie max 20 (init 10), déplacement diagonal autorisé, 3 déplacements/tour max
- **Tempêtes T1–T4** : 2 déplacements/tour max, immobilisent les drones (2 tours)
- **Bâtiments B** : obstacles infranchissables
- **Hôpital H** en A12 : zone de recharge et de dépôt des survivants
- **Zones dangereuses X** : se propagent (pas en diagonal, pas sur bâtiment/hôpital)
- **Fin de partie** : tous les survivants sauvés OU tours max atteints

## 🧭 Légende ASCII

```
.  case vide
B  bâtiment
H  hôpital
S  survivant
D  drone (D1–D6)
T  tempête (T1–T4)
X  zone dangereuse
```

## 📖 Format du log

```
T[nn] P[n] [D|T]  [ID] [départ]→[arrivée]  bat:x→y  surv:x  [ÉVÈNEMENT]
```

Exemples :
```
T04 P1 D  D3 B7→E6    bat:6→5    surv:—
T04 P1 D  D2 D5→D5    BLOQUÉ(T2) bat:—   surv:S3
T05 P1 D  D4 E7→A12   bat:5→4    surv:S3  LIVRAISON +1pt
```
