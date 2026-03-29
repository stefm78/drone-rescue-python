# =============================================================================
# config.py — Paramètres globaux du jeu Drone Rescue
# Tous les réglages se trouvent ici. Modifier ces valeurs change le comportement
# du jeu sans toucher au code des autres modules.
# =============================================================================

# --- Grille ---
GRILLE_TAILLE = 12          # La grille est GRILLE_TAILLE x GRILLE_TAILLE (12x12)

# --- Entités ---
NB_DRONES = 6               # Nombre de drones (D1..D6)
NB_TEMPETES = 4             # Nombre de tempêtes (T1..T4)
NB_BATIMENTS = 20           # Nombre de bâtiments placés aléatoirement
NB_SURVIVANTS = 10          # Nombre de survivants à sauver
NB_ZONES_DANGER = 2         # Nombre de zones dangereuses X initiales

# --- Batterie des drones ---
BATTERIE_MAX = 20           # Capacité maximale de la batterie
BATTERIE_INIT = 10          # Batterie de départ

# --- Déplacements par tour ---
MAX_DEPL_DRONE = 3          # Nombre de cases max qu'un drone peut parcourir par tour
MAX_DEPL_TEMPETE = 2        # Nombre de déplacements max d'une tempête par tour

# --- Durée de partie ---
NB_TOURS_MAX = 20           # Nombre de tours avant défaite automatique

# --- Propagation des tempêtes ---
# Probabilité (entre 0.0 et 1.0) qu'une zone X se propage à un tour de propagation
PROBA_PROPAGATION = 0.3

# --- Propagation : fréquence ---
# Les zones X se propagent tous les PROPAGATION_FREQUENCE tours
PROPAGATION_FREQUENCE = 2

# --- Position fixe de l'hôpital ---
# L'hôpital est toujours en A12 (colonne 0, ligne 11 en index 0-based)
HOPITAL_COL = 0            # Index colonne : 0 = 'A'
HOPITAL_LIG = 11           # Index ligne   : 11 = ligne 12

# --- Fichier de log ---
LOG_FICHIER = "partie.log"  # Nom du fichier journal généré à la fin de partie
