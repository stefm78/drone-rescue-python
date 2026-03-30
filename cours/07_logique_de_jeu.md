# Module 07 — Logique de jeu

## Concepts couverts

- Architecture MVC légère (Modèle / Vue / Contrôleur)
- Gestion d'état global
- Validation de mouvement avec règles composées
- Propagation stochastique (probabilité)
- Conditions de fin de partie

## Règles du jeu à implémenter

### Déplacement d'un drone

1. Batterie > 0
2. Drone non bloqué (`bloque == 0`)
3. Cible dans la grille
4. Distance Chebyshev ≤ 1
5. Survivant libre sur la case cible → chargé automatiquement
6. Case cible = hôpital + drone porte survivant → livraison +1pt + recharge batterie
7. Batterie −= 1 **sauf** si tempête sur la case du drone
8. Maximum 3 déplacements par drone par tour

### Propagation des tempêtes

- Chaque tour, chaque tempête peut se déplacer d'une case (pas en diagonale)
- Probabilité de déplacement : `PROBA_PROPAGATION = 0.3`
- Une tempête ne peut pas se déplacer sur l'hôpital
- Une zone dangereuse (X) se propage tous les 2 tours, orthogonalement, pas sur bâtiment/hôpital/survivant

### Blocage par tempête

- Tempête arrive sur un drone → drone bloqué 2 tours
- Un drone bloqué ne consomme pas de batterie
- Un drone bloqué portant un survivant le conserve

## Lien avec le projet

**Convention : `colonne: str`, `ligne: int` (1-based)**

```python
def peut_se_deplacer(drone, col_cible: str, lig_cible: int, etat) -> tuple:
    """
    Vérifie si un drone peut se déplacer vers la cible.
    Retourne (bool, str) : (autorisé, message d'erreur ou '')
    """
    if drone.est_hs:
        return False, 'Drone HS (batterie vide)'
    if drone.est_bloque:
        return False, f'Drone bloqué ({drone.bloque} tours restants)'
    if not coord_valide(col_cible, lig_cible):
        return False, 'Case hors grille'
    dist = distance_chebyshev(drone.colonne, drone.ligne, col_cible, lig_cible)
    if dist != 1:
        return False, f"Distance invalide ({dist}) — une case à la fois"
    return True, ''


def executer_deplacement(drone, col_cible: str, lig_cible: int, etat) -> list:
    """
    Exécute un déplacement validé. Retourne la liste des événements survenus.
    """
    evenements = []
    drone.colonne = col_cible
    drone.ligne   = lig_cible

    # Tempête sur la case d'arrivée ?
    tempete = next((t for t in etat.tempetes if t.colonne == col_cible and t.ligne == lig_cible), None)
    if tempete:
        drone.bloque = 2
        evenements.append(('BLOQUE', drone.identifiant, tempete.identifiant))
    else:
        drone.consommer_batterie()   # -1 batterie

    # Chargement d'un survivant ?
    surv = next((s for s in etat.survivants
                 if s.etat == 'en_attente' and s.colonne == col_cible and s.ligne == lig_cible), None)
    if surv and drone.survivant is None:
        drone.survivant = surv
        surv.etat = 'porte'
        evenements.append(('CHARGE', drone.identifiant, surv.identifiant))

    # Livraison à l'hôpital ?
    if (col_cible == etat.hopital.colonne and lig_cible == etat.hopital.ligne
            and drone.survivant):
        s = drone.survivant
        s.etat = 'sauve'
        drone.survivant = None
        etat.score += 1
        drone.batterie = drone.batterie_max   # recharge
        evenements.append(('LIVRAISON', drone.identifiant, s.identifiant))

    return evenements


def propager_tempetes(etat, proba: float = 0.3) -> None:
    """Déplace chaque tempête aléatoirement avec probabilité proba."""
    import random
    COLS = [chr(ord('A') + i) for i in range(12)]
    for t in etat.tempetes:
        if random.random() < proba:
            # Voisins orthogonaux valides (pas l'hôpital)
            voisins = []
            for dcol, dlig in [(-1,0),(1,0),(0,-1),(0,1)]:
                i = ord(t.colonne) - ord('A') + dcol
                l = t.ligne + dlig
                if 0 <= i < 12 and 1 <= l <= 12:
                    c = COLS[i]
                    if not (c == etat.hopital.colonne and l == etat.hopital.ligne):
                        voisins.append((c, l))
            if voisins:
                t.colonne, t.ligne = random.choice(voisins)
```

## Erreurs classiques

**Erreur 1 — Exécuter sans valider**
```python
# ❌ Aucune vérification → déplacement invalide silencieux
drone.colonne = col_cible
drone.ligne   = lig_cible

# ✅ Toujours valider avant d'exécuter
ok, msg = peut_se_deplacer(drone, col_cible, lig_cible, etat)
if ok:
    evenements = executer_deplacement(drone, col_cible, lig_cible, etat)
else:
    print(f'Mouvement refusé : {msg}')
```

**Erreur 2 — Afficher dans les fonctions de logique**
```python
# ❌ La logique ne doit pas afficher — mélange MVC
def executer_deplacement(drone, ...):
    print(f'{drone.identifiant} se déplace')   # ❌
    ...

# ✅ Retourner des événements, afficher dans la vue
def executer_deplacement(drone, ...) -> list:
    evenements = []
    ...
    return evenements   # l'affichage est fait par console.py
```

**Erreur 3 — Modifier l'état pendant l'itération**
```python
# ❌ Modifier etat.survivants pendant une itération sur etat.survivants
for s in etat.survivants:
    if s.etat == 'sauve':
        etat.survivants.remove(s)   # comportement imprévisible

# ✅ Itérer sur une copie
for s in etat.survivants[:]:
    if s.etat == 'sauve':
        etat.survivants.remove(s)
```

## Exercice de compréhension

**Q1.** Pourquoi `peut_se_deplacer()` et `executer_deplacement()` sont deux fonctions séparées ?
<details><summary>Réponse</summary>

Principe de responsabilité unique : la validation vérifie les règles sans changer l'état, l'exécution modifie l'état. On peut ainsi tester la validation indépendamment, et prévisualiser un mouvement sans l'exécuter.
</details>

**Q2.** Que retourne `executer_deplacement()` et pourquoi une liste ?
<details><summary>Réponse</summary>

Une liste de tuples d'événements : `('BLOQUE', 'D1', 'T2')`, `('LIVRAISON', 'D3', 'S1')`… Une liste car plusieurs événements peuvent se produire en un déplacement (ex : charger un survivant ET se bloquer).
</details>

**Q3.** Avec `PROBA_PROPAGATION = 0.3` et `random.seed(42)`, la tempête se déplace-t-elle à coup sûr ?
<details><summary>Réponse</summary>

Non. `random.random() < 0.3` signifie 30% de chances par tour. Avec `seed=42`, la séquence est déterministe mais pas forcément vraie au premier appel.
</details>

## Exercices du module

Voir `exercices/ex_07_logique.py`

## Tips et best practices

- **Sépare validation et exécution** : `peut_se_deplacer()` + `executer_deplacement()`.
- **Retourne des événements** plutôt que d'afficher dans les fonctions de logique.
- **Teste chaque règle indépendamment** avec de petits scripts.
- **Jamais de `print()` dans la logique** — les affichages appartiennent à `affichage.py`.

## Références

- [Real Python — MVC Pattern in Python](https://realpython.com/python-mvc/)
- [Docs Python — random.random()](https://docs.python.org/fr/3/library/random.html#random.random)

## Prompts IA

> *« Comment structurer un moteur de jeu en Python pour séparer la logique, l'affichage et la saisie ? »*

> *« Explique-moi comment implémenter une propagation aléatoire dans un jeu Python (probabilité par case). »*

> *« Comment retourner plusieurs informations depuis une fonction Python — tuple, dataclass, ou dict ? »*
