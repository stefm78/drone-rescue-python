# 🚁 Drone Rescue — Cours Python par projet

> Projet pédagogique : développer un jeu de simulation de sauvetage par drones, en Python console, sur 6 semaines.

## Objectif

Apprendre Python de manière progressive en construisant un jeu complet :
- Grille ASCII paramétrable (défaut 10×10)
- Drones (D1–D3) et Tempêtes (T1–T2) déplacés par dictionnaires
- Console de pilotage 2 joueurs (drones vs tempêtes)
- Tableau de bord, historique, fichier de log et bilan final

## Prérequis

- Python 3.10 ou supérieur
- Un terminal (PowerShell, bash, zsh…)
- Aucune bibliothèque externe (stdlib uniquement)

## Lancer le jeu

```bash
cd drone-rescue-python
python jeu/main.py
```

## Structure du repo

```
drone-rescue-python/
├── README.md
├── ROADMAP.md
├── CHANTIER_CODE.md
├── REFERENTIEL_ENSEIGNEMENTS.md
├── GUIDE_FORMATEUR.md
├── AUDIT.md
├── prompt.md
├── cours/               ← fiches de cours (Markdown)
│   ├── 00_introduction.md
│   ├── 01_structures_de_base.md
│   ├── 02_boucles_et_conditions.md
│   ├── 03_fonctions.md
│   ├── 04_modules_et_io.md
│   ├── 05_dictionnaires_avances.md   ← remplace l'ancien module POO
│   ├── 06_grille_et_affichage.md
│   ├── 07_logique_de_jeu.md
│   ├── 08_console_et_log.md
│   ├── 09_assemblage_final.md
│   └── annexe_formatage.md
├── exercices/           ← énoncés d'exercices par module (ex_01 à ex_08)
├── corrections/         ← corrigés exécutables avec assert (corr_01 à corr_08)
├── notebooks/           ← notebooks Jupyter (nb_01 à nb_05)
└── jeu/                 ← code final complet jouable
    ├── config.json      ← paramètres du jeu (source de vérité)
    ├── config.py        ← lecture config.json + constantes
    ├── logique.py       ← toutes les règles (dicts uniquement, sans POO)
    ├── affichage.py     ← rendu console 3 colonnes (grille | statuts | log)
    ├── console.py       ← boucle J1/J2 + saisie joueurs
    ├── logger.py        ← partie.log + resultats.txt
    └── main.py          ← point d'entrée
```

> **Note** : `modeles.py` et `05_classes_et_objets.md` ont été supprimés — le projet n'utilise **pas** la POO (conformément aux contraintes du sujet).

## Feuille de route (6 semaines)

| Semaine | Module | Thème |
|---------|--------|-------|
| 1 | 01 + 02 | Variables, listes, boucles, conditions |
| 2 | 03 | Fonctions et gestion d'erreurs |
| 3 | 04 + 05 | Modules, I/O JSON, dictionnaires avancés |
| 4 | 06 | Grille ASCII et affichage |
| 5 | 07 + 08 | Logique de jeu + Console/Log |
| 6 | 09 | Assemblage final et tests |

## Règles du jeu (résumé)

- **Plateau** : grille carrée paramétrable (défaut 10×10), coordonnées colonne (A–J) × ligne (1–10)
- **Hôpital** : placé aléatoirement en début de partie, destination de livraison des survivants
- **Drones** : 3 drones (D1–D3), batterie max 20, déplacement diagonal autorisé (distance Chebyshev ≤ 1), 3 déplacements max par tour
- **Tempêtes** : 2 tempêtes (T1–T2), 2 déplacements max par tour, bloquent les drones 2 tours
- **Coûts** : déplacement normal −1 bat, transport survivant −2 bat, entrée zone X −2 bat supplémentaire
- **Recharge** : +3 batterie à chaque tour passé ou arrivant sur l'hôpital
- **Zones dangereuses** : propagation ortho tous les 3 tours (probabilité 30 %)
- **Fin de partie** : tous les survivants secourus (victoire) OU tous les drones HS OU 20 tours écoulés (défaite)

## Convention de log

```
T[nn]  [ID]  [départ]→[arrivée]  bat:x→y  [ÉVÈNEMENT]
```

Exemple :
```
T04  D3   B7→C8   bat:6→4
T04  D2   D5→D5   bat:8→8  BLOQUE(T2)
T05  D1   E7→A10  bat:5→6  S3  LIVRAISON S3 +1pt
```
