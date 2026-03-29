# Module 07 — Logique de jeu

## Concepts couverts

- Architecture MVC légère (Modèle / Vue / Contrôleur)
- Gestion d'état global
- Validation de mouvement avec règles complexes
- Propagation stochastique (probabilité)
- Conditions de fin de partie

## Règles du jeu à implémenter

### Déplacement d'un drone

1. Le drone doit avoir `batterie > 0`
2. Le drone ne doit pas être bloqué (`bloque == 0`)
3. La cible doit être dans la grille
4. La distance de Chebyshev entre départ et cible doit être `<= 1` (une case par déplacement)
5. Si la case cible contient un survivant libre, le drone le charge automatiquement
6. Si la case cible est l'hôpital et que le drone porte un survivant → livraison → `+1` point
7. La batterie diminue de 1 **sauf** si une tempête est sur la case du drone
8. Maximum 3 déplacements par drone par tour

### Propagation des tempêtes

- Chaque tour, chaque tempête peut se déplacer d'une case (pas en diagonale)
- Probabilité de déplacement : paramétrable (`PROBA_PROPAGATION = 0.3`)
- Une tempête ne peut pas se déplacer sur l'hôpital
- Une zone dangereuse (X) se propage aussi tous les 2 tours, sans diagonal, pas sur bâtiment/hôpital/survivant

### Blocage par tempête

- Si une tempête arrive sur un drone : drone bloqué 2 tours
- Un drone bloqué ne consomme pas de batterie
- Un drone bloqué portant un survivant garde son survivant

## Code — fonctions clés

```python
def peut_se_deplacer(drone, cible_col: int, cible_row: int, etat: dict) -> tuple:
    """
    Vérifie si un drone peut se déplacer vers la cible.
    
    Returns:
        (bool, str) — (autorisé, message d'erreur ou '')
    """
    if drone.est_hs:
        return False, 'Drone HS (batterie vide)'
    if drone.est_bloque:
        return False, f'Drone bloqué ({drone.bloque} tours restants)'
    dist = distance_chebyshev(
        (drone.col, drone.row), (cible_col, cible_row)
    )
    if dist != 1:
        return False, f'Distance invalide ({dist}) — déplacement d\'une case à la fois'
    if not coord_valide_idx(cible_col, cible_row, etat['taille']):
        return False, 'Case hors grille'
    return True, ''


def executer_deplacement(drone, cible_col: int, cible_row: int, etat: dict) -> list:
    """
    Exécute un déplacement validé. Retourne les événements survenus.
    """
    evenements = []
    
    # Déplacement
    drone.col = cible_col
    drone.row = cible_row
    
    # Vérification tempête sur la case d'arrivée
    tempete_sur_case = next(
        (t for t in etat['tempetes'] if t.col == cible_col and t.row == cible_row),
        None
    )
    if tempete_sur_case:
        drone.bloque = 2
        evenements.append(('BLOQUE', drone.id, tempete_sur_case.id))
    else:
        # Consommation batterie seulement si pas de tempête
        drone.batterie -= 1
    
    # Chargement d'un survivant
    survivant_sur_case = _survivant_libre_en(cible_col, cible_row, etat)
    if survivant_sur_case and drone.survivant is None:
        drone.survivant = survivant_sur_case
        survivant_sur_case.porte_par = drone
        evenements.append(('CHARGE', drone.id, survivant_sur_case.id))
    
    # Livraison à l'hôpital
    hopital = etat['hopital']
    if cible_col == hopital.col and cible_row == hopital.row and drone.survivant:
        surv = drone.survivant
        surv.sauve = True
        surv.porte_par = None
        drone.survivant = None
        etat['score'] += 1
        evenements.append(('LIVRAISON', drone.id, surv.id))
        # Recharge batterie à l'hôpital
        drone.batterie = drone.batterie_max
        evenements.append(('RECHARGÉ', drone.id))
    
    return evenements
```

## Exercices du module

Voir `exercices/ex_07_logique.py`

## Tips et best practices

- **Sépare `peut_se_deplacer()` de `executer_deplacement()`** : validation d'abord, exécution ensuite.
- **Retourne des événements** plutôt que d'afficher dans les fonctions de logique — l'affichage appartient à la vue.
- **Teste chaque règle indépendamment** avec de petits scripts avant de les intégrer.

## Références

- [Real Python — MVC Pattern in Python](https://realpython.com/python-mvc/)
- [Docs Python — random.random()](https://docs.python.org/fr/3/library/random.html#random.random)

## Prompts IA

> *« Comment structurer un moteur de jeu en Python pour séparer la logique, l'affichage et la saisie ? »*

> *« Explique-moi comment implémenter une propagation aléatoire dans un jeu Python (probabilité par case). »*

> *« Comment retourner plusieurs informations depuis une fonction Python — tuple, dataclass, ou dict ? »*
