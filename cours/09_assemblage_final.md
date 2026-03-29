# Module 09 (Annexe) — Notice d'assemblage global

Ce module est la **notice d'assemblage** : il ne t'apprend pas de nouveau concept Python, il t'explique comment connecter tous les modules pour obtenir le jeu complet.

## Structure finale du dossier `jeu/`

```
jeu/
├── config.py       ← Paramètres globaux
├── modeles.py      ← Classes Drone, Tempete, Survivant, Batiment, Hopital, EtatJeu
├── logique.py      ← Règles métier (déplacements, propagation, fin de partie)
├── affichage.py    ← Rendu ASCII (grille, tableaux de bord, historique)
├── console.py      ← Boucle de saisie, parsing des commandes
├── logger.py       ← Écriture log fichier + historique écran
└── main.py         ← Point d'entrée — initialisation + boucle principale
```

## Graphe des dépendances

```
main.py
  └── console.py
        ├── affichage.py
        │     └── modeles.py
        ├── logique.py
        │     ├── modeles.py
        │     └── config.py
        └── logger.py
              └── config.py
```

**Règle d'or** : aucun fichier ne doit importer `console.py` ou `main.py` — ce sont les feuilles du graphe de dépendances.

## Ordre d'intégration recommandé

1. **`config.py`** — aucune dépendance, commencer par là
2. **`modeles.py`** — classes pures, ne dépend que de `config.py`
3. **`affichage.py`** — utilise les modèles, teste avec des données fictives
4. **`logique.py`** — règles, utilise modèles + config
5. **`logger.py`** — entrée/sortie fichier
6. **`console.py`** — assemble tout
7. **`main.py`** — point d'entrée final

## Lancer le jeu

```bash
cd jeu
python main.py
```

Options de lancement :

```bash
python main.py --seed 42          # partie reproductible
python main.py --grille 15        # grille 15×15
python main.py --drones 4         # 4 drones
python main.py --log partie.log   # chemin du fichier log
```

## Checklist de rendu étudiant

- [ ] Le jeu se lance avec `python main.py` sans erreur
- [ ] La grille s'affiche correctement (12×12 par défaut)
- [ ] Les drones sont pilotables via la console (D1..D6, coordonnées, ok, next)
- [ ] Les tempêtes se déplacent automatiquement chaque tour
- [ ] Le fichier `.log` est créé et lisible
- [ ] L'historique des 10 dernières lignes est visible dans l'interface
- [ ] La fin de partie (victoire ou défaite) est détectée et affichée
- [ ] Les paramètres de `config.py` sont effectivement pris en compte

## Étendre le jeu (idées bonus)

- Ajouter un mode 2 joueurs (alternance des tours)
- Ajouter des obstacles dynamiques (nouvelles tempêtes qui apparaissent)
- Ajouter une IA pour les drones non pilotés
- Sauvegarder et reprendre une partie (sérialisation JSON)
- Ajouter un système de scoring avec classement

## Prompts IA

> *« Comment organiser un projet Python en plusieurs fichiers qui s'importent entre eux sans créer de dépendances circulaires ? »*

> *« Comment ajouter des arguments en ligne de commande à un script Python avec argparse ? »*

> *« Comment sauvegarder l'état d'un jeu Python dans un fichier JSON pour pouvoir le reprendre plus tard ? »*
