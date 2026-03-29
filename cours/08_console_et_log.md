# Module 08 — Console et log

## Concepts couverts

- `input()` — saisie utilisateur
- Parsing de commandes texte
- `str.split()`, `str.strip()`, `str.upper()`, `str.lower()`
- Expressions régulières légères avec `re.match()`
- `try` / `except` — gestion d'erreurs de saisie
- Écriture simultanée écran + fichier log

## Format des commandes

```
> D3         # sélectionner le drone D3
> T2         # sélectionner la tempête T2
> E6         # définir la cible (col=E, ligne=6)
> ok         # valider le mouvement
> annuler    # annuler la sélection
> next       # passer au tour suivant
```

## Code — parsing

```python
import re

def parser_commande(saisie: str) -> tuple:
    """
    Parse une commande console.
    
    Returns:
        ('drone', 'D3')           → sélection drone
        ('tempete', 'T2')         → sélection tempête
        ('coord', 'E', 6)         → cible
        ('ok',)                   → valider
        ('annuler',)              → annuler
        ('next',)                 → passer
        ('inconnu', saisie)       → commande non reconnue
    """
    s = saisie.strip().upper()
    
    # Sélection drone : D1 à D9
    if re.match(r'^D[1-9]$', s):
        return ('drone', s)
    
    # Sélection tempête : T1 à T9
    if re.match(r'^T[1-9]$', s):
        return ('tempete', s)
    
    # Coordonnée cible : lettre + chiffre(s) ex: E6, A12
    m = re.match(r'^([A-L])(\d{1,2})$', s)
    if m:
        col = m.group(1)
        try:
            row = int(m.group(2))
            return ('coord', col, row)
        except ValueError:
            pass
    
    if s == 'OK':
        return ('ok',)
    if s == 'ANNULER':
        return ('annuler',)
    if s == 'NEXT':
        return ('next',)
    
    return ('inconnu', saisie)


def saisie_securisee(prompt: str = '> ') -> str:
    """Saisie avec gestion d'interruption clavier (Ctrl+C)."""
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        return 'next'
```

## Format du log

```
T[nn] P[n] [D|T]  [ID] [départ]→[arrivée]  [bat:x→y]  [surv:x]  [EVENEMENT]

Exemples :
T04 P1 D  D3 B7→E6    bat:6→5    surv:—
T04 P1 D  D2 D5→D5    BLOQUÉ(T2) bat:—     surv:S3
T04 P1 T  T1 J2→K2
T05 P1 D  D4 E7→A12   bat:5→4    surv:S3   LIVRAISON +1pt
T05 P1 D  D6 F12→—    bat:0      HS
```

```python
def formater_log_deplacement(tour: int, joueur: int, entite,
                              ancien_col: int, ancien_row: int,
                              evenements: list) -> str:
    """Génère la ligne de log pour un déplacement."""
    COLS = 'ABCDEFGHIJKL'
    type_e = 'D' if hasattr(entite, 'batterie') else 'T'
    dep = f"{COLS[ancien_col]}{ancien_row + 1}"
    arr = entite.position_str
    ligne = f"T{tour:02d} P{joueur} {type_e}  {entite.id:<3} {dep}→{arr}"
    
    if type_e == 'D':
        bat_str = f"bat:{entite.batterie + 1}→{entite.batterie}"
        surv_str = f"surv:{entite.survivant.id if entite.survivant else '—'}"
        ligne += f"    {bat_str:<12} {surv_str}"
    
    for ev in evenements:
        if ev[0] == 'BLOQUE':
            ligne += f"    BLOQUÉ({ev[2]})"
        elif ev[0] == 'LIVRAISON':
            ligne += f"    LIVRAISON +1pt"
        elif ev[0] == 'HS':
            ligne += f"    HS"
    
    return ligne
```

## Exercices du module

Voir `exercices/ex_08_console.py`

## Tips et best practices

- **`try/except` sur toute saisie `input()`** — l'utilisateur peut envoyer Ctrl+C.
- **Normalise la casse immédiatement** : `saisie.strip().upper()` dès l'entrée.
- **Log = source de vérité** : ce qui est dans le fichier doit être identique à ce qui est affiché.
- **`re.match()` pour les patterns simples**, pas besoin de regex compliquées.

## Références

- [Docs Python — re](https://docs.python.org/fr/3/library/re.html)
- [Real Python — Regular Expressions in Python](https://realpython.com/regex-python/)
- [Real Python — Python Exceptions](https://realpython.com/python-exceptions/)

## Prompts IA

> *« Comment utiliser try/except en Python pour gérer proprement les erreurs de saisie utilisateur ? »*

> *« Explique-moi les expressions régulières Python avec re.match() pour valider des saisies simples. »*

> *« Comment écrire dans un fichier log en Python en même temps qu'on affiche à l'écran ? »*
