# Client IA pour Jeu

Un framework Python pour développer un client IA qui communique avec un serveur de jeu via TCP/IP.

## Structure du Projet

```
game_ai_client/
│à─ __init__.py          # Exports du package
│à─ connection.py        # Gestion de la connexion TCP
│à─ ai_client.py         # Logique de prise de décision IA
└─ utils/
    │à─ __init__.py      # Exports des utilitaires
    │à─ config.py        # Paramètres de configuration
    └─ logger.py        # Utilitaires de journalisation
main.py                  # Point d'entrée
```

## Fonctionnalités

- Communication TCP/IP avec le serveur de jeu
- Modèle de connexion singleton
- Traitement des messages JSON
- Système de journalisation configurable
- Support des arguments en ligne de commande
- Suivi de l'état du jeu
- Framework extensible de prise de décision IA

## Prérequis

- Python 3.8+

## Installation

Clonez le dépôt et installez les dépendances :

```bash
# Aucune dépendance externe requise pour les fonctionnalités de base
```

## Utilisation

Exécutez le client avec les paramètres par défaut :

```bash
python main.py
```

Configurez la connexion au serveur :

```bash
python main.py --host game-server.example.com --port 9000
```

Définissez le niveau de journalisation :

```bash
python main.py --log-level DEBUG
```

## Extension de la Logique IA

Pour implémenter votre propre logique IA, modifiez la méthode `make_decision` dans la classe `AIClient` :

```python
def make_decision(self) -> Dict[str, Any]:
    # Votre logique IA ici
    # Analysez self.game_state et prenez des décisions
    
    return {
        "action": "votre_action",
        "parameters": {
            # Paramètres d'action
        }
    }
```

## Licence

MIT
