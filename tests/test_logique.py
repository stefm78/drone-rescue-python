# =============================================================================
# test_logique.py — Tests automatisés du moteur Drone Rescue
#
# Exécution :
#   pytest tests/test_logique.py -v
#   python tests/test_logique.py
#
# Couvre : initialisation, validation mouvement, exécution, propagation,
#          fin de partie, coûts officiels, collision tempête (PR #11).
# =============================================================================

import sys
import os

# Accès au dossier jeu/ depuis tests/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'jeu'))

from logique import (
    initialiser_partie,
    creer_drone, creer_survivant,
    valider_mouvement, executer_mouvement,
    propager_zones_x, verifier_fin_partie,
    appliquer_recharges_hopital,
)
from config import COUT_TRANSPORT, COUT_ZONE_X, RECHARGE_HOPITAL, BATTERIE_INIT


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _etat_minimal():
    """Retourne un état de jeu minimal reproductible pour les tests."""
    etat = initialiser_partie()
    # Placer D1 en (0, 0) manuellement pour des tests déterministes
    drone = list(etat["drones"].values())[0]
    drone["col"], drone["lig"] = 0, 0
    etat["grille"][0][0] = 'D'
    return etat, drone


# ---------------------------------------------------------------------------
# Tests initialisation
# ---------------------------------------------------------------------------

def test_initialiser_partie_structure():
    """L'état initial contient toutes les clés attendues."""
    etat = initialiser_partie()
    for cle in ("tour", "score", "partie_finie", "victoire",
                "grille", "hopital", "drones", "tempetes",
                "survivants", "zones_x", "historique"):
        assert cle in etat, f"Clé manquante : {cle}"


def test_initialiser_partie_tour_1():
    """La partie commence au tour 1."""
    etat = initialiser_partie()
    assert etat["tour"] == 1
    assert etat["score"] == 0
    assert etat["partie_finie"] is False


def test_initialiser_partie_hopital_dans_grille():
    """L'hôpital est dans les limites de la grille."""
    from config import GRILLE_TAILLE
    etat = initialiser_partie()
    col, lig = etat["hopital"]
    assert 0 <= col < GRILLE_TAILLE
    assert 0 <= lig < GRILLE_TAILLE


# ---------------------------------------------------------------------------
# Tests valider_mouvement
# ---------------------------------------------------------------------------

def test_valider_mouvement_ok():
    """Un déplacement d'une case valide est accepté."""
    etat, drone = _etat_minimal()
    drone["col"], drone["lig"] = 3, 3
    ok, raison = valider_mouvement(etat, drone, (4, 3))
    assert ok, f"Attendu True, got False : {raison}"


def test_valider_mouvement_hors_service():
    """Un drone hors service ne peut pas se déplacer."""
    etat, drone = _etat_minimal()
    drone["hors_service"] = True
    ok, raison = valider_mouvement(etat, drone, (1, 0))
    assert not ok
    assert "hors service" in raison.lower()


def test_valider_mouvement_trop_loin():
    """Un déplacement de 2 cases est refusé."""
    etat, drone = _etat_minimal()
    drone["col"], drone["lig"] = 0, 0
    ok, raison = valider_mouvement(etat, drone, (2, 0))
    assert not ok


def test_valider_mouvement_batterie_insuffisante():
    """Un drone avec 1 batterie ne peut pas entrer en zone X (coût = 1+2 = 3)."""
    etat, drone = _etat_minimal()
    drone["col"], drone["lig"] = 3, 3
    drone["batterie"] = 1
    cible = (4, 3)
    etat["zones_x"].add(cible)  # zone X sur la cible
    ok, raison = valider_mouvement(etat, drone, cible)
    assert not ok
    assert "batterie insuffisante" in raison.lower() or "insuffisant" in raison.lower()


def test_valider_mouvement_bloque():
    """Un drone bloqué ne peut pas se déplacer."""
    etat, drone = _etat_minimal()
    drone["bloque"] = 2
    ok, _ = valider_mouvement(etat, drone, (1, 0))
    assert not ok


def test_valider_mouvement_batiment():
    """Un drone ne peut pas entrer sur un bâtiment."""
    etat, drone = _etat_minimal()
    drone["col"], drone["lig"] = 3, 3
    cible = (4, 3)
    etat["batiments"].append(cible)
    ok, _ = valider_mouvement(etat, drone, cible)
    assert not ok


# ---------------------------------------------------------------------------
# Tests coûts officiels
# ---------------------------------------------------------------------------

def test_cout_deplacement_normal():
    """Déplacement sans survivant, hors zone X : coût = 1."""
    etat, drone = _etat_minimal()
    drone["col"], drone["lig"] = 3, 3
    drone["batterie"] = 10
    bat_avant = drone["batterie"]
    executer_mouvement(etat, drone, (4, 3), set())
    assert drone["batterie"] == bat_avant - 1


def test_cout_transport_survivant():
    """Déplacement avec survivant, hors zone X : coût = COUT_TRANSPORT."""
    etat, drone = _etat_minimal()
    drone["col"], drone["lig"] = 3, 3
    drone["batterie"] = 10
    drone["survivant"] = "S1"
    # Ajouter S1 comme sauvé pour éviter de déclencher la livraison
    etat["survivants"]["S1"] = {"id": "S1", "col": 3, "lig": 3, "etat": "embarque"}
    bat_avant = drone["batterie"]
    cible = (4, 3)
    # S'assurer que la cible n'est pas l'hôpital
    if cible == etat["hopital"]:
        cible = (4, 4)
    executer_mouvement(etat, drone, cible, set())
    assert drone["batterie"] == bat_avant - COUT_TRANSPORT


def test_cout_zone_x():
    """Déplacement normal en zone X : coût = 1 + COUT_ZONE_X."""
    etat, drone = _etat_minimal()
    drone["col"], drone["lig"] = 3, 3
    drone["batterie"] = 10
    cible = (4, 3)
    etat["zones_x"].add(cible)
    bat_avant = drone["batterie"]
    executer_mouvement(etat, drone, cible, set())
    assert drone["batterie"] == bat_avant - (1 + COUT_ZONE_X)


# ---------------------------------------------------------------------------
# Tests collision tempête — PR #11
# ---------------------------------------------------------------------------

def test_tempete_bloque_drone_2_tours():
    """Un drone entrant dans une tempête est bloqué 2 tours."""
    etat, drone = _etat_minimal()
    drone["col"], drone["lig"] = 3, 3
    drone["batterie"] = 10
    cible = (4, 3)
    etat["tempetes"].append({"col": 4, "lig": 3})  # tempête sur la cible
    executer_mouvement(etat, drone, cible, set())
    assert drone["bloque"] == 2, f"Attendu bloque=2, got {drone['bloque']}"


def test_tempete_consomme_batterie_deplacement_normal():
    """Collision tempête sans survivant : batterie consommée = 1 (coût normal)."""
    etat, drone = _etat_minimal()
    drone["col"], drone["lig"] = 3, 3
    drone["batterie"] = 10
    bat_avant = drone["batterie"]
    cible = (4, 3)
    etat["tempetes"].append({"col": 4, "lig": 3})
    executer_mouvement(etat, drone, cible, set())
    assert drone["batterie"] == bat_avant - 1, (
        f"Batterie devrait être {bat_avant - 1}, got {drone['batterie']} — "
        "bug PR#11 : batterie non consommée lors d'une collision tempête"
    )


def test_tempete_consomme_batterie_avec_survivant():
    """Collision tempête avec survivant : batterie consommée = COUT_TRANSPORT."""
    etat, drone = _etat_minimal()
    drone["col"], drone["lig"] = 3, 3
    drone["batterie"] = 10
    drone["survivant"] = "S1"
    etat["survivants"]["S1"] = {"id": "S1", "col": 3, "lig": 3, "etat": "embarque"}
    bat_avant = drone["batterie"]
    cible = (4, 3)
    etat["tempetes"].append({"col": 4, "lig": 3})
    executer_mouvement(etat, drone, cible, set())
    assert drone["batterie"] == bat_avant - COUT_TRANSPORT, (
        f"Batterie devrait être {bat_avant - COUT_TRANSPORT}, got {drone['batterie']}"
    )


def test_tempete_zone_x_consomme_batterie_supplementaire():
    """Collision tempête sur case zone X : coût = 1 + COUT_ZONE_X."""
    etat, drone = _etat_minimal()
    drone["col"], drone["lig"] = 3, 3
    drone["batterie"] = 10
    bat_avant = drone["batterie"]
    cible = (4, 3)
    etat["tempetes"].append({"col": 4, "lig": 3})
    etat["zones_x"].add(cible)  # la case tempête est aussi une zone X
    executer_mouvement(etat, drone, cible, set())
    assert drone["batterie"] == bat_avant - (1 + COUT_ZONE_X), (
        f"Attendu {bat_avant - (1 + COUT_ZONE_X)}, got {drone['batterie']}"
    )


def test_tempete_batterie_zero_met_hors_service():
    """Drone avec exactement 1 batterie + collision tempête → hors_service=True et bloque=2."""
    etat, drone = _etat_minimal()
    drone["col"], drone["lig"] = 3, 3
    drone["batterie"] = 1  # coût normal = 1 → batterie tombe à 0
    cible = (4, 3)
    etat["tempetes"].append({"col": 4, "lig": 3})
    executer_mouvement(etat, drone, cible, set())
    assert drone["batterie"] == 0
    assert drone["hors_service"] is True, "Drone à 0 batterie doit être hors service"
    assert drone["bloque"] == 2, "Drone hors service + tempête doit rester bloqué 2 tours"


# ---------------------------------------------------------------------------
# Tests recharge hôpital
# ---------------------------------------------------------------------------

def test_recharge_hopital():
    """Un drone sur l'hôpital est rechargé de RECHARGE_HOPITAL."""
    etat, drone = _etat_minimal()
    hopital = etat["hopital"]
    drone["col"], drone["lig"] = hopital
    drone["batterie"] = 5
    drones_recharges = set()
    appliquer_recharges_hopital(etat, drones_recharges)
    assert drone["batterie"] == min(drone["batterie_max"], 5 + RECHARGE_HOPITAL)


def test_recharge_hopital_pas_double():
    """Un drone ne peut pas être rechargé deux fois le même tour."""
    etat, drone = _etat_minimal()
    hopital = etat["hopital"]
    drone["col"], drone["lig"] = hopital
    drone["batterie"] = 5
    drones_recharges = set()
    appliquer_recharges_hopital(etat, drones_recharges)
    bat_apres_1ere = drone["batterie"]
    appliquer_recharges_hopital(etat, drones_recharges)  # 2e appel
    assert drone["batterie"] == bat_apres_1ere  # pas de deuxième recharge


# ---------------------------------------------------------------------------
# Tests propagation zones X
# ---------------------------------------------------------------------------

def test_propager_zones_x_retourne_une_ligne_ou_zero():
    """propager_zones_x retourne une liste de 0 ou 1 élément."""
    etat = initialiser_partie()
    etat["tour"] = 5  # PROPAGATION_FREQUENCE = 5
    logs = propager_zones_x(etat)
    assert len(logs) <= 1


def test_propager_zones_x_pas_sur_hopital():
    """Les zones X ne se propagent jamais sur l'hôpital."""
    from config import PROPAGATION_FREQUENCE
    etat = initialiser_partie()
    hopital = etat["hopital"]
    # Placer des zones X tout autour de l'hôpital
    col, lig = hopital
    for dc in (-1, 0, 1):
        for dl in (-1, 0, 1):
            pos = (col + dc, lig + dl)
            if pos != hopital:
                etat["zones_x"].add(pos)
    etat["tour"] = PROPAGATION_FREQUENCE
    propager_zones_x(etat)
    assert hopital not in etat["zones_x"]


# ---------------------------------------------------------------------------
# Tests fin de partie
# ---------------------------------------------------------------------------

def test_verifier_fin_victoire():
    """Victoire quand tous les survivants sont sauvés."""
    etat = initialiser_partie()
    for s in etat["survivants"].values():
        s["etat"] = "sauve"
    assert verifier_fin_partie(etat) is True
    assert etat["victoire"] is True


def test_verifier_fin_defaite_tours():
    """Défaite quand le nombre de tours max est dépassé."""
    from config import NB_TOURS_MAX
    etat = initialiser_partie()
    etat["tour"] = NB_TOURS_MAX + 1
    assert verifier_fin_partie(etat) is True
    assert etat["victoire"] is False


def test_verifier_fin_defaite_tous_hs():
    """Défaite quand tous les drones sont hors service."""
    etat = initialiser_partie()
    for d in etat["drones"].values():
        d["hors_service"] = True
    assert verifier_fin_partie(etat) is True
    assert etat["victoire"] is False


def test_partie_en_cours():
    """Aucune fin de partie si conditions non remplies."""
    etat = initialiser_partie()
    assert verifier_fin_partie(etat) is False


# ---------------------------------------------------------------------------
# Point d'entrée direct (sans pytest)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        test_initialiser_partie_structure,
        test_initialiser_partie_tour_1,
        test_initialiser_partie_hopital_dans_grille,
        test_valider_mouvement_ok,
        test_valider_mouvement_hors_service,
        test_valider_mouvement_trop_loin,
        test_valider_mouvement_batterie_insuffisante,
        test_valider_mouvement_bloque,
        test_valider_mouvement_batiment,
        test_cout_deplacement_normal,
        test_cout_transport_survivant,
        test_cout_zone_x,
        # --- collision tempête (PR #11) ---
        test_tempete_bloque_drone_2_tours,
        test_tempete_consomme_batterie_deplacement_normal,
        test_tempete_consomme_batterie_avec_survivant,
        test_tempete_zone_x_consomme_batterie_supplementaire,
        test_tempete_batterie_zero_met_hors_service,
        # --- recharge ---
        test_recharge_hopital,
        test_recharge_hopital_pas_double,
        # --- propagation ---
        test_propager_zones_x_retourne_une_ligne_ou_zero,
        test_propager_zones_x_pas_sur_hopital,
        # --- fin de partie ---
        test_verifier_fin_victoire,
        test_verifier_fin_defaite_tours,
        test_verifier_fin_defaite_tous_hs,
        test_partie_en_cours,
    ]
    echecs = 0
    for t in tests:
        try:
            t()
            print(f"  ✓ {t.__name__}")
        except Exception as e:
            print(f"  ✗ {t.__name__} — {e}")
            echecs += 1
    print(f"\n{'TOUS LES TESTS PASSENT' if echecs == 0 else f'{echecs} ECHEC(S)'} ({len(tests)} tests)")
