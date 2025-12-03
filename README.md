# Mini-Projet Supinfo – Jeu de stratégie en Python

Note obtenue: **90/100**

## Résumé

Ce projet est un jeu de stratégie à deux joueurs, développé en Python avec la bibliothèque Tkinter. L’objectif est de déplacer ses pièces (reine et tours) et de capturer celles de l’adversaire selon des règles précises, sur un plateau carré.

Le projet utilise une approche orientée objet stricte, avec une interface graphique complète.

---

## Règles du jeu

- Deux joueurs s’affrontent sur un plateau `n x n` (valeur paire, par défaut `8x8`).
- Chaque joueur commence avec :
  - 1 Reine
  - `(n² / 4) - 1` Tours
- **Reine** : se déplace comme aux échecs (orthogonal et diagonal), sans capture.
- **Tour** : se déplace comme aux échecs (orthogonal uniquement), et peut capturer :
  - Si la tour et la reine forment deux coins opposés d’un rectangle,
    et qu’une tour adverse est sur l’un des deux autres coins, elle est capturée.
- Les reines ne peuvent pas être capturées.
- Un joueur perd lorsqu’il ne lui reste plus que **2 pièces ou moins** (reine incluse).

---

## Fonctionnalités

- Choix de la taille du plateau (entre 6 et 12, uniquement pair)
- Affichage du plateau et des pièces
- Indication du joueur en cours
- Sélection des pièces uniquement valides via la souris
- Déplacement et captures selon les règles
- Alternance des tours
- Détection automatique de la victoire
- Fin de partie avec affichage du résultat et redémarrage possible
- Séparation claire entre logique et interface graphique

---

## Contraintes techniques

- **Langage** : Python
- **Interface graphique** : Tkinter (obligatoire)
- **Architecture** : Programmation orientée objet
- **Encapsulation stricte**
- Aucune autre bibliothèque graphique n’est autorisée
- Le non-respect des règles techniques entraîne l’échec du projet

---

## Bonus (facultatifs)

- Affichage des coups possibles
- Sauvegarde/chargement de la partie
- Animations visuelles ou sons
- Mode contre IA (aléatoire ou basique)

---

## Modalités de rendu

- Travail en **binôme obligatoire**
- **Plagiat ou recours à une IA** interdits → note **0**
- Le projet doit être rendu sous la forme d’une **archive `.zip` contenant le code source**
- Une **soutenance orale** est prévue (voir les consignes du campus)

