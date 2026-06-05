# 📞 Call Me Maybe — Checklist d'apprentissage

> Introduction au *function calling* dans les LLMs — tout ce qu'il faut comprendre et savoir expliquer pour la défense.

---

## 📦 Imports de référence

```python
import re
import argparse
from pathlib import Path
import json
from llm_sdk import Small_LLM_Model
import numpy as np
import math
from collections import defaultdict
from enum import Enum
```

---

## 🎯 Concepts fondamentaux

- [ ] Expliquer pourquoi le function calling est utile : interagir avec des APIs, exécuter du code, extraire des données structurées de texte brut
- [ ] Comprendre comment un LLM génère du texte **token par token**
- [ ] Maîtriser le mécanisme central :
  produire les logits → identifier les tokens valides → mettre les logits invalides à **−∞** → échantillonner uniquement parmi les valides
- [ ] Comprendre que la contrainte assure **deux choses** :
  - JSON syntaxiquement valide
  - conformité au schéma (ex : un champ `number` n'accepte que des tokens formant un entier ou un flottant)
- [ ] Expliquer pourquoi cette approche est fiable à **~100 %** là où le prompting seul échoue (~30 % sur un petit modèle)
- [ ] ⚠️ **Point critique** : la solution ne doit **pas** espérer que le modèle produise du bon JSON spontanément — c'est explicitement ce qu'ils ne veulent pas

---

## 🔤 Tokenisation

- [ ] Différence entre **mots** et **tokens** (sous-unités, BPE / SentencePiece)
- [ ] Les tokens incluent souvent les espaces de tête (le symbole `Ġ`)
- [ ] Conversion tokens → **input IDs** (identifiants numériques)
- [ ] Utiliser le fichier **vocabulary JSON** pour mapper input_ids ↔ représentations textuelles des tokens *(crucial pour savoir quels tokens sont valides à chaque étape)*

---

## 🧰 Le SDK fourni (`llm_sdk`)

Savoir exactement ce que fait chaque méthode et laquelle utiliser :

- [ ] `get_logits_from_input_ids(input_ids)` → renvoie les logits bruts
- [ ] `get_path_to_vocabulary_json()` → chemin du fichier de correspondance
- [ ] `encode(text)` → texte vers liste de token IDs
- [ ] `decode(token_ids)` → optionnel, inverse
- [ ] ⚠️ **Interdiction** d'utiliser les méthodes/attributs **privés** du package

---

## 🔁 La boucle de génération à implémenter

Le squelette à savoir coder **et** expliquer :

- [ ] Construire le prompt → tokeniser → input IDs
- [ ] Appeler le modèle pour obtenir les logits
- [ ] Appliquer le masque de contrainte (tokens invalides → −∞)
- [ ] Sélectionner le token (généralement le plus probable)
- [ ] Ajouter le token généré et répéter jusqu'à la fin du JSON
- [ ] Savoir comment la **machine à états** suit la structure JSON attendue
  *(où en est-on : nom de clé ? valeur ? nombre ? string ?)*
- [ ] Comment la sélection de la fonction se fait **via le LLM** et pas avec des heuristiques *(interdit)*

---

## 🐍 Compétences Python / outillage exigées

- [ ] **Python 3.10+**
- [ ] **pydantic** pour toutes les classes (validation)
- [ ] **numpy** et **json** autorisés
- [ ] Conformité **flake8**
- [ ] **Type hints** partout + passer **mypy** sans erreur (module `typing`)
- [ ] **Docstrings** PEP 257 (style Google ou NumPy)
- [ ] Gestion d'exceptions avec `try-except` + **context managers** pour les ressources
- [ ] ⚠️ **Interdits** : dspy, pytorch, huggingface, transformers, outlines, etc.

---

## ⚙️ Environnement et build

- [ ] Créer un venv et installer **numpy** + **pydantic** avec **uv**
- [ ] `pyproject.toml` + `uv.lock` *(le correcteur fait juste `uv sync`)*
- [ ] **Makefile** avec les règles : `install`, `run`, `debug`, `clean`, `lint`, `lint-strict`
- [ ] Connaître les commandes exactes de la règle `lint` (flake8 + flags mypy)
- [ ] `.gitignore` pour les artefacts Python

---

## 📥📤 Entrées / Sorties

- [ ] Lire les deux fichiers :
  - `function_calling_tests.json` (prompts)
  - `functions_definition.json` (fonctions disponibles)
- [ ] Comprendre la structure de `functions_definition.json` : `name`, `parameters` (avec types), `returns`, `description`
- [ ] Produire `function_calling_results.json` avec exactement les clés : `prompt`, `name`, `parameters`
- [ ] Connaître les **règles de validation** : JSON valide, types conformes au schéma, pas de clés en trop, tous les arguments requis présents
- [ ] Gérer la CLI :
  ```bash
  uv run python -m src [--functions_definition ...] [--input ...] [--output ...]
  ```
  avec les dossiers par défaut `data/input/` et `data/output/`

---

## 🛡️ Robustesse *(testé à l'évaluation)*

- [ ] JSON invalide ou fichier manquant → géré proprement, **jamais de crash**
- [ ] Messages d'erreur clairs
- [ ] Cas limites à tester : strings vides, grands nombres, caractères spéciaux, mauvais types, prompts ambigus, fonctions à plusieurs paramètres
- [ ] ⚠️ **Ne jamais hardcoder** des solutions basées sur les exemples *(les fichiers changent à la review)*

---

## 📊 Performance visée

- [ ] **90 %+** de sélection de fonction et extraction d'arguments corrects
- [ ] **100 %** de JSON valide et conforme au schéma
- [ ] Tous les prompts traités en **moins de 5 minutes**

---

## 📝 Le README *(obligatoire et noté)*

À rédiger **en anglais** :

- [ ] Première ligne en italique avec le format imposé :
  *This project has been created as part of the 42 curriculum by...*
- [ ] Section **Description**
- [ ] Section **Instructions**
- [ ] Section **Resources** (avec comment l'IA a été utilisée)
- [ ] Explication détaillée de l'algorithme de **décodage contraint**
- [ ] **Décisions de design**
- [ ] **Analyse de performance**
- [ ] **Difficultés rencontrées**
- [ ] **Stratégie de test**
- [ ] **Exemples d'usage**


Je comprend

llm -> une machine qui predit le mot suivant -> le token suivant

token -> decoupage de mot pour mieux comprendre
lettre par lettre trop lent, mot entier vocabulaire trop grand et inconnus
donc token sous lalgorithme BPE byte pair Encoding
chaque token a un ID unique (numero unique)

logits -> score 
```
token 90 ("{")   : 8.3   ← score élevé, très probable
token 14990      : 0.1
token 279        : -2.4  ← score bas, peu probable
```

comment on choisi le token ?
Greedy on prend le token au score le plus eleve pour le projet
et Sampling (avec tempereaure) on tire aleatoirement un score plus ou moins avec
des delta pour sage ou creatif.



![génération autorégressive](image.png)

float16 pr GPU vs float32 pr CPU

sdk -> software development kit (Kit de développement logiciel)

llm predit du texte


Hugging Face
[Hugging face page](https://huggingface.co/spaces?filter=reachy_mini)
github pour les IA permet de chopper plein de model deja entrainer
[IA used for project](https://huggingface.co/Qwen/Qwen3-0.6B)

transformers
il sait comment les couches de neurones sont organisées
il sait Comment tokeniser le texte avec le bon tokenizer du modèle

PyTorch
bibliotheque de calcul mathematique sur des matrices
import torch
remplace numpy pour utiliser la puissance des GPU
[torch doc](https://www.python-simple.com/python-torch/torch-intro.php)
[torch doc complete](https://pypi.org/project/torch/)


L'analogie en une phrase
torch = le moteur et les roues (la mécanique de calcul).
transformers = la voiture complète, conçue pour un modèle précis, posée sur ce moteur.



```bash
User: "What is the sum of 40 and 2?"
Traditional LLM: "The sum of 40 and 2 is 42."
Function Calling System:
{
"function": "add_numbers",
"arguments": {"a": 40, "b": 2}
}
```