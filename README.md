# Discord Slot Ping Limiter Bot

Ce bot Discord permet de créer des "slots" (canaux) avec un vendeur assigné, où le nombre de mentions `@here` et `@everyone` est limité par canal. Si une limite est dépassée, les permissions de l’auteur du message sont restreintes.

## Fonctionnalités

- Création dynamique de slots (canaux) via une commande slash `/new_slot`.
- Attribution d’un vendeur responsable du slot.
- Limitation du nombre de mentions `@here` et `@everyone` par canal.
- Suppression des messages et restriction des permissions si la limite est dépassée.
- Réinitialisation automatique des compteurs de pings chaque jour à minuit.

## Commandes

### `/new_slot`

- **Paramètres :**
  - `vendeur` : Membre responsable du slot.
  - `nom` : Nom du canal à créer.
  - `category` : Catégorie Discord où sera créé le canal.
  - `ping_max_here` : Nombre maximum de mentions `@here` autorisées.
  - `ping_max_everyone` : Nombre maximum de mentions `@everyone` autorisées.

## Installation

1. Clonez ce dépôt.
2. Installez les dépendances :
   ```bash
   pip install -U discord.py 
