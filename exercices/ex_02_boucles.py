# ============================================================
# EXERCICE 02 — Boucles et conditions
# Module : cours/02_boucles_et_conditions.md
# ============================================================
# Objectif : maîtriser for, while, if/elif/else, break, continue
# dans le contexte du jeu Drone Rescue.
# ============================================================

# Données de départ utilisées dans les exercices
batteries = {"D1": 10, "D2": 8, "D3": 0, "D4": 15, "D5": 0, "D6": 5}
positions  = {"D1": (0,0), "D2": (3,4), "D3": (1,1), "D4": (5,5), "D5": (0,11), "D6": (7,3)}
surv_positions = [(2,3), (4,4), (8,1), (0,7), (11,11)]

# ----------------------------------------------------------
# PARTIE A — for classique
# ----------------------------------------------------------
# Exercice A1
# Affichez chaque identifiant de drone avec sa batterie.
# Format attendu par ligne : "D1 : 10"  (sans guillemets)

def afficher_batteries(batteries: dict) -> None:
    """Affiche id : batterie pour chaque drone."""
    # Votre code ici
    pass

# Test A1
print("--- A1 : afficher_batteries ---")
afficher_batteries(batteries)
# (vérification visuelle)

# ----------------------------------------------------------
# Exercice A2
# Retournez la liste des identifiants de drones dont la batterie est > 0.

def drones_actifs(batteries: dict) -> list:
    """Retourne la liste des IDs de drones avec batterie > 0."""
    # Votre code ici
    pass

# Test A2
resultat = drones_actifs(batteries)
assert set(resultat) == {"D1", "D2", "D4", "D6"}, f"A2 : attendu {{D1,D2,D4,D6}}, obtenu {set(resultat)}"
print("A2 OK")

# ----------------------------------------------------------
# PARTIE B — while et compteurs
# ----------------------------------------------------------
# Exercice B1
# Simulez la consommation de batterie d'un drone.
# Le drone se déplace tant que :
#   - sa batterie est > 0
#   - le nombre de déplacements effectués est < max_depl
# Retournez la batterie finale et le nombre de déplacements réels.

def simuler_deplacements(batterie_init: int, max_depl: int) -> tuple:
    """
    Retourne (batterie_finale, nb_deplacements_effectues).
    Chaque déplacement coûte 1 point de batterie.
    """
    # Votre code ici
    pass

# Test B1
bat, nb = simuler_deplacements(10, 3)
assert bat == 7 and nb == 3, f"B1 : attendu (7,3), obtenu ({bat},{nb})"
bat, nb = simuler_deplacements(1, 3)
assert bat == 0 and nb == 1, f"B1 : batterie faible, attendu (0,1), obtenu ({bat},{nb})"
print("B1 OK")

# ----------------------------------------------------------
# PARTIE C — if / elif / else
# ----------------------------------------------------------
# Exercice C1
# Classifiez l'état d'un drone selon sa batterie :
#   batterie == 0         → "HS"
#   batterie <= 5         → "critique"
#   batterie <= 10        → "normal"
#   batterie > 10         → "plein"

def etat_batterie(batterie: int) -> str:
    """Retourne l'état du drone selon sa batterie."""
    # Votre code ici
    pass

# Test C1
assert etat_batterie(0)  == "HS",       "C1 : 0 → HS"
assert etat_batterie(3)  == "critique", "C1 : 3 → critique"
assert etat_batterie(8)  == "normal",   "C1 : 8 → normal"
assert etat_batterie(20) == "plein",    "C1 : 20 → plein"
print("C1 OK")

# ----------------------------------------------------------
# Exercice C2
# Validez si un déplacement est possible :
#   - la batterie doit être > 0
#   - le drone ne doit pas être bloqué (bloque=False)
#   - le nombre de déplacements déjà effectués ce tour doit être < max_depl
# Retournez True si le déplacement est possible, False sinon.
# En cas de refus, retournez aussi la raison (str).

def deplacement_possible(batterie: int, bloque: bool, depl_effectues: int, max_depl: int) -> tuple:
    """
    Retourne (bool, raison_str).
    raison_str est "" si possible, sinon message d'erreur.
    """
    # Votre code ici
    pass

# Test C2
ok, _ = deplacement_possible(10, False, 0, 3)
assert ok is True, "C2 : devrait être possible"
ok, raison = deplacement_possible(0, False, 0, 3)
assert ok is False and "batterie" in raison.lower(), "C2 : batterie à 0"
ok, raison = deplacement_possible(5, True, 0, 3)
assert ok is False and "bloqu" in raison.lower(), "C2 : drone bloqué"
ok, raison = deplacement_possible(5, False, 3, 3)
assert ok is False, "C2 : max déplacements atteint"
print("C2 OK")

# ----------------------------------------------------------
# PARTIE D — break et continue
# ----------------------------------------------------------
# Exercice D1
# Parcourez la liste surv_positions et trouvez la première position
# de survivant qui se trouve dans la moitié gauche de la grille
# (colonne < 6). Retournez cette position ou None si aucune.

def premier_surv_gauche(surv_positions: list) -> tuple | None:
    """Retourne la première position de survivant avec col < 6."""
    # Votre code ici (utilisez break)
    pass

# Test D1
res = premier_surv_gauche(surv_positions)
assert res == (2,3), f"D1 : attendu (2,3), obtenu {res}"
print("D1 OK")

# Exercice D2
# Calculez la batterie totale en ignorant les drones HS (batterie == 0).
# Utilisez continue pour sauter les drones HS.

def batterie_totale_actifs(batteries: dict) -> int:
    """Retourne la somme des batteries des drones non-HS."""
    # Votre code ici (utilisez continue)
    pass

# Test D2
total = batterie_totale_actifs(batteries)
assert total == 10 + 8 + 15 + 5, f"D2 : attendu {10+8+15+5}, obtenu {total}"
print("D2 OK")

# ----------------------------------------------------------
# PARTIE E — list comprehension (bonus)
# ----------------------------------------------------------
# Exercice E1
# Recréez drones_actifs (A2) en une seule ligne avec une list comprehension.

def drones_actifs_v2(batteries: dict) -> list:
    """Version one-liner avec list comprehension."""
    # Votre code ici (une seule ligne)
    pass

# Test E1
resultat2 = drones_actifs_v2(batteries)
assert set(resultat2) == {"D1", "D2", "D4", "D6"}, "E1 : list comprehension incorrecte"
print("E1 OK")

print("\n=== Tous les tests de l'exercice 02 sont passés ! ===")
