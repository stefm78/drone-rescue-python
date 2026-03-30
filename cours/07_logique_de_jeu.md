# Module 07 — Logique de jeu

> **Fil rouge :** `logique.py` contient toutes les règles du jeu.
> À la fin de ce module, tu sauras valider un mouvement, exécuter ses effets,
> gérer les règles de batterie et comprendre la séparation validation/exécution.

---

## 1. Principe : séparer validation et exécution

C'est la règle la plus importante du module :

```
valider_mouvement()   →  vérifie les règles SANS modifier l'état
executer_mouvement()  →  applique le mouvement SI validé
```

```python
# Dans console.py
ok, raison = valider_mouvement(etat, drone, cible)
if ok:
    ligne_log = executer_mouvement(etat, drone, cible, drones_recharges)
else:
    print(f"Mouvement refusé : {raison}")
```

Avantage : on peut tester la validation sans modifier quoi que ce soit dans le jeu.
C'est aussi plus lisible : chaque fonction fait une seule chose.

---

## 2. Valider un mouvement drone

La validation vérifie plusieurs règles dans l'ordre. Dès qu'une échoue,
on retourne `(False, raison)` immédiatement.

```python
def valider_mouvement(etat, drone, cible):
    """
    drone  : dictionnaire du drone
    cible  : tuple (col, lig)
    Retourne (True, "") ou (False, message d'erreur).
    """
    did = drone["id"]

    if drone["hors_service"]:
        return False, f"{did} est hors service"

    if drone["bloque"] > 0:
        return False, f"{did} est bloqué ({drone['bloque']} tour(s))"

    col, lig = cible
    if not (0 <= col < 8 and 0 <= lig < 8):
        return False, "Position hors de la grille"

    dist = max(abs(col - drone["col"]), abs(lig - drone["lig"]))
    if dist > 1:
        return False, "Max 1 case par déplacement"

    if cible in etat["batiments"]:
        return False, "Case bloquée par un bâtiment"

    if drone["batterie"] <= 0:
        return False, f"{did} n'a plus de batterie"

    return True, ""
```

---

## 3. Règles de batterie (officielles)

Trois règles distinctes s'appliquent sur la batterie :

| Situation | Coût batterie |
|-----------|---------------|
| Déplacement seul | −1 |
| Déplacement avec survivant embarqué | −2 |
| Entrée dans une zone X (s'ajoute au coût précédent) | −2 supplémentaires |
| Recharge à l'hôpital | +3 (par tour sur place) |

```python
# Calcul du coût dans executer_mouvement()
cout = 2 if drone["survivant"] else 1        # transport ou déplacement simple
if cible in etat["zones_x"]:
    cout += 2                                  # supplément zone X
drone["batterie"] = max(0, drone["batterie"] - cout)
```

> ⚠️ `max(0, ...)` empêche la batterie de passer en négatif.

---

## 4. Exécution d'un mouvement

Après validation, `executer_mouvement()` modifie l'état et retourne une ligne de log.

```python
def executer_mouvement(etat, drone, cible, drones_recharges_ce_tour):
    did = drone["id"]
    depart = (drone["col"], drone["lig"])
    bat_avant = drone["batterie"]

    # 1. Collision avec une tempête ?
    tempete_sur_cible = _tempete_sur_case(etat, cible)
    if tempete_sur_cible:
        drone["bloque"] = 2
        drone["col"], drone["lig"] = cible
        return ...  # log "BLOQUE"

    # 2. Coût batterie
    cout = 2 if drone["survivant"] else 1
    if cible in etat["zones_x"]:
        cout += 2
    drone["batterie"] = max(0, drone["batterie"] - cout)
    drone["col"], drone["lig"] = cible

    # 3. Hôpital : livraison + recharge
    if cible == etat["hopital"]:
        if drone["survivant"]:
            etat["survivants"][drone["survivant"]]["etat"] = "sauve"
            etat["score"] += 1
            drone["survivant"] = None
        if did not in drones_recharges_ce_tour:
            drone["batterie"] = min(drone["batterie_max"],
                                    drone["batterie"] + 3)   # +3 par tour
            drones_recharges_ce_tour.add(did)
    else:
        # 4. Prise d'un survivant
        s = _survivant_sur_case(etat, cible)
        if s and drone["survivant"] is None:
            drone["survivant"] = s["id"]
            s["etat"] = "embarque"

    # 5. Hors service si batterie à 0
    if drone["batterie"] <= 0:
        drone["hors_service"] = True

    return ...  # ligne de log
```

---

## 5. Propagation des zones X

Tous les `PROPAGATION_FREQUENCE` tours, les zones X s'étendent vers leurs voisins
orthogonaux avec une probabilité `PROBA_PROPAGATION` :

```python
def propager_zones_x(etat):
    nouvelles = set()

    for zone in list(etat["zones_x"]):      # list() pour itérer sur une copie
        for voisin in _voisins_ortho(zone):  # 4 voisins N/S/E/O
            if not _case_valide(voisin):
                continue
            if voisin in etat["zones_x"] or voisin in nouvelles:
                continue
            if random.random() < PROBA_PROPAGATION:   # ex: 30% de chance
                nouvelles.add(voisin)

    for pos in nouvelles:
        etat["zones_x"].add(pos)
```

Pourquoi `list(etat["zones_x"])` avant d'itérer ?
Parce qu'on ne peut pas modifier un set pendant qu'on l'itère.
La copie garantit qu'on travaille sur l'état avant propagation.

---

## 6. Phase météo (déplacement automatique des tempêtes)

Ch aque tempête a 50% de chance de se déplacer automatiquement en fin de tour :

```python
def deplacer_tempetes(etat):
    for tempete in etat["tempetes"].values():
        if random.random() > 0.5:          # 50% : ne bouge pas
            continue

        cible = (tempete["col"] + tempete["dx"],
                 tempete["lig"] + tempete["dy"])

        if not _case_libre_tempete(etat, cible, etat["hopital"]):
            # Rebond : chercher une direction libre aléatoire
            voisins = _voisins_diag((tempete["col"], tempete["lig"]))
            libres = [v for v in voisins
                      if _case_libre_tempete(etat, v, etat["hopital"])]
            if libres:
                cible = random.choice(libres)
                tempete["dx"] = cible[0] - tempete["col"]
                tempete["dy"] = cible[1] - tempete["lig"]
            else:
                continue   # reste sur place

        tempete["col"], tempete["lig"] = cible
```

---

## 7. Fin de partie

```python
def verifier_fin_partie(etat):
    survivants = etat["survivants"]
    drones = etat["drones"]

    # Victoire : tous les survivants sont sauvés
    if all(s["etat"] == "sauve" for s in survivants.values()):
        etat["partie_finie"] = True
        etat["victoire"] = True
        return True

    # Défaite : dépassement du nombre de tours
    if etat["tour"] > NB_TOURS_MAX:
        etat["partie_finie"] = True
        return True

    # Défaite : tous les drones hors service
    if all(d["hors_service"] for d in drones.values()):
        etat["partie_finie"] = True
        return True

    return False
```

La fonction `all()` est très lisible : elle retourne `True` si la condition est vraie
pour **chaque** élément de l'itérable.

---

## 8. Exercice A — Valider un mouvement simple

```python
etat = {
    "batiments": [(2, 3)],
    "zones_x": set(),
    "hopital": (0, 7),
    "drones": {},
    "tempetes": {},
    "survivants": {},
}
drone = {
    "id": "D1", "col": 1, "lig": 1,
    "batterie": 5, "batterie_max": 20,
    "survivant": None, "bloque": 0, "hors_service": False
}

# Test 1 : mouvement valide
print(valider_mouvement(etat, drone, (2, 1)))   # (True, "")

# Test 2 : distance trop grande
print(valider_mouvement(etat, drone, (4, 1)))   # (False, "Max 1 case...")

# Test 3 : bâtiment sur la cible
print(valider_mouvement(etat, drone, (2, 3)))   # (False, "Case bloquée...")
```

---

## 9. Exercice B — Compter les survivants restants

```python
# Avec all() et values()
def tous_sauves(etat):
    return all(s["etat"] == "sauve" for s in etat["survivants"].values())

# Avec un compteur
def nb_survivants_restants(etat):
    nb = 0
    for s in etat["survivants"].values():
        if s["etat"] != "sauve":
            nb += 1
    return nb
```

---

## Erreurs classiques

**Erreur 1 — Exécuter sans valider**
```python
# ❌ Déplacement direct sans vérification
drone["col"], drone["lig"] = cible

# ✅ Toujours valider d'abord
ok, raison = valider_mouvement(etat, drone, cible)
if ok:
    executer_mouvement(etat, drone, cible, drones_recharges)
else:
    print(f"Refusé : {raison}")
```

**Erreur 2 — Itérer sur un set en le modifiant**
```python
# ❌ RuntimeError : modification pendant itération
for zone in etat["zones_x"]:
    etat["zones_x"].add(voisin)

# ✅ Itérer sur une copie
for zone in list(etat["zones_x"]):
    etat["zones_x"].add(voisin)
```

**Erreur 3 — Batterie négative**
```python
# ❌ La batterie peut passer en dessous de 0
drone["batterie"] -= cout

# ✅ Bloquer à 0
drone["batterie"] = max(0, drone["batterie"] - cout)
```

---

## Résumé des règles du jeu

| Règle | Valeur |
|-------|--------|
| Déplacements J1 par tour | 3 max (1 par drone) |
| Déplacements J2 par tour | 2 max (1 par tempête) |
| Coût déplacement seul | −1 batterie |
| Coût avec survivant | −2 batterie |
| Supplément zone X | −2 batterie |
| Recharge hôpital | +3 par tour |
| Blocage tempête | 2 tours |
| Propagation zones X | tous les 3 tours, 30% |
| Phase météo | 50% de chance/tempête |

---

## Exercices du module

Voir `exercices/ex_07_logique.py`

## Prompts IA utiles

> *« Comment séparer la validation et l'exécution d'une action dans un jeu Python ? »*

> *« Comment implémenter un système de points avec des dictionnaires Python ? »*

> *« Comment itérer sur un dictionnaire de dictionnaires pour trouver tous les éléments qui vérifient une condition ? »*
