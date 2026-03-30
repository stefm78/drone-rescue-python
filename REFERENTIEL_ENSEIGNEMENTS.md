# Référentiel des enseignements Python — Drone Rescue

> **Objectif de ce fichier**  
> Lister tous les concepts Python qu'un apprenant débutant doit maîtriser
> pour être capable de lire, comprendre et écrire le code du jeu Drone Rescue.  
> Ce référentiel sert de grille de vérification : chaque entrée doit correspondre
> à un (ou plusieurs) module(s) du cours.

---

## Comment utiliser ce fichier

Chaque entrée est structurée ainsi :

```
- [ ] Concept  — où il apparaît dans le jeu (fichier, ligne représentative)
```

Une case cochée `[x]` indiquera qu'un module de cours couvre ce concept.

---

## Module 1 — Fondamentaux du langage

### 1.1 Variables et types de base
- [ ] Déclaration et affectation de variables — `config.py` (GRILLE_TAILLE = 12)
- [ ] Types entiers (`int`) — `config.py` (NB_DRONES, BATTERIE_MAX…)
- [ ] Types flottants (`float`) — `config.py` (PROBA_PROPAGATION = 0.3)
- [ ] Chaînes de caractères (`str`) — `modeles.py` (etat = "en_attente")
- [ ] Booléens (`bool`) — `modeles.py` (hors_service = False)
- [ ] La valeur `None` — `modeles.py` (survivant = None)
- [ ] Constantes de module (convention MAJUSCULES) — `config.py`

### 1.2 Opérateurs
- [ ] Opérateurs arithmétiques (`+`, `-`, `*`, `/`, `//`, `%`) — `logique.py` (batterie -= nb)
- [ ] Opérateurs de comparaison (`==`, `!=`, `<`, `<=`, `>`, `>=`) — `logique.py` (valider_mouvement)
- [ ] Opérateurs logiques (`and`, `or`, `not`) — `logique.py` (valider_mouvement_tempete)
- [ ] Opérateur `in` / `not in` — `logique.py` (pos not in interdit)
- [ ] Opérateur de walrus `:=` (optionnel, niveau avancé)

### 1.3 Chaînes de caractères — opérations courantes
- [ ] Concaténation et f-strings — `modeles.py` (`__repr__`, `__str__`)
- [ ] Méthodes `.strip()`, `.upper()`, `.lower()` — `console.py` (parser_commande)
- [ ] Méthode `.isdigit()`, `.isalpha()` — `console.py` (parser_commande)
- [ ] Indexation d'une chaîne (`texte[0]`, `texte[1:]`) — `modeles.py` (depuis_chaine)
- [ ] `len()` sur une chaîne — `modeles.py` (depuis_chaine : `if len(texte) < 2`)
- [ ] `.index()` sur une liste/chaîne — `modeles.py` (LETTRES.index(lettre))
- [ ] Formatage avec `.rjust()`, `:<N`, `:>N`, `:02d` — `affichage.py`, `logique.py`

---

## Module 2 — Structures de contrôle

### 2.1 Conditions
- [ ] `if` / `elif` / `else` — `console.py` (parser_commande, phase_drones)
- [ ] Conditions imbriquées — `logique.py` (executer_mouvement)
- [ ] Expression ternaire `valeur_si_vrai if condition else valeur_si_faux` — `affichage.py`

### 2.2 Boucles
- [ ] Boucle `for` sur un itérable — `logique.py` (for i in range(NB_DRONES))
- [ ] Boucle `for` avec `range()` — `logique.py` (_mettre_a_jour_grille)
- [ ] Boucle `while` — `console.py` (while deplacements_restants > 0)
- [ ] Instructions `break` et `continue` — `console.py` (phase_drones)
- [ ] Boucle `for` avec `enumerate()` — non utilisé dans le jeu, mais utile à enseigner

### 2.3 Gestion des erreurs
- [ ] `try` / `except` — `modeles.py` (depuis_chaine : try int(texte[1:]))
- [ ] Exceptions spécifiques (`ValueError`, `OSError`, `KeyboardInterrupt`, `EOFError`) — `logger.py`, `console.py`
- [ ] Bloc `finally` (à enseigner même si peu présent dans le jeu)

---

## Module 3 — Fonctions

### 3.1 Définir et appeler une fonction
- [ ] Définition avec `def` — tous les fichiers
- [ ] Paramètres positionnels — `logique.py` (valider_mouvement)
- [ ] Paramètres avec valeur par défaut — `logique.py` (_position_aleatoire, max_tentatives=200)
- [ ] Valeur de retour `return` — `logique.py` (valider_mouvement → tuple)
- [ ] Retour de plusieurs valeurs (tuple) — `logique.py` (return False, "raison")
- [ ] Fonctions sans retour explicite (retournent `None`) — `logique.py` (appliquer_blocages)

### 3.2 Portée des variables
- [ ] Variable locale vs globale — `logger.py` (`global _fichier_ouvert`)
- [ ] Mot-clé `global` — `logger.py` (_ecrire_fichier)

### 3.3 Fonctions avancées
- [ ] Fonctions imbriquées (closures légères) — `logique.py` (def _cible_libre(pos) dans deplacer_tempetes)
- [ ] Annotations de type (`-> bool`, `-> str`, `: int`) — `modeles.py`, `logique.py`
- [ ] Chaîne de documentation `docstring` — tous les fichiers

---

## Module 4 — Structures de données

### 4.1 Listes
- [ ] Création et accès par index — `modeles.py` (LETTRES, cases)
- [ ] List comprehension — `modeles.py` (voisins_ortho, cases = [['.' for _ …] for _ …])
- [ ] `.append()` — `logique.py` (etat.batiments.append(bat))
- [ ] `len()` — `affichage.py` (len(col1))
- [ ] Itération sur une liste — `logique.py` (for drone in etat.drones)
- [ ] Slicing (`liste[-n:]`) — `affichage.py` (historique[-(max(1, nb_lignes - 1)):])
- [ ] `list()` appliqué à un itérable — `modeles.py` (list("ABCDEFGHIJKL"))

### 4.2 Tuples
- [ ] Création et déballage (`dc, dl = tempete.direction`) — `logique.py`
- [ ] Tuple comme valeur de retour — `logique.py` (return True, "")
- [ ] Tuple comme clé de `set` ou `dict` — `modeles.py` (`__hash__` : hash((col, lig)))

### 4.3 Dictionnaires
- [ ] Création avec `{}` — `affichage.py` (_C = { 'D': '\033[94m', … })
- [ ] Accès à une valeur (`dict[cle]`) — `affichage.py` (_C.get(sym, ''))
- [ ] Méthode `.get()` avec valeur par défaut — `affichage.py`
- [ ] Itération sur un dictionnaire — `console.py` (drones_bouge = {d.identifiant: False …})

### 4.4 Ensembles (sets)
- [ ] Création avec `set()` — `logique.py` (occupees: set = set())
- [ ] Opérateur `|` (union) — `logique.py` (interdit = (interdites or set()) | occupees)
- [ ] `.add()` — `logique.py` (etat.zones_x.add(pos))
- [ ] Test d'appartenance avec `in` — `logique.py` (if pos not in interdit)
- [ ] Itération sur un set — `logique.py` (for zone_x in list(etat.zones_x))

---

## Module 5 — Programmation Orientée Objet (POO)

### 5.1 Classes et instances
- [ ] Définition d'une classe avec `class` — `modeles.py` (class Position, Drone, etc.)
- [ ] Constructeur `__init__` — `modeles.py` (toutes les classes)
- [ ] Attributs d'instance (`self.x`) — `modeles.py`
- [ ] Attributs de classe (partagés) — `modeles.py` (Position.LETTRES, Tempete._DIRECTIONS)
- [ ] Méthodes d'instance — `modeles.py` (est_actif, consommer_batterie…)

### 5.2 Méthodes spéciales (dunder methods)
- [ ] `__str__` — `modeles.py` (Position.__str__)
- [ ] `__repr__` — `modeles.py` (Position.__repr__, Drone.__repr__)
- [ ] `__eq__` — `modeles.py` (Position.__eq__)
- [ ] `__hash__` — `modeles.py` (Position.__hash__)

### 5.3 Méthodes de classe
- [ ] `@classmethod` et `cls` — `modeles.py` (Position.depuis_chaine)

### 5.4 Héritage et isinstance
- [ ] `isinstance()` — `modeles.py` (Position.__eq__ : if not isinstance(autre, Position))
- [ ] Héritage (notion, même si le jeu n'en fait pas un usage extensif)

### 5.5 Annotations de type en POO
- [ ] Annotation de type pour les paramètres de méthode — `modeles.py` (def __init__(self, col: int, lig: int))
- [ ] Références circulaires dans les annotations (`"Position"` entre guillemets) — `modeles.py` (distance_chebyshev)
- [ ] Union de types (`Drone | None`) — `modeles.py`, `logique.py`

---

## Module 6 — Modules et organisation du code

### 6.1 Import de modules
- [ ] `import module` — `main.py` (import random)
- [ ] `from module import symbole` — tous les fichiers (from modeles import EtatJeu…)
- [ ] Import dans un bloc conditionnel — `main.py` (if args.seed is not None: import random)

### 6.2 Modules standards utilisés dans le jeu
- [ ] `random` : `random.randint()`, `random.choice()`, `random.random()`, `random.seed()` — `logique.py`, `main.py`
- [ ] `os` : `os.path.dirname()` — `main.py`
- [ ] `sys` : `sys.path.insert()`, `sys.exit()` — `main.py`
- [ ] `argparse` : `ArgumentParser`, `add_argument`, `parse_args` — `main.py`
- [ ] `shutil` : `shutil.get_terminal_size()` — `affichage.py`
- [ ] `re` : `re.sub()` et expressions régulières (basique) — `affichage.py` (_strip_ansi)

### 6.3 Structure d'un projet multi-fichiers
- [ ] Point d'entrée `if __name__ == '__main__':` — `main.py`
- [ ] Séparation des responsabilités (config / modèles / logique / affichage / console / logger)
- [ ] Manipulation du `sys.path` pour les imports locaux — `main.py`

---

## Module 7 — Entrées / Sorties

### 7.1 Entrées utilisateur
- [ ] `input()` — `console.py` (_prompt)
- [ ] Gestion de `EOFError` et `KeyboardInterrupt` lors d'un `input()` — `console.py`

### 7.2 Affichage console
- [ ] `print()` et paramètres `end=`, `flush=` — `console.py`, `affichage.py`
- [ ] Codes d'échappement ANSI (couleurs, effacement écran) — `affichage.py` (_C dict, \033[2J\033[H)

### 7.3 Fichiers
- [ ] Ouverture d'un fichier avec `open()` en mode écriture — `logger.py`
- [ ] Encodage `encoding='utf-8'` — `logger.py`
- [ ] Écriture avec `.write()` et `.flush()` — `logger.py`
- [ ] Fermeture avec `.close()` — `logger.py` (fermer_log)
- [ ] Gestionnaire de contexte `with open(...) as f:` — `logger.py` (sauvegarder_log)
- [ ] Gestion des erreurs disque (`OSError`) — `logger.py`

---

## Module 8 — Algorithmique et logique de jeu

### 8.1 Algorithmes de base
- [ ] Recherche dans une liste (boucle + condition de retour) — `modeles.py` (drone_par_id)
- [ ] Génération de positions aléatoires avec contraintes — `logique.py` (_position_aleatoire)
- [ ] Distance de Chebyshev (max des différences absolues) — `modeles.py` (distance_chebyshev)
- [ ] Propagation sur une grille (voisins orthogonaux) — `logique.py` (propager_zones_x)
- [ ] Rebond sur les bords (IA de déplacement) — `logique.py` (deplacer_tempetes)

### 8.2 Modélisation avec des classes
- [ ] Représenter un état de jeu complet dans un objet — `modeles.py` (EtatJeu)
- [ ] Grille 2D modélisée par une liste de listes — `modeles.py` (Grille.cases)
- [ ] Coordonnées sur une grille (colonne / ligne, indexation 0-based) — `modeles.py` (Position)

### 8.3 Boucle de jeu
- [ ] Architecture boucle principale + phases — `main.py` / `console.py` (boucle_principale, boucle_saisie)
- [ ] Séparation de la logique et de l'affichage — `logique.py` vs `affichage.py`
- [ ] Pattern commande : parser → valider → exécuter — `console.py` (parser_commande + valider_mouvement + executer_mouvement)

---

## Module 9 — Bonnes pratiques et style

- [ ] Convention de nommage PEP 8 (snake_case, MAJUSCULES pour constantes)
- [ ] Commentaires et docstrings (quand et comment les écrire)
- [ ] Découpage en fonctions courtes et réutilisables
- [ ] Variables de configuration centralisées dans un fichier dédié
- [ ] Eviter les valeurs "magiques" (magic numbers) — remplacer par des constantes nommées
- [ ] Ne pas dupliquer le code (DRY — Don't Repeat Yourself)

---

## Récapitulatif par fichier du jeu

| Fichier         | Concepts clés mis en œuvre |
|-----------------|----------------------------|
| `config.py`     | Variables, constantes, types de base |
| `modeles.py`    | Classes, `__init__`, méthodes spéciales, `@classmethod`, annotations, sets, listes |
| `logique.py`    | Fonctions, tuples de retour, aléatoire, sets, boucles, conditions, imports |
| `affichage.py`  | Chaînes, f-strings, formatage, ANSI, `shutil`, listes de listes, `re` |
| `console.py`    | `input()`, boucle `while`, `break`/`continue`, dictionnaires, pattern commande |
| `logger.py`     | Fichiers, `open`/`write`/`flush`, `with`, variable globale, gestion d'erreurs |
| `main.py`       | `argparse`, `sys`, `os`, `if __name__`, imports conditionnels, fonctions orchestratrices |

---

*Référentiel généré le 2026-03-30 — à mettre à jour si le code du jeu évolue.*
