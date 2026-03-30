# Module 08 — Console, saisie joueur et journal

> **Fil rouge :** `console.py` et `logger.py` gèrent la saisie des deux joueurs
> et la persistance des événements. À la fin de ce module, tu sauras
> construire une boucle de jeu interactive et écrire dans des fichiers.

---

## 1. Architecture de la boucle de jeu (#65)

Toute boucle de jeu interactive suit le même schéma en 3 étapes :

```
┌───────────────────────────────────────────────┐
│  1. PARSER    : transformer la saisie brute en données    │
│  2. VALIDER   : vérifier que l'action est autorisée        │
│  3. EXÉCUTER  : modifier l'état + logger l'événement      │
└───────────────────────────────────────────────┘
```

```python
# Exemple minimal d'une boucle de saisie
while nombre_de_deplacements < MAX:
    saisie = input("Destination (ex: B3) : ").strip().upper()

    # 1. PARSER : convertir la saisie en tuple (col, lig)
    cible = position_depuis_chaine(saisie)
    if cible is None:
        print("Format invalide, exemple : B3")
        continue                         # recommencer la saisie

    # 2. VALIDER : vérifier les règles
    ok, raison = valider_mouvement(etat, drone, cible)
    if not ok:
        print(f"Mouvement refusé : {raison}")
        continue

    # 3. EXÉCUTER : modifier l'état et logger
    ligne_log = executer_mouvement(etat, drone, cible, drones_recharges)
    etat["historique"].append(ligne_log)
    enregistrer_log(ligne_log)
    nombre_de_deplacements += 1
```

Ce schéma est présent dans **tout** programme interactif : jeux, CLI, formulaires.

---

## 2. Convertir une saisie en position

Le joueur tape `"B3"`. Il faut convertir ça en tuple `(1, 2)` (col=1, lig=2).

```python
LETTRES = ["A", "B", "C", "D", "E", "F", "G", "H"]

def position_depuis_chaine(texte):
    """
    Convertit "B3" en (1, 2).
    Retourne None si la saisie est invalide.
    """
    texte = texte.strip().upper()
    if len(texte) < 2:
        return None

    lettre = texte[0]           # "B"
    if lettre not in LETTRES:
        return None

    try:
        lig = int(texte[1:]) - 1   # "3" -> 2 (0-basé)
    except ValueError:
        return None

    col = LETTRES.index(lettre)    # "B" -> 1

    if 0 <= col < 8 and 0 <= lig < 8:
        return (col, lig)
    return None
```

Points clés :
- `texte[0]` = première lettre (la colonne)
- `texte[1:]` = tout le reste (le numéro de ligne)
- `int(texte[1:]) - 1` : conversion en entier, puis -1 pour passer en 0-basé
- `try/except ValueError` : si `"B"` est suivi de lettres et non de chiffres

---

## 3. La boucle de jeu à 2 joueurs

Le jeu alt erne 3 phases à chaque tour :

```
Tour N
  ├── Phase J1 : Joueur 1 déplace jusqu'à 3 drones
  ├── Phase J2 : Joueur 2 déplace jusqu'à 2 tempêtes
  └── Phase auto : tempêtes restantes bougent (50% chacune)
```

```python
def boucle_de_jeu(etat):
    while not etat["partie_finie"]:
        _phase_drones(etat)      # J1
        if etat["partie_finie"]:
            break
        _phase_tempetes(etat)    # J2
        if etat["partie_finie"]:
            break
        # Phase auto : météo + propagation zones X
        logs = deplacer_tempetes(etat)
        logs += propager_zones_x(etat)
        for ligne in logs:
            etat["historique"].append(ligne)
            enregistrer_log(ligne)
        if verifier_fin_partie(etat):
            break
        etat["tour"] += 1
```

---

## 4. Gérer les commandes simples

Pas besoin d'expressions régulières pour ce jeu — une comparaison de chaîne suffit :

```python
saisie = input("Déplacement (ex: D1) ou 'next' pour passer : ").strip().upper()

if saisie == "Q":
    etat["partie_finie"] = True
    return

if saisie == "NEXT":
    break

if saisie in etat["drones"]:    # "D1", "D2", "D3"
    drone = etat["drones"][saisie]
else:
    print(f"'{saisie}' n'est pas un drone valide.")
    continue
```

> 💡 `.strip().upper()` en premier : supprime les espaces et normalise la casse.
> L'utilisateur peut taper `"d1"`, `"D1"` ou `" D1 "` — tout sera reconnu.

---

## 5. Écrire dans un fichier — `logger.py`

Deux fichiers sont produits à chaque partie :

```
partie.log      ← tous les événements, un par ligne
resultats.txt   ← bilan final : score, tours, survivants
```

### Créer le log au début de la partie

```python
def demarrer_log():
    """Crée (ou écrase) le fichier de log."""
    with open("partie.log", "w", encoding="utf-8") as f:
        f.write("=== DRONE RESCUE — Journal de partie ===\n")
```

- `"w"` = écriture (efface le fichier s'il existait déjà)
- `with ... as f` : fermeture automatique, même si une erreur survient
- `encoding="utf-8"` : pour les accents et caractères spéciaux

### Ajouter une ligne à chaque événement

```python
def enregistrer_log(ligne):
    """Ajoute une ligne au journal."""
    with open("partie.log", "a", encoding="utf-8") as f:
        f.write(ligne + "\n")
```

- `"a"` = append (ajout en fin de fichier, sans écraser)

### Sauvegarder les résultats finaux

```python
def sauvegarder_resultats(etat):
    sauves = sum(1 for s in etat["survivants"].values() if s["etat"] == "sauve")
    total = len(etat["survivants"])
    issue = "VICTOIRE" if etat["victoire"] else "DÉFAITE"

    with open("resultats.txt", "w", encoding="utf-8") as f:
        f.write(f"Issue         : {issue}\n")
        f.write(f"Score final   : {etat['score']} pt(s)\n")
        f.write(f"Tours joués   : {etat['tour']}\n")
        f.write(f"Survivants    : {sauves}/{total} sauvés\n")
```

---

## 6. Format du journal de partie

Chaque ligne de log suit ce format :

```
T[nn]  [ID]   [départ]→[arrivée]   bat:[avant]→[après]   [EVENT]

Exemples :
T04  D1   B3→C3   bat:9→[8   PRISE S2
T04  D2   A1→A1   bat:8→[8   BLOQUE(T1)
T05  D3   E5→D7   bat:5→[4   [S2]   LIVRAISON S2 +1pt
T06  T1   IMMOBILE
```

---

## 7. Exercice A — Boucle de saisie simple

```python
# Écris une boucle qui demande des destinations jusqu'à ce que
# le joueur tape 'STOP'. Affiche chaque position valide reçue.
LETTRES = ["A", "B", "C", "D", "E", "F", "G", "H"]

while True:
    saisie = input("Destination : ").strip().upper()
    if saisie == "STOP":
        break
    cible = position_depuis_chaine(saisie)
    if cible is None:
        print("Format invalide (exemple : B3)")
    else:
        col, lig = cible
        print(f"Position validée : colonne {LETTRES[col]}, ligne {lig + 1}")
```

---

## 8. Exercice B — Écrire et lire un fichier de résultats

```python
# Partie 1 : écrire
resultats = {
    "score": 3,
    "tours": 12,
    "victoire": True
}
with open("resultats.txt", "w", encoding="utf-8") as f:
    for cle, valeur in resultats.items():
        f.write(f"{cle} : {valeur}\n")

# Partie 2 : lire
with open("resultats.txt", "r", encoding="utf-8") as f:
    contenu = f.read()
print(contenu)
```

---

## Erreurs classiques

**Erreur 1 — Logger avant d'exécuter**
```python
# ❌ Le log peut mentir si l'action est ensuite annulée
enregistrer_log("D1 se déplace vers B3")
ok, _ = valider_mouvement(...)

# ✅ Logger uniquement après exécution
ok, raison = valider_mouvement(etat, drone, cible)
if ok:
    ligne = executer_mouvement(etat, drone, cible, recharges)
    enregistrer_log(ligne)
```

**Erreur 2 — Oublier `.strip().upper()`**
```python
# ❌ "d1" ou " D1" ne matchent pas
if saisie == "D1":
    ...

# ✅
if saisie.strip().upper() == "D1":
    ...
```

**Erreur 3 — Utiliser `"w"` au lieu de `"a"` pour l'ajout**
```python
# ❌ Efface le fichier à chaque événement
with open("partie.log", "w") as f:
    f.write(ligne)

# ✅
with open("partie.log", "a") as f:
    f.write(ligne + "\n")
```

---

## Résumé des points clés

| Concept | Exemple | À retenir |
|---------|---------|----------|
| Normaliser saisie | `.strip().upper()` | Toujours en premier |
| Parser position | `position_depuis_chaine("B3")` | Retourne `(col, lig)` ou `None` |
| Boucle interactive | `while not fini: parser → valider → exécuter` | 3 étapes |
| Écrire fichier | `open("f.txt", "w")` | Écrase le fichier |
| Ajouter fichier | `open("f.txt", "a")` | Ajoute en fin |
| Logger | Après exécution uniquement | Jamais avant |

---

## Exercices du module

Voir `exercices/ex_08_console.py`

## Prompts IA utiles

> *« Comment écrire et lire un fichier texte en Python avec `with open()` ? »*

> *« Comment construire une boucle de saisie interactive en Python qui valide les entrées utilisateur ? »*

> *« Comment convertir une saisie comme 'B3' en coordonnées numériques dans un jeu Python ? »*
