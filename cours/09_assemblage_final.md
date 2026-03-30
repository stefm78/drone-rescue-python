# Module 09 — Assemblage final

Ce module est la **notice d'assemblage** : il ne t'apprend pas de nouveau concept Python,
il t'explique comment tous les fichiers s'articulent pour former le jeu complet.

---

## 1. Structure du projet

```
jeu/
  config.json        ← tous les paramètres (source de vérité)
  config.py          ← lit config.json et expose les constantes
  logique.py         ← creer_*() + toutes les règles du jeu
  affichage.py       ← rendu console (grille, tableaux, log)
  console.py         ← boucle de jeu, 2 joueurs
  logger.py          ← partie.log + resultats.txt
  main.py            ← point d'entrée : initialise et lance la boucle
```

---

## 2. Graphe des dépendances

```
main.py
  └── console.py
        ├── logique.py
        │     └── config.py  ← lit config.json
        ├── affichage.py
        │     └── config.py
        └── logger.py
```

**Règle d'or** : `main.py` et `console.py` peuvent importer les autres,
mais les autres ne doivent jamais importer `console.py` ou `main.py`.
Cela évite les dépendances circulaires.

---

## 3. Ordre d'intégration recommandé

1. `config.json` + `config.py` — aucune dépendance, base de tout
2. `logique.py` — uniquement les fonctions `creer_*()` et l'initialisation
3. `affichage.py` — tester `render_grille()` avec une grille vide
4. `logger.py` — tester `demarrer_log()` + `enregistrer_log()`
5. `console.py` — tester la saisie d'une position
6. `main.py` — assembler et tester le tout

---

## 4. Lancer le jeu

```bash
cd jeu
python main.py
```

Le jeu se lance, affiche la grille et attend la saisie du joueur J1.

---

## 5. Flux d'un tour complet

```
┌───────────────────────────────────────────────┐
│ Tour N                                          │
│   ├── J1 : déplace jusqu'à 3 drones             │
│   │     pour chaque drone :                    │
│   │       parser_cible() → saisie joueur        │
│   │       valider_mouvement()                   │
│   │       executer_mouvement()                  │
│   │       enregistrer_log()                     │
│   ├── J2 : déplace jusqu'à 2 tempêtes           │
│   └── Auto : tempêtes restantes (50%)           │
│         + propagation zones X                  │
│         + verifier_fin_partie()                 │
│         + afficher_jeu()                        │
└───────────────────────────────────────────────┘
```

---

## 6. Checklist de rendu étudiant

- [ ] Le jeu se lance avec `python main.py` depuis `jeu/` sans erreur
- [ ] La grille s'affiche correctement (taille selon `config.json`)
- [ ] J1 peut déplacer 3 drones par tour (commande type `D1` puis `B3`)
- [ ] J2 peut déplacer 2 tempêtes par tour
- [ ] Les tempêtes restantes bougent automatiquement (50%)
- [ ] Le fichier `partie.log` est créé et lisible
- [ ] Le fichier `resultats.txt` est créé en fin de partie
- [ ] Les règles de batterie sont respectées (−1, −2 transport, −2 zone X, +3 hôpital)
- [ ] La fin de partie (victoire ou défaite) est détectée et affichée
- [ ] Les zones X se propagent tous les 3 tours

---

## 7. Pistes d'amélioration (bonus)

- Sauvegarder et reprendre une partie (`json.dump` / `json.load`)
- Ajouter un mode IA pour les drones non pilotés
- Afficher un historique des 10 derniers événements dans l'interface
- Ajouter une gestion des scores entre plusieurs parties

---

## Prompts IA utiles

> *« Comment organiser un projet Python en plusieurs fichiers sans dépendances circulaires ? »*

> *« Comment sauvegarder l'état d'un jeu Python dans un fichier JSON pour le reprendre plus tard ? »*

> *« Comment tester chaque module Python séparément avant d'assembler le projet complet ? »*
