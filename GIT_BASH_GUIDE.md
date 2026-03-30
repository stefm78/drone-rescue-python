# Guide Git & Bash — Drone Rescue Python

> Ce guide est pour toi si tu n'as jamais (ou peu) utilisé un terminal.
> Tu trouveras ici **toutes les commandes dont tu as besoin** pour travailler sur ce projet.

---

## 🖥️ Ouvrir un terminal

| Système | Comment faire |
|---------|---------------|
| **Windows** | Touche `Windows` → tape `Git Bash` → Entrée |
| **Windows** (alt.) | Dans VS Code : menu `Terminal` → `Nouveau terminal` |
| **macOS** | `Cmd + Espace` → tape `Terminal` → Entrée |
| **Linux** | `Ctrl + Alt + T` |

> 💡 **Git Bash sur Windows** simule un terminal Linux. Toutes les commandes ci-dessous fonctionnent dedans.

---

## 📍 Se repérer dans les dossiers

```bash
# Où suis-je ?
pwd

# Lister les fichiers du dossier courant
ls

# Lister avec les dossiers cachés et les détails
ls -la

# Aller dans un dossier
cd nom-du-dossier

# Aller dans un dossier par chemin complet
cd C:/Users/tonnom/Documents/drone-rescue-python

# Remonter d'un niveau (dossier parent)
cd ..

# Revenir à la racine de ton espace utilisateur
cd ~

# Effacer l'écran du terminal
clear
```

> 💡 **Astuce** : appuie sur `Tab` pour auto-compléter un nom de dossier ou fichier.

---

## 📥 Récupérer le projet (une seule fois)

```bash
# Télécharger le repo sur ton ordinateur
git clone https://github.com/stefm78/drone-rescue-python

# Entrer dans le dossier du projet
cd drone-rescue-python

# Vérifier que tout est là
ls
```

> Après `git clone`, tu as une copie complète du projet sur ton disque.
> Tu n'as besoin de faire ça **qu'une seule fois**.

---

## 🔄 Récupérer les dernières mises à jour

Le prof peut mettre à jour le projet (nouveaux exercices, corrections…).
Pour récupérer ces mises à jour :

```bash
# Se placer dans le dossier du projet (si pas déjà dedans)
cd drone-rescue-python

# Récupérer les mises à jour
git pull
```

> ⚠️ Fais toujours `git pull` en début de séance pour avoir la dernière version.

---

## ▶️ Lancer le jeu

```bash
# Depuis la racine du projet
python jeu/main.py
```

> Sur certains systèmes, utilise `python3` à la place de `python`.

---

## 🧪 Lancer les tests

```bash
# Lancer tous les tests automatisés
pytest tests/test_logique.py -v

# Sans pytest installé (mode direct)
python tests/test_logique.py
```

---

## 📝 Travailler sur tes exercices

```bash
# Voir quels fichiers tu as modifiés
git status

# Voir le détail des modifications dans un fichier
git diff exercices/ex_01.py

# Sauvegarder tes modifications ("prendre un instantané")
git add exercices/ex_01.py
git commit -m "ex01 : solution boucle for terminée"

# Sauvegarder tous les fichiers modifiés en une fois
git add .
git commit -m "exercices semaine 1 complétés"
```

> 💡 Un `commit`, c'est comme une **sauvegarde avec un message**. Si tu fais une bêtise, tu peux revenir en arrière.

---

## 🌿 Travailler sur sa propre branche (recommandé)

Pour ne pas écraser le travail des autres et garder `main` propre :

```bash
# Créer une nouvelle branche à ton nom
git checkout -b prenom-exercices

# Ex : git checkout -b marie-exercices

# Vérifier sur quelle branche tu es
git branch

# Changer de branche
git checkout main
git checkout marie-exercices
```

---

## 📤 Envoyer son travail sur GitHub

```bash
# Envoyer ta branche sur GitHub (première fois)
git push -u origin prenom-exercices

# Les fois suivantes, depuis ta branche
git push
```

---

## 🔍 Voir l'historique

```bash
# Voir les derniers commits (appuie sur 'q' pour quitter)
git log --oneline

# Version graphique compacte
git log --oneline --graph --all
```

---

## 🚑 Commandes de secours

```bash
# Annuler les modifications non sauvegardées sur un fichier
git checkout -- exercices/ex_01.py

# Annuler TOUTES les modifications non sauvegardées (⚠️ irréversible)
git checkout -- .

# Voir ce que fait une commande git
git help commit
git help pull
```

---

## 🐍 Commandes Python utiles

```bash
# Vérifier la version de Python installée
python --version
# ou
python3 --version

# Lancer un fichier Python
python exercices/ex_01.py

# Ouvrir le shell Python interactif (pour tester des bouts de code)
python
# Pour quitter : exit() ou Ctrl+D

# Installer une bibliothèque
pip install nom-bibliotheque

# Lister les bibliothèques installées
pip list
```

---

## ⚡ Raccourcis clavier du terminal

| Raccourci | Action |
|-----------|--------|
| `Tab` | Auto-complétion (nom de fichier / dossier) |
| `↑` / `↓` | Naviguer dans l'historique des commandes |
| `Ctrl + C` | Stopper un programme en cours |
| `Ctrl + L` | Effacer l'écran (= `clear`) |
| `Ctrl + D` | Quitter le shell Python ou le terminal |
| `Ctrl + A` | Aller au début de la ligne |
| `Ctrl + E` | Aller à la fin de la ligne |

---

## 📋 Récapitulatif — Les 10 commandes à connaître

```bash
# 1. Cloner le projet
git clone https://github.com/stefm78/drone-rescue-python

# 2. Entrer dans le dossier
cd drone-rescue-python

# 3. Récupérer les mises à jour
git pull

# 4. Voir où on en est
git status

# 5. Lancer le jeu
python jeu/main.py

# 6. Lancer les tests
pytest tests/test_logique.py -v

# 7. Sauvegarder ses modifs
git add .
git commit -m "message explicite"

# 8. Créer sa branche
git checkout -b prenom-exercices

# 9. Envoyer sur GitHub
git push

# 10. Voir l'historique
git log --oneline
```

---

## ❓ En cas de problème

1. **Lis le message d'erreur** — Git est très verbeux, il dit souvent quoi faire
2. **Copie-colle l'erreur** dans un moteur de recherche
3. **Prompts IA utiles :**

> *« Je suis débutant en Git. J'ai cette erreur : [colle l'erreur]. Que faire ? »*

> *« Explique-moi la commande `git rebase` en termes simples pour un débutant. »*

---

*Voir aussi : [cours/00_introduction.md](cours/00_introduction.md) pour le guide de démarrage du projet.*
