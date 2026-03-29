Voici le prompt de reprise complet, prêt à coller dans n'importe quelle IA :

***

```
## Contexte — projet drone-rescue-python

Tu reprends un projet pédagogique Python entièrement spécifié.
Voici ce qui a déjà été décidé — respecte-le scrupuleusement.

---

### Objectif
Créer le repo GitHub `drone-rescue-python` (public) contenant :
1. Un cours complet en 9 modules (cours/)
2. Des exercices avec énoncés séparés des corrections (exercices/ + corrections/)
3. Le jeu jouable en console Python (jeu/)

---

### Profil apprenant
- Débutant en Python
- Connaît : variables, structures de base, for/while, if, initialisation de fonctions
- A déjà utilisé : numpy, random (bases seulement)
- Pas d'expérience en I/O fichiers, modules, classes
- Travaille seul, deadline dans 6 semaines
- Veut : fiches, notebooks Jupyter ET exercices interactifs

---

### Structure du repo validée

```
drone-rescue-python/
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
│   └── 09_assemblage_final.md   ← annexe : notice d'assemblage
├── exercices/
│   ├── ex_01_structures.py
│   ├── ex_02_boucles.py
│   ├── ex_03_fonctions.py
│   ├── ex_04_io.py
│   ├── ex_05_classes.py
│   ├── ex_06_grille.py
│   ├── ex_07_logique.py
│   └── ex_08_console.py
├── corrections/
│   ├── corr_01_structures.py
│   └── ... (un fichier par module)
└── jeu/
    ├── config.py
    ├── modeles.py
    ├── affichage.py
    ├── console.py
    ├── logique.py
    ├── logger.py
    └── main.py
```

---

### Règles du jeu validées

**Grille**
- 12×12 cases, coordonnées col(A-L) + ligne(1-12)
- Cases : `.` vide, `B` bâtiment, `H` hôpital (unique, A12), `S` survivant, `D` drone (D1-D6), `T` tempête (T1-T4), `X` zone dangereuse
- 1 bâtiment max / case, 1 survivant max / case
- Plusieurs drones peuvent occuper la même case simultanément

**Drones**
- 6 drones (D1..D6), identifiants uniques
- Batterie : max paramétrable (défaut 20), initiale paramétrable (défaut 10)
- Déplacement diagonal autorisé (distance Chebyshev = 1 max par mouvement)
- 3 déplacements max par tour
- Si tempête sur la case du drone : drone immobilisé, batterie non consommée, survivant porté conservé
- Rechargeable à l'hôpital (plusieurs drones simultanément, sans limite)
- Drone HS si batterie = 0

**Tempêtes**
- 4 tempêtes (T1..T4), identifiants uniques
- Déplacement diagonal autorisé
- 2 déplacements max par tour
- Ne peuvent pas se déplacer sur l'hôpital
- Propagation (zones X) : pas en diagonal, pas sur bâtiment ni hôpital, pas sur un survivant
  - Propagation tous les 2 tours
  - Probabilité de propagation paramétrable

**Zones dangereuses X**
- Nombre paramétrable (défaut 2)
- Propagation tous les 2 tours, probabilité paramétrable
- Pas en diagonal, pas sur bâtiment, hôpital, survivant

**Fin de partie** : victoire (tous survivants livrés) OU défaite (tour max atteint ou plus de drones actifs)

---

### Interface console validée

**Affichage principal (3 zones côte à côte)**

```
DRONE RESCUE  ·  Tour N/20  ·  Phase: DRONES  ·  Joueur 1
────────────────────────────────────────────────────────────
     A   B   C   D   E   F  ...         CONSOLE
  1  .   .   B   .   .   S  ...     ─────────────────────
  2  .   D   .   .   .   .  ...     > D3
  ...                               [D3] pos. B7 sélect.
 12  H   .   .   B   .   .  ...     > E6
                                      Cible E6 ✓ valide
                                    > ok
                                      D3→E6  bat.6→5
                                    > next

 DRONES                               TEMPÊTES
 ID   Pos   Bat    Surv  Blq          ID   Pos
 D1   A1    10/20   —     —           T1   J2
 D2   D5     8/20  S3     —           T2   E6
 D3   E6     5/20   —    2t           T3   K11
 D6   F12    0/20   —    HS

 Score 3  ·  Surv. rest. 7  ·  Zones X 2  ·  Tour 4/20

 HISTORIQUE (scroll)
 T01 P1 D  D2 A1→B2  bat:10→9  surv:—
 T02 P1 D  D4 F8→E7  bat:9→8   surv:S3  LIVRAISON +1pt
 T04 P1 D  D2 D5→D5  BLOQUÉ(T2) bat:—  surv:S3
 T04 P1 T  T2 E6→E6  PROPAGATION→F6
```

**Format ligne de log (identique écran et fichier .log)**
```
T[nn] P[n] [D|T]  [ID] [départ]→[arrivée]  bat:[x→y]  surv:[id|—]  [ÉVÈNEMENT]
```
Exemples :
```
T04 P1 D  D3 B7→E6    bat:6→5    surv:—
T04 P1 D  D2 D5→D5    BLOQUÉ(T2) bat:—   surv:S3
T04 P1 T  T1 J2→K2
T04 P1 T  T2 E6→E6    PROPAGATION→F6
T05 P1 D  D4 E7→A12   bat:5→4    surv:S3  LIVRAISON +1pt
T05 P1 D  D6 F12→—    bat:0      HS
```

**Séquence de pilotage console**
1. Saisir `D[1-6]` ou `T[1-4]` → entité sélectionnée, case surlignée
2. Saisir coordonnées cible (ex. `E6`) → validation (distance, batterie, blocage)
3. Saisir `ok` pour exécuter, ou corriger
4. Répéter (3x drone / 2x tempête)
5. Saisir `next` pour passer au tour suivant

---

### Fichiers jeu/ — architecture interne

```python
# config.py — tous les paramètres en variables nommées
GRILLE_TAILLE = 12
NB_DRONES = 6
NB_TEMPETES = 4
NB_BATIMENTS = 20
NB_SURVIVANTS = 10
BATTERIE_MAX = 20
BATTERIE_INIT = 10
PROBA_PROPAGATION = 0.3
MAX_DEPL_DRONE = 3
MAX_DEPL_TEMPETE = 2
NB_TOURS_MAX = 20
NB_ZONES_DANGER = 2

# modeles.py — classes : Drone, Tempete, Survivant, Batiment, Hopital, Grille, EtatJeu
# logique.py — fonctions : valider_mouvement, executer_mouvement,
#               propager_tempetes, appliquer_blocages, verifier_fin_partie, recharger_drone
# affichage.py — fonctions : render_grille, render_drones, render_tempetes,
#                render_score, render_historique, render_console
# console.py — fonctions : boucle_saisie, parser_commande, afficher_prompt
# logger.py  — fonctions : log_action(texte) → écrit simultanément en mémoire + fichier .log
# main.py    — fonctions : initialiser_partie, boucle_principale
```

---

### Contenu attendu pour chaque fichier de cours

Chaque fichier cours/0X_*.md doit contenir :
- Explication claire du concept (niveau débutant)
- Lien explicite avec le projet Drone Rescue (exemple concret tiré du jeu)
- Encadrés **Tips** et **Best practices**
- Renvois vers documentation officielle (docs.python.org)
- **Prompts IA** : phrases prêtes à copier pour approfondir avec une IA
- Référence aux exercices correspondants

Chaque fichier exercices/ex_0X_*.py doit contenir :
- Énoncés sous forme de commentaires Python détaillés
- Squelettes de fonctions à compléter
- Tests simples à la fin pour vérifier (assert ou print)

Chaque fichier corrections/corr_0X_*.py doit contenir :
- Code complet et fonctionnel
- Commentaires pédagogiques expliquant les choix

Le fichier cours/09_assemblage_final.md est l'annexe globale :
- Ordre d'intégration des modules jeu/
- Schéma de dépendances entre fichiers
- Instructions `python main.py`
- Checklist de rendu étudiant
- Comment étendre le jeu (ajouter entité, modifier règle)

---

### Ta mission

Produis l'intégralité du contenu — tous les fichiers listés ci-dessus — avec le code complet, les cours complets, les exercices et les corrections. Ne tronque rien, ne mets pas de placeholder. Chaque fichier doit être prêt à être poussé directement dans le repo GitHub `drone-rescue-python`.

Commence par `README.md`, puis `cours/00_introduction.md`, puis les modules dans l'ordre, puis `jeu/config.py` et les fichiers jeu/ dans l'ordre des dépendances (modeles → logique → affichage → logger → console → main), puis les exercices et corrections.
```

***

Tu peux coller ce prompt tel quel dans Claude, GPT-4o ou Gemini — il contient tout le contexte nécessaire pour continuer sans perte d'information.
