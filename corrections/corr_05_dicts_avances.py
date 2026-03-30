# =============================================================================
# CORRECTION 05 — Dictionnaires avancés et sets
# =============================================================================


# -----------------------------------------------------------------------------
# EXERCICE 1 — Créer un drone (fonction factory)
# -----------------------------------------------------------------------------

def creer_drone(identifiant, col, lig, batterie_max=20, batterie_init=10):
    """Retourne un dict représentant un drone."""
    return {
        "id"          : identifiant,
        "col"         : col,
        "lig"         : lig,
        "batterie"    : batterie_init,
        "batterie_max": batterie_max,
        "survivant"   : None,   # None = ne porte personne
        "bloque"      : 0,      # 0 = libre
        "hors_service": False,
    }


if __name__ == "__main__":
    d = creer_drone("D1", 0, 5)
    assert d["id"] == "D1"
    assert d["batterie"] == 10
    assert d["batterie_max"] == 20
    assert d["survivant"] is None
    assert d["hors_service"] is False
    print("Ex1 OK")


# -----------------------------------------------------------------------------
# EXERCICE 2 — Dict de dicts : initialiser_drones
# -----------------------------------------------------------------------------

def initialiser_drones(nb=6, batterie_max=20, batterie_init=10):
    """Retourne {"D1": {...}, "D2": {...}, ...} avec nb drones."""
    drones = {}
    for i in range(nb):
        identifiant = f"D{i + 1}"
        # Drones placés sur la ligne 0, colonnes 0..nb-1
        drones[identifiant] = creer_drone(identifiant, i, 0,
                                          batterie_max, batterie_init)
    return drones
    # Note : on pourrait aussi utiliser un dict comprehension :
    # return {f"D{i+1}": creer_drone(f"D{i+1}", i, 0, ...) for i in range(nb)}


if __name__ == "__main__":
    drones = initialiser_drones(3)
    assert list(drones.keys()) == ["D1", "D2", "D3"]
    assert drones["D2"]["col"] == 1
    assert drones["D3"]["batterie"] == 10
    drones["D1"]["batterie"] -= 1
    assert drones["D1"]["batterie"] == 9
    print("Ex2 OK")


# -----------------------------------------------------------------------------
# EXERCICE 3 — Sets de tuples pour les zones X
# -----------------------------------------------------------------------------

def ajouter_zone_x(zones_x, col, lig):
    """Ajoute (col, lig) au set. Un set ignore les doublons."""
    zones_x.add((col, lig))


def retirer_zone_x(zones_x, col, lig):
    """Retire (col, lig) si présent. discard() ne plante pas si absent."""
    zones_x.discard((col, lig))


def est_zone_x(zones_x, col, lig):
    """Retourne True si (col, lig) est dans le set."""
    return (col, lig) in zones_x


if __name__ == "__main__":
    zones = set()
    ajouter_zone_x(zones, 3, 5)
    ajouter_zone_x(zones, 7, 2)
    ajouter_zone_x(zones, 3, 5)   # doublon — ignoré
    assert len(zones) == 2
    assert est_zone_x(zones, 3, 5) is True
    assert est_zone_x(zones, 0, 0) is False
    retirer_zone_x(zones, 3, 5)
    assert est_zone_x(zones, 3, 5) is False
    retirer_zone_x(zones, 9, 9)   # ne plante pas
    print("Ex3 OK")


# -----------------------------------------------------------------------------
# EXERCICE 4 — Accéder et modifier un dict de dicts
# -----------------------------------------------------------------------------

def drone_par_id(drones, identifiant):
    """Retourne le dict du drone ou None."""
    return drones.get(identifiant)   # .get() retourne None si clé absente


def drones_actifs(drones):
    """Retourne la liste des dicts de drones dont hors_service == False."""
    return [d for d in drones.values() if not d["hors_service"]]


def consommer_batterie(drone, cout=1):
    """Diminue la batterie de cout (min 0). Passe HS si batterie = 0."""
    drone["batterie"] = max(0, drone["batterie"] - cout)
    if drone["batterie"] == 0:
        drone["hors_service"] = True


if __name__ == "__main__":
    drones = initialiser_drones(4)
    d = drone_par_id(drones, "D2")
    assert d["id"] == "D2"
    assert drone_par_id(drones, "D9") is None
    assert len(drones_actifs(drones)) == 4
    drones["D3"]["hors_service"] = True
    assert len(drones_actifs(drones)) == 3
    drone = drones["D1"]
    for _ in range(10):
        consommer_batterie(drone)
    assert drone["batterie"] == 0
    assert drone["hors_service"] is True
    print("Ex4 OK")


# -----------------------------------------------------------------------------
# EXERCICE 5 — Tableau de bord aligné
# -----------------------------------------------------------------------------

def afficher_tableau_drones(drones):
    """Affiche le tableau de bord des drones avec colonnes alignées."""
    print(f"{'ID':<4}  {'Col':<4} {'Lig':<4} {'Bat':<6} {'Surv'}")
    for drone in drones.values():
        surv = drone["survivant"] if drone["survivant"] else "—"
        bat  = f"{drone['batterie']}/{drone['batterie_max']}"
        hs   = "  HS" if drone["hors_service"] else ""
        print(f"{drone['id']:<4}  {drone['col']:<4} {drone['lig']:<4} {bat:<6} {surv}{hs}")


if __name__ == "__main__":
    drones = initialiser_drones(3)
    drones["D1"]["batterie"] = 9
    drones["D3"]["batterie"] = 0
    drones["D3"]["hors_service"] = True
    drones["D2"]["survivant"] = "S2"
    afficher_tableau_drones(drones)
    print("Ex5 OK")
