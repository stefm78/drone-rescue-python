# Guide formateur — drone-rescue-python

> Ce guide est destiné à toute personne animant ce cours en présentiel ou à distance.
> Il complète le `README.md` (vue apprenant) et le `ROADMAP.md` (vue technique).

---

## 1. Planning type 6 semaines

| Semaine | Modules | Livrables apprenant | Fichiers |
|---|---|---|---|
| 1 | 00 + 01 | Environnement installé, ex_01 passé | `cours/00`, `cours/01`, `ex_01`, `nb_01` |
| 2 | 02 + 03 | ex_02 + ex_03 passés | `cours/02`, `cours/03`, `ex_02`, `ex_03`, `nb_02`, `nb_03` |
| 3 | 04 + 05 | ex_04 + ex_05 passés, 1re classe fonctionnelle | `cours/04`, `cours/05`, `ex_04`, `ex_05`, `nb_04`, `nb_05` |
| 4 | 06 + 07 | Grille affichée + logique de mouvement | `cours/06`, `cours/07`, `ex_06`, `ex_07` |
| 5 | 08 | Saisie console + log de partie | `cours/08`, `ex_08` |
| 6 | 09 | Jeu complet jouable en console | `cours/09`, `jeu/` |

**Conseils de rythme :**
- Chaque module = 1 séance de 2h (concept + exercice guidé + correction).
- Réserver 30 min en fin de séance pour la relecture collective du code.
- Modules 07 et 09 sont les plus denses — prévoir une séance supplémentaire si besoin.

---

## 2. Quand débloquer les corrections

| Moment | Action |
|---|---|---|
| Après 20 min de blocage | Donner l’indice dans le commentaire de l’exercice |
| Après 40 min sans avancement | Montrer la signature de la fonction, pas le corps |
| En fin de séance | Débloquer `corr_0X.py` pour relecture à la maison |
| Dès le début de la séance suivante | La correction est disponible, discuter les choix |

> **Règle d’or** : ne jamais donner le code complet avant que l’apprenant ait écrit au moins une tentative.

---

## 3. Grille d’évaluation des compétences

| Compétence | Débutant | Intermédiaire | Autonome |
|---|---|---|---|
| Types de base (int, str, list, dict) | Sait créer | Sait modifier et itérer | Choisit le bon type |
| Fonctions | Sait définir + appeler | Docstring + type hints | Décompose en sous-fonctions |
| Classes | Sait écrire `__init__` | `@property` + `__str__` | Héritage + composition |
| Fichiers/IO | Sait lire/écrire avec `with` | `try/except` + `pathlib` | Logger complet |
| Logique de jeu | Valide un mouvement | Sépare validation/exécution | Retourne des événements |
| Débogage | Lit les messages d’erreur | Utilise `print` stratégique | Utilise `assert` + tests |

**Comment évaluer** : lire le code de l’exercice final (`ex_07` ou `ex_08`) et cocher la colonne correspondante pour chaque ligne.

---

## 4. Comment étendre le projet

### Ajouter une nouvelle entité (ex. : robot de ravitaillement)

1. Créer une classe `Robot(EntiteGrille)` dans `jeu/modeles.py`
2. Ajouter les règles de déplacement dans `jeu/logique.py`
3. Ajouter le symbole `'R'` dans `jeu/affichage.py` (couleur + symbole)
4. Ajouter la commande `R1`…`R9` dans `jeu/console.py` (parser)
5. Écrire `cours/10_robot.md` + `exercices/ex_10_robot.py`

### Ajouter une nouvelle règle de jeu (ex. : zone de recharge)

1. Ajouter le symbole `'Z'` dans `jeu/config.py` (`SYMBOLES`)
2. Implémenter la règle dans `executer_deplacement()` — `jeu/logique.py`
3. Documenter dans `cours/07_logique_de_jeu.md` (section Règles)
4. Ajouter un test dans `exercices/ex_07_logique.py`

### Ajouter un mode 2 joueurs

1. `jeu/config.py` : `NB_JOUEURS = 2`
2. `jeu/console.py` : alterner les boucles de saisie par joueur
3. `jeu/logger.py` : le champ `P[n]` du log est déjà prévu pour ça

---

## 5. Graphe de dépendances `jeu/`

```
main.py
  └── config.py          ← constantes globales (TAILLE, NB_DRONES…)
  └── modeles.py         ← EntiteGrille, Drone, Tempete, Survivant, EtatJeu
  └── logique.py         ← valider_mouvement, executer_deplacement, propager…
       └── modeles.py
       └── config.py
  └── affichage.py       ← afficher_grille, afficher_tableau_drones…
       └── modeles.py
  └── console.py         ← parser_commande, boucle_tour
       └── logique.py
       └── affichage.py
       └── logger.py
  └── logger.py          ← Logger (fichier + mémoire)
```

**Règle** : ne jamais importer `console.py` depuis `logique.py` ni `affichage.py` (cycle de dépendance).

---

## 6. Adapter la difficulté

| Paramètre | Fichier | Facile | Normal | Difficile |
|---|---|---|---|---|
| Taille grille | `config.py` | 8×8 | 12×12 | 12×12 |
| Nombre de drones | `config.py` | 8 | 6 | 4 |
| Nombre de survivants | `config.py` | 5 | 10 | 15 |
| Probabilité propagation | `config.py` | 0.1 | 0.3 | 0.5 |
| Batterie initiale | `config.py` | 20 | 10 | 6 |
| Tours maximum | `config.py` | 30 | 20 | 15 |

---

## 7. FAQ formateur

**Q : L’apprenant obtient `IndexError` sur la grille.**
A : Vérifier la conversion coordonnées → index : `i = ligne - 1`, `j = ord(colonne) - ord('A')`. La valeur `ligne` doit être 1-based et `colonne` une lettre str.

**Q : Les codes ANSI s’affichent sous forme de caractères bizarres sur Windows.**
A : Ajouter `import colorama; colorama.init()` en début de `main.py`, ou utiliser Windows Terminal / PowerShell 7+.

**Q : L’apprenant veut tester sans jouer (vérifier la logique seule).**
A : Montrer `if __name__ == '__main__':` dans les corrections : chaque fichier est testable indépendamment.

**Q : Comment faire jouer deux apprenants sur le même projet ?**
A : Chacun travaille sur sa branche git (`git checkout -b prenom`), comparaison en fin de séance avec `git diff`.
