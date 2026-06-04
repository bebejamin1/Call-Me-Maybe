# Call-Me-Maybe
```
import re
import argparse
from pathlib import Path
import json
from llm_sdk import Small_LLM_Model
import numpy as np
import math
from collections import defaultdict
import Enum
```
```
Savoir expliquer pourquoi c'est utile (interagir avec des APIs, exécuter du code, extraire des données structurées de texte brut)
Comprendre comment un LLM génère du texte token par token
Maîtriser le mécanisme central : produire les logits → identifier les tokens valides → mettre les logits invalides à −∞ → échantillonner uniquement parmi les valides
Comprendre que la contrainte doit assurer deux choses : JSON syntaxiquement valide ET conformité au schéma (ex : un champ number ne peut recevoir que des tokens formant un entier ou un flottant)
Savoir expliquer pourquoi cette approche est fiable à ~100% là où le prompting seul échoue (~30% avec un petit modèle)
⚠️ Point critique : ta solution ne doit PAS espérer que le modèle produise du bon JSON spontanément. C'est explicitement ce qu'ils ne veulent pas.
```
```
Comprendre la tokenisation

Différence entre mots et tokens (sous-unités, BPE / SentencePiece)
Le fait que les tokens incluent souvent les espaces de tête (le symbole "Ġ")
La conversion tokens → input IDs (identifiants numériques)
Comment utiliser le fichier vocabulary JSON pour mapper input_ids ↔ représentations textuelles des tokens (c'est crucial pour savoir quels tokens sont valides à chaque étape)
```

```
Le SDK fourni (llm_sdk)
Tu dois savoir exactement ce que fait chaque méthode et laquelle utiliser :

get_logits_from_input_ids(input_ids) → renvoie les logits bruts
get_path_to_vocabulary_json() → chemin du fichier de correspondance
encode(text) → texte vers liste de token IDs
decode(token_ids) → optionnel, inverse
⚠️ Interdiction d'utiliser les méthodes/attributs privés du package
```

```
La boucle de génération à implémenter
C'est le squelette que tu dois pouvoir coder et expliquer :

Construire le prompt → tokeniser → input IDs
Appeler le modèle pour obtenir les logits
Appliquer le masque de contrainte (mettre les tokens invalides à −∞)
Sélectionner le token (généralement le plus probable)
Ajouter le token généré et répéter jusqu'à la fin du JSON


Savoir comment ta machine à états suit la structure JSON attendue (où on en est : dans un nom de clé ? une valeur ? un nombre ? une string ?)
Comment la sélection de la fonction se fait via le LLM et pas avec des heuristiques (interdit)
```

```
Compétences Python / outillage exigées

Python 3.10+
pydantic pour toutes les classes (validation) — savoir t'en servir
numpy et json autorisés
Conformité flake8
Type hints partout + passer mypy sans erreur (connaître le module typing)
Docstrings PEP 257 (style Google ou NumPy)
Gestion d'exceptions avec try-except + context managers pour les ressources
⚠️ Interdits : dspy, pytorch, huggingface, transformers, outlines, etc.
```

```
Environnement et build

Créer un venv et installer numpy + pydantic avec uv
pyproject.toml + uv.lock (le correcteur fait juste uv sync)
Le Makefile avec les règles : install, run, debug, clean, lint, lint-strict
Connaître les commandes exactes de la règle lint (flake8 + flags mypy)
.gitignore pour les artefacts Python
```

```
Entrées / Sorties

Lire les deux fichiers : function_calling_tests.json (prompts) et functions_definition.json (fonctions disponibles)
Comprendre la structure de functions_definition.json : name, parameters (avec types), returns, description
Produire function_calling_results.json avec exactement les clés : prompt, name, parameters
Connaître les règles de validation : JSON valide, types conformes au schéma, pas de clés en trop, tous les arguments requis présents
Gérer la commande CLI : uv run python -m src [--functions_definition ...] [--input ...] [--output ...] avec les dossiers par défaut data/input/ et data/output/
```

```
Robustesse (testé à l'évaluation)

JSON invalide ou fichier manquant → géré proprement, jamais de crash
Messages d'erreur clairs
Cas limites à tester : strings vides, grands nombres, caractères spéciaux, mauvais types, prompts ambigus, fonctions à plusieurs paramètres
⚠️ Ne jamais hardcoder des solutions basées sur les exemples (les fichiers changent à la review)
```

```
Performance visée

90%+ de sélection de fonction et extraction d'arguments corrects
100% de JSON valide et conforme au schéma
Tous les prompts traités en moins de 5 minutes
```

```
Le README (obligatoire et noté)
Tu dois pouvoir rédiger toutes ces sections :

Première ligne en italique avec le format imposé "This project has been created as part of the 42 curriculum by..."
Description, Instructions, Resources (avec comment tu as utilisé l'IA)
Explication de ton algorithme de décodage contraint en détail
Décisions de design, analyse de performance, difficultés rencontrées, stratégie de test, exemples d'usage
En anglais
```
