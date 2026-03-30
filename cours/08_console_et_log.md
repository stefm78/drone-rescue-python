# Module 08 — Console et log

## Concepts couverts

- `input()` — saisie utilisateur
- Parsing de commandes texte
- `str.split()`, `str.strip()`, `str.upper()`, `str.lower()`
- Expressions régulières avec `re.match()` — syntaxe de base
- `try` / `except` — gestion d'erreurs de saisie
- Écriture simultanée écran + fichier log

## Format des commandes

```
> D3       ← sélectionner le drone D3
> T2       ← sélectionner la tempête T2
> E6       ← définir la cible (colonne E, ligne 6)
> ok       ← valider le mouvement
> annuler  ← annuler la sélection
> next     ← passer au tour suivant
```

## Lien avec le projet

### Expressions régulières — syntaxe utile

```
^          début de chaîne
$          fin de chaîne
[A-L]      une lettre de A à L
\d         un chiffre
\d{1,2}    1 ou 2 chiffres
D[1-9]     D suivi d'un chiffre 1-9
(...)      groupe capturant → m.group(1)
```

```python
import re

def parser_commande(saisie: str) -> tuple:
    """
    Parse une commande console.
    Retourne un tuple dont le premier élément indique le type :
      ('drone', 'D3')        ← sélection drone
      ('tempete', 'T2')      ← sélection tempête
      ('coord', 'E', 6)      ← cible colonne str + ligne int
      ('ok',)                ← valider
      ('annuler',)           ← annuler
      ('next',)              ← passer
      ('inconnu', saisie)    ← commande non reconnue
    """
    s = saisie.strip().upper()

    if re.match(r'^D[1-9]$', s):
        return ('drone', s)

    if re.match(r'^T[1-9]$', s):
        return ('tempete', s)

    # Coordonnée cible : lettre A-L + 1 ou 2 chiffres (ex: E6, A12)
    m = re.match(r'^([A-L])(\d{1,2})$', s)
    if m:
        colonne = m.group(1)          # str : 'A'..'L'
        try:
            ligne = int(m.group(2))   # int : 1..12
            if 1 <= ligne <= 12:
                return ('coord', colonne, ligne)
        except ValueError:
            pass

    if s == 'OK':      return ('ok',)
    if s == 'ANNULER': return ('annuler',)
    if s == 'NEXT':    return ('next',)

    return ('inconnu', saisie)


def saisie_securisee(prompt: str = '> ') -> str:
    """Saisie avec gestion d'interruption clavier (Ctrl+C / EOF)."""
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        return 'next'   # action sûre par défaut
```

### Format du log

```
T[nn] P[n] [D|T]  [ID] [départ]→[arrivée]  [bat:x→y]  [surv:id]  [EVÉNEMENT]

Exemples :
T04 P1 D  D3 B7→E6    bat:6→5    surv:—
T04 P1 D  D2 D5→D5    BLOQUÉ(T2) bat:—      surv:S3
T04 P1 T  T1 J2→K2
T05 P1 D  D4 E7→A12   bat:5→4    surv:S3   LIVRAISON +1pt
```

```python
def formater_log_deplacement(tour: int, joueur: int, entite,
                              col_avant: str, lig_avant: int,
                              evenements: list) -> str:
    """Génère la ligne de log pour un déplacement."""
    type_e = 'D' if hasattr(entite, 'batterie') else 'T'
    dep = f"{col_avant}{lig_avant}"
    arr = entite.position_str   # colonne + ligne actuels
    ligne = f"T{tour:02d} P{joueur} {type_e}  {entite.identifiant:<3} {dep}→{arr}"

    if type_e == 'D':
        bat = getattr(entite, 'batterie', '?')
        surv = entite.survivant.identifiant if entite.survivant else '—'
        ligne += f"    bat:{bat+1}→{bat:<2}   surv:{surv}"

    for ev in evenements:
        if ev[0] == 'BLOQUE':
            ligne += f"    BLOQUÉ({ev[2]})"
        elif ev[0] == 'LIVRAISON':
            ligne += f"    LIVRAISON +1pt"
        elif ev[0] == 'HS':
            ligne += f"    HS"

    return ligne
```

## Erreurs classiques

**Erreur 1 — `input()` sans `try/except` → crash sur Ctrl+C**
```python
# ❌ KeyboardInterrupt si l'utilisateur appuie sur Ctrl+C
commande = input('> ')

# ✅
try:
    commande = input('> ')
except (KeyboardInterrupt, EOFError):
    commande = 'next'
```

**Erreur 2 — Ne pas normaliser la casse avant de comparer**
```python
# ❌ 'Next', 'NEXT', 'next' ne matchent pas tous
if saisie == 'next':
    ...

# ✅ Normaliser dès l'entrée
s = saisie.strip().upper()
if s == 'NEXT':
    ...
```

**Erreur 3 — `re.match` vs `re.search` : match ancre au début, pas à la fin**
```python
# ❌ match réussit sur 'D3XYZ' car il ne vérifie pas la fin !
import re
if re.match(r'D[1-9]', 'D3XYZ'):   # True ! — il faut '$'
    print('drone')  # s'affiche à tort

# ✅ Toujours ancrer avec ^ et $
if re.match(r'^D[1-9]$', 'D3XYZ'):  # False
    print('drone')
```

**Erreur 4 — Log incohérent avec l'affichage**
```python
# ❌ Écrire dans le log AVANT que l'action soit vraiment exécutée
ecrire_log('D3 se déplace vers E6')   # log
ok, msg = valider(...)                  # validation après !

# ✅ Logger APRES validation + exécution
ok, msg = valider(...)
if ok:
    evenements = executer(...)
    ecrire_log(formater_log(...))
```

## Exercice de compréhension

**Q1.** Que retourne `parser_commande('e6')` ?
<details><summary>Réponse</summary>

`('coord', 'E', 6)` — la saisie est normalisée en majuscules (`strip().upper()`), donc `'e6'` devient `'E6'`, reconnu par le pattern `^([A-L])(\d{1,2})$`.
</details>

**Q2.** Pourquoi `re.match(r'^D[1-9]$', s)` et pas juste `s.startswith('D')` ?
<details><summary>Réponse</summary>

`startswith('D')` accepterait `'D10'`, `'DRONE'`, `'D'`… Le pattern `^D[1-9]$` garantit exactement : D, puis un seul chiffre de 1 à 9, rien d'autre.
</details>

**Q3.** À quel moment écrire dans le fichier log ?
<details><summary>Réponse</summary>

Après la validation ET l'exécution, jamais avant. Le log doit refléter l'état réel du jeu, pas les intentions.
</details>

## Exercices du module

Voir `exercices/ex_08_console.py`

## Tips et best practices

- **`try/except` sur toute saisie `input()`** — l'utilisateur peut envoyer Ctrl+C.
- **Normalise la casse immédiatement** : `saisie.strip().upper()` dès l'entrée.
- **Ancre toujours tes regex** avec `^` et `$`.
- **Log = source de vérité** : logger après exécution, jamais avant.
- **`re.match()` pour les patterns simples**, pas besoin de regex complexes.

## Références

- [Docs Python — re](https://docs.python.org/fr/3/library/re.html)
- [Real Python — Regular Expressions in Python](https://realpython.com/regex-python/)
- [Real Python — Python Exceptions](https://realpython.com/python-exceptions/)

## Prompts IA

> *« Comment utiliser try/except en Python pour gérer proprement les erreurs de saisie utilisateur ? »*

> *« Explique-moi les expressions régulières Python avec re.match() pour valider des saisies simples. »*

> *« Comment écrire dans un fichier log en Python en même temps qu'on affiche à l'écran ? »*
