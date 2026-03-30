# Module 04 — Modules, I/O fichiers et JSON

> **Fil rouge :** `config.py` lit `config.json` au démarrage, `logger.py` écrit
> `partie.log` et `resultats.txt`. À la fin de ce module, tu sauras importer
> des modules, lire/écrire des fichiers texte et charger un fichier JSON.

---

## 1. Importer un module

Python fournit de nombreuses bibliothèques prêtes à l'emploi :

```python
import random     # génération aléatoire
import json       # lire/écrire du JSON
import os         # interaction avec le système d'exploitation
```

On peut aussi n'importer qu'une fonction spécifique :

```python
from random import choice, randint, sample
```

Dans le jeu, `random` est utilisé pour le placement initial et la phase météo :

```python
import random

# Placer des entités aléatoirement
positions = random.sample(cases_libres, nb_drones)

# Phase météo : la tempête bouge avec 50% de chance
if random.random() > 0.5:
    deplacer_tempete(tempete)
```

> 💡 `random.seed(42)` fixe l'aléatoire : même seed = même partie. Utile pour tester.

---

## 2. Lire et écrire des fichiers texte

### Ouvrir avec `with open()`

```python
# Écrire (crée ou écrase)
with open("partie.log", "w", encoding="utf-8") as f:
    f.write("=== Début de partie ===\n")

# Ajouter à la fin (append)
with open("partie.log", "a", encoding="utf-8") as f:
    f.write("T01  D1  A0→B0  bat:10→8\n")

# Lire tout le contenu
with open("partie.log", "r", encoding="utf-8") as f:
    contenu = f.read()
```

`with ... as f` garantit que le fichier est fermé même si une erreur survient.
C'est la façon standard — ne jamais utiliser `f = open(...)` sans `with`.

### Les 3 modes essentiels

| Mode | Signification | Utilisation |
|------|--------------|-------------|
| `"w"` | write — écrase | Démarrer un log, écrire les résultats |
| `"a"` | append — ajoute | Chaque événement de jeu |
| `"r"` | read — lit | Relire un log, charger une config |

---

## 3. Lire un fichier JSON

Le fichier `config.json` contient tous les paramètres du jeu :

```json
{
  "GRILLE_TAILLE": 8,
  "NB_DRONES": 6,
  "BATTERIE_MAX": 20,
  "HOPITAL_COL": 0,
  "HOPITAL_LIG": 7
}
```

Pour le lire en Python :

```python
import json

def charger_config(chemin="config.json"):
    """Lit le fichier JSON et retourne un dictionnaire."""
    with open(chemin, "r", encoding="utf-8") as f:
        return json.load(f)   # retourne un dict Python

config = charger_config()
print(config["GRILLE_TAILLE"])   # 8
print(config["NB_DRONES"])       # 6
```

- `json.load(f)` : lit le fichier et convertit automatiquement en `dict` Python
- Les clés JSON deviennent des clés de dictionnaire
- Les `true`/`false` JSON deviennent `True`/`False` Python
- Les `null` JSON deviennent `None` Python

> 💡 `json.load(f)` = lire depuis un fichier ouvert. `json.loads(chaine)` = lire depuis une chaîne.

---

## 4. Gérer les fichiers absents avec `try/except`

Si le fichier `config.json` n'existe pas, Python lève une `FileNotFoundError`.
On la capture avec `try/except` :

```python
def charger_config(chemin="config.json"):
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Fichier '{chemin}' introuvable.")
        return {}   # config vide par défaut
```

Ici, `except FileNotFoundError` ne capture que ce type d'erreur précis.
C'est une bonne pratique : ne pas capturer toutes les erreurs en même temps.

---

## 5. Créer ses propres modules (#51)

Un module Python, c'est simplement un fichier `.py` que tu importes depuis un autre.

### Questions à se poser avant de créer un nouveau fichier

1. **Est-ce un groupe de fonctions liées ?** (ex: toutes les fonctions de logique)
2. **D'autres fichiers en ont-ils besoin ?** (ex: `affichage.py` a besoin de `logique.py`)
3. **Est-ce réutilisable indépendamment ?** (ex: `logger.py` peut fonctionner seul)

Si oui à au moins deux : c'est un bon candidat pour un module séparé.

```
jeu/
  config.py    ← lit config.json
  logique.py   ← règles du jeu
  affichage.py ← rendu console
  console.py   ← saisie joueur
  logger.py    ← écriture fichiers
  main.py      ← point d'entrée
```

```python
# Dans console.py
from logique import valider_mouvement, executer_mouvement
from affichage import afficher_jeu
from logger import enregistrer_log
```

**Règle d'or** : `main.py` et `console.py` peuvent importer les autres,
mais les autres ne doivent jamais importer `console.py` ou `main.py`.
Cela évite les dépendances circulaires.

---

## 6. `if __name__ == '__main__'` (#50)

Cette ligne permet d'exécuter du code uniquement quand le fichier est
**lancé directement**, pas quand il est importé.

```python
# logique.py

def distance_chebyshev(col1, lig1, col2, lig2):
    return max(abs(col2 - col1), abs(lig2 - lig1))

# Ce bloc ne s'exécute QUE si on fait : python logique.py
if __name__ == '__main__':
    print(distance_chebyshev(0, 0, 1, 1))   # test rapide : affiche 1
```

Quand `console.py` fait `from logique import distance_chebyshev`,
le bloc `if __name__ == '__main__'` n'est **pas** exécuté.

Utilisations courantes :
- Tests rapides d'un module seul
- Point d'entrée de `main.py`

---

## 7. Exercice A — Lire une config JSON

```python
# Crée un fichier config_test.json avec ce contenu :
# {"taille": 8, "nb_drones": 3, "batterie_max": 20}

import json

with open("config_test.json", "r", encoding="utf-8") as f:
    config = json.load(f)

print(config["taille"])       # 8
print(config["nb_drones"])    # 3
print(config["batterie_max"]) # 20
```

---

## 8. Exercice B — Écrire et lire un log

```python
# Étapes :
# 1. Créer le fichier log avec l'en-tête
# 2. Ajouter 3 lignes d'événements
# 3. Lire et afficher le contenu

with open("test.log", "w", encoding="utf-8") as f:
    f.write("=== Journal de test ===\n")

for i in range(1, 4):
    with open("test.log", "a", encoding="utf-8") as f:
        f.write(f"T0{i}  événement {i}\n")

with open("test.log", "r", encoding="utf-8") as f:
    print(f.read())
```

---

## Erreurs classiques

**Erreur 1 — Oublier `with` → fichier non fermé**
```python
# ❌ Si une erreur survient, le fichier reste bloqué
f = open("partie.log", "w")
f.write("Tour 1")
f.close()   # peut ne jamais être appelé si exception

# ✅
with open("partie.log", "w", encoding="utf-8") as f:
    f.write("Tour 1")
```

**Erreur 2 — Mode `"w"` au lieu de `"a"` pour un log**
```python
# ❌ Écrase tout à chaque événement
with open("partie.log", "w") as f:
    f.write(f"T{tour}\n")

# ✅ Ajoute en fin de fichier
with open("partie.log", "a", encoding="utf-8") as f:
    f.write(f"T{tour}\n")
```

**Erreur 3 — `FileNotFoundError` non gérée**
```python
# ❌ Plante si le fichier n'existe pas
with open("config.json", "r") as f:
    config = json.load(f)

# ✅
try:
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    config = {}   # valeurs par défaut
```

---

## Résumé des points clés

| Concept | Exemple | À retenir |
|---------|---------|----------|
| Importer | `import json` | En haut du fichier |
| Lire JSON | `json.load(f)` | Retourne un dict |
| Écrire fichier | `open("f", "w")` | Écrase |
| Ajouter | `open("f", "a")` | Préserve |
| Fichier absent | `except FileNotFoundError` | Toujours gérer |
| Module séparé | `from logique import f` | Import ciblé |
| Test d'un module | `if __name__ == '__main__'` | Pas exécuté à l'import |

---

## Exercices du module

Voir `exercices/ex_04_io.py`

## Prompts IA utiles

> *« Comment lire un fichier JSON en Python et accéder à ses valeurs ? »*

> *« Quelle est la différence entre les modes `'w'` et `'a'` dans `open()` en Python ? »*

> *« À quoi sert `if __name__ == '__main__'` en Python ? »*
