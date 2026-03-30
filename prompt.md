# Prompt de reprise — drone-rescue-python

Colle ce prompt dans n'importe quelle IA pour reprendre le projet sans perte d'information.

---

```
## Contexte — projet drone-rescue-python

Tu reprends un projet pédagogique Python entièrement spécifié et partiellement réalisé.
Voici ce qui a été décidé et codé — respecte-le scrupuleusement.

---

### Objectif
Créer le repo GitHub `drone-rescue-python` (public) contenant :
1. Un cours Python en 9 modules + annexes (cours/)
2. Des exercices avec énoncés séparés des corrections (exercices/ + corrections/)
3. Le jeu jouable en console Python (jeu/)

---

### Profil apprenant
- Débutant en Python
- Connaît : variables, structures de base, for/while, if, fonctions simples
- Pas d'expérience en I/O fichiers, modules, classes
- Travaille seul, deadline dans 6 semaines

---

### Branche de travail
`refonte/dicts-regles-officiel` — merge dans `main` uniquement quand tout est validé.
Ne jamais pousser directement sur `main`.

---

### Décisions architecturales clés (DÉFINITIVES)

1. **Pas de POO** : `modeles.py` est supprimé. Toutes les entités sont des **dictionnaires**.
2. **config.json** : tous les paramètres sont dans un fichier JSON externe lu par `config.py`.
3. **Pas d'argparse** : `main.py` lance le jeu directement, sans arguments CLI.
4. **Pas de codes ANSI** : `affichage.py` utilise uniquement `print()` et le formatage de chaînes.
5. **Pas de `re`** : le parsing des commandes utilise des opérations de chaîne simples.
6. **2 joueurs humains** : J1 pilote les drones, J2 pilote les tempêtes.

---

### Structure du repo (state actuel ✅)

```
drone-rescue-python/
├── README.md
├── CHANTIER_CODE.md          ← suivi du chantier (phases 1-7 terminées)
├── REFERENTIEL_ENSEIGNEMENTS.md
├── prompt.md                  ← ce fichier
├── cours/
│   ├── 00_introduction.md
│   ├── 01_structures_de_base.md
│   ├── 02_boucles_et_conditions.md
│   ├── 03_fonctions.md
│   ├── 04_modules_et_io.md
│   ├── 05_dictionnaires_avances.md    ← remplace 05_classes_et_objets.md
│   ├── 06_grille_et_affichage.md
│   ├── 07_logique_de_jeu.md
│   ├── 08_console_et_log.md
│   ├── 09_assemblage_final.md
│   └── annexe_formatage.md            ← f-strings avancés
├── exercices/
│   ├── ex_01_structures.py
│   ├── ex_02_boucles.py
│   ├── ex_03_fonctions.py
│   ├── ex_04_io.py
│   ├── ex_05_dicts_avances.py         ← remplace ex_05_classes.py
│   ├── ex_06_grille.py
│   ├── ex_07_logique.py
│   └── ex_08_console.py
├── corrections/
│   └── corr_0X_*.py  (un par module)
└── jeu/
    ├── config.json      ← source de vérité de tous les paramètres
    ├── config.py        ← lit config.json, expose les constantes
    ├── logique.py       ← creer_*() + toutes les règles
    ├── affichage.py     ← rendu console, sans ANSI
    ├── console.py       ← boucle de jeu, 2 joueurs
    ├── logger.py        ← partie.log + resultats.txt
    └── main.py          ← point d'entrée, sans argparse
```

---

### Structure des entités (dictionnaires)

```python
# Drone
drone = {
    "id"          : "D1",
    "col"         : 0,           # int, 0-basé
    "lig"         : 5,           # int, 0-basé
    "batterie"    : 10,
    "batterie_max": 20,
    "survivant"   : None,        # None ou "S1"
    "bloque"      : 0,           # nb tours bloqué
    "hors_service": False,
    "dx"          : 0,           # direction (rebond)
    "dy"          : 0,
}

# Survivant
survivant = {
    "id"  : "S1",
    "col" : 3,
    "lig" : 7,
    "etat": "en_attente",    # en_attente | embarque | sauve
}

# Tempête
tempete = {
    "id" : "T1",
    "col": 8,
    "lig": 3,
    "dx" : 1,
    "dy" : 1,
}

# Zones dangereuses : set de tuples
zones_x = {(3, 5), (7, 8)}

# État global
etat = {
    "tour"        : 1,
    "score"       : 0,
    "partie_finie": False,
    "victoire"    : False,
    "grille"      : [['.'] * TAILLE for _ in range(TAILLE)],
    "hopital"     : (0, 7),
    "batiments"   : [(2, 3), (5, 1)],   # liste de tuples
    "drones"      : {"D1": {...}, ...},
    "tempetes"    : {"T1": {...}, ...},
    "survivants"  : {"S1": {...}, ...},
    "zones_x"     : {(3, 5), (7, 8)},
    "historique"  : [],
}
```

---

### Règles officielles du jeu (`Projet_Drones_G4.pdf`)

| Règle | Valeur |
|-------|--------|
| Déplacements J1 par tour | 3 max (1 par drone) |
| Déplacements J2 par tour | 2 max (1 par tempête) |
| Coût déplacement seul | −1 batterie |
| Coût avec survivant embarqué | −2 batterie |
| Supplément zone X | −2 batterie |
| Recharge hôpital | +3 par tour sur place |
| Blocage tempête | 2 tours |
| Propagation zones X | tous les 3 tours, 30% |
| Phase météo | 50% de chance/tempête |
| Fin partie victoire | Tous les survivants "sauve" |
| Fin partie défaite | Tours max atteint OU tous drones HS |

---

### Contenu attendu pour chaque fichier

**Cours `cours/0X_*.md`**
- Explication niveau débutant
- Lien explicite avec le jeu (exemple du code réel)
- Erreurs classiques encadrées
- Résumé tableau en fin
- Prompts IA prêts à copier
- Référence aux exercices correspondants

**Exercices `exercices/ex_0X_*.py`**
- Énoncés en commentaires
- Squelettes de fonctions à compléter
- Tests avec `print()` ou `assert` en bas du fichier

**Corrections `corrections/corr_0X_*.py`**
- Code complet et fonctionnel
- Commentaires pédagogiques

---

### État d'avancement

| Élément | Statut |
|---------|--------|
| Code `jeu/` (phases 1-7) | ✅ Terminé |
| Cours 00 à 09 + annexe formatage | ✅ Terminé |
| `REFERENTIEL_ENSEIGNEMENTS.md` | ✅ Mis à jour |
| `CHANTIER_CODE.md` | ✅ Mis à jour |
| `prompt.md` | ✅ Ce fichier |
| Exercices `exercices/` | ⬜ À créer (ex_05 à renommer + ex_05 dicts) |
| Corrections `corrections/` | ⬜ À créer |
| Merge `refonte/dicts-regles-officiel` → `main` | ⬜ Dernière étape |

---

### Comment reprendre
1. Lire `CHANTIER_CODE.md` (tableau des phases, état actuel)
2. Lire ce fichier `prompt.md` pour le contexte complet
3. Travailler uniquement sur `refonte/dicts-regles-officiel`
4. Ne merger dans `main` qu'une fois exercices + corrections terminés

```
