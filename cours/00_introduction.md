# Module 00 — Introduction au projet

## Bienvenue dans Drone Rescue !

Ce cours t'apprend Python en construisant **Drone Rescue**, un jeu de simulation jouable dans le terminal.
Tu vas progressivement écrire chaque brique du jeu, de la gestion des données à l'interface console.

> 🎮 **Le principe du jeu** : J1 déplace des drones de secours pour sauver des survivants.
> J2 déplace des tempêtes pour bloquer les drones. Qui gagne en 20 tours ?

---

## Ce que tu vas construire

```
     A   B   C   D   E   F   G   H   I   J
  1  .   .   B   .   .   S   .   .   .   B
  2  .   D   .   .   .   .   .   S   .   T
  3  .   .   .   B   .   .   .   .   .   .
  4  .   .   .   .   T   .   .   .   X   .
  5  H   .   S   .   .   .   D   .   .   .
  6  .   .   .   .   .   .   .   B   .   .
  7  .   X   .   .   .   S   .   .   .   .
  8  .   .   .   D   .   .   .   .   T   .
  9  .   .   B   .   .   .   .   .   .   S
 10  .   .   .   .   .   .   .   .   .   .

 Légende : . vide  B bâtiment  H hôpital
            S survivant  D drone  T tempête  X zone dangereuse
```

Les joueurs pilotent les drones via une console textuelle, tour par tour.

---

## Plan du cours (9 modules)

| Semaine | Modules | Thème | Ce que tu codes |
|---------|---------|-------|-----------------|
| 1 | 01 + 02 | Structures, boucles | Listes, dicts, `for`, `while`, `if` |
| 2 | 03 + 04 | Fonctions, fichiers | `def`, `return`, `import`, `open()` |
| 3 | 05 + 06 | Dicts avancés, grille | Entités du jeu, affichage ASCII |
| 4 | 07 | Logique de jeu | Validation mouvements, coûts, fin de partie |
| 5 | 08 | Console et logs | Saisie joueur, journalisation fichier |
| 6 | 09 | Assemblage final | Jeu complet jouable |

---

## Structure du repo

```
drone-rescue-python/
├── cours/          ← Tu es ici : fiches de cours .md (01 → 09)
├── notebooks/      ← Notebooks Google Colab interactifs (nb_01 → nb_09)
├── exercices/      ← Fichiers .py à compléter (ex_01 → ex_09)
├── corrections/    ← Solutions (ouvrir après avoir essayé !)
└── jeu/            ← Le jeu complet (ne pas modifier)
    ├── main.py       ← Point d'entrée : python main.py
    ├── logique.py
    ├── affichage.py
    ├── console.py
    ├── logger.py
    └── config.py
```

---

## Par où commencer ?

### Option A — Google Colab (recommandée, zéro installation)

Google Colab te permet d'exécuter du code Python directement dans ton navigateur, sans rien installer.

1. Va dans le dossier [`notebooks/`](../notebooks/) du repo
2. Ouvre le fichier `nb_01_structures.ipynb`
3. En haut de la page GitHub, clique sur le bouton **« Open in Colab »**
   *(ou va sur [colab.research.google.com](https://colab.research.google.com) → Fichier → Importer un notebook → GitHub)*
4. Exécute les cellules dans l'ordre avec **Shift+Entrée**
5. Complète les exercices directement dans le notebook

> 💡 **Le notebook de chaque module contient** : la théorie, des exemples exécutables, les exercices et les solutions cachées (cellules `solution`).

### Option B — VS Code en local

```bash
# 1. Clone le repo
git clone https://github.com/stefm78/drone-rescue-python
cd drone-rescue-python

# 2. Lance le jeu pour voir ce que tu vas construire
python jeu/main.py

# 3. Commence par le module 01
# Lis : cours/01_structures_de_base.md
# Code : exercices/ex_01.py
```

**Prérequis locaux :**
- Python 3.10+
- VS Code avec l'extension Python
- Un terminal (PowerShell, bash, zsh)

---

## Progression recommandée pour chaque module

```
┌─────────────────────────────────────────────┐
│  1️⃣ Lis la fiche cours/XX_...md                   │
│  2️⃣ Ouvre et joue avec notebooks/nb_XX_...ipynb   │
│  3️⃣ Complète exercices/ex_XX.py (squelette à toi) │
│  4️⃣ Compare avec corrections/corr_XX.py           │
│  5️⃣ Passe au module suivant                       │
└─────────────────────────────────────────────┘
```

---

## Les notebooks en détail

Chaque notebook Google Colab du dossier `notebooks/` suit la même structure en 8 cellules :

| Cellule | Contenu |
|---------|---------|
| 1 | En-tête du module |
| 2 | Concepts clés (théorie + exemples) |
| 3 | Exemples interactifs à modifier |
| 4 | Lien avec Drone Rescue |
| 5 | Exemple concret tiré du jeu |
| 6 | À toi de jouer (exercice A) |
| 7 | Squelette de code à compléter |
| 8 | Solution (cellule cachée — tag `solution`) |

> ⚠️ N'ouvre la cellule `solution` qu'après avoir essayé toi-même !

---

## Convention de coordonnées

Tu verras souvent des notations du type **`B3`** dans les exercices.
Cela signifie : colonne B (= 2e colonne), ligne 3.

```
Grille (10×10) :

      A   B   C   D   E  ...  J
  1   .   .   .   .   .       .
  2   .   .   .   .   .       .
  3   .  B3   .   .   .       .
  ...
```

> En Python interne : `B3` → `col=1, lig=2` (0-based). La conversion est gérée automatiquement par le jeu.

---

## Prérequis

- Quelques notions de Python (variables, boucles, fonctions basiques) ✓
- Pour Colab : un compte Google
- Pour local : Python 3.10+, VS Code, un terminal

---

## Prompts IA utiles pour ce module

> *« Je débute en Python et je veux comprendre la structure générale d'un projet Python avec plusieurs fichiers. Explique-moi comment les fichiers s'importent entre eux. »*

> *« Qu'est-ce qu'un notebook Jupyter / Google Colab ? Comment exécuter une cellule de code ? »*

> *« Explique-moi comment fonctionne un jeu au tour par tour en Python, en gardant l'état du jeu dans des dictionnaires. »*
