#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   parsing.py                                           :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/05 09:58:26 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/09 15:56:38 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import json
import os

# verif bon format, permission, si le dossier existe
# number, string, boolean, etc.

rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"

# *****************************************************************************
# *                              PROMPT                                       *
# *                                                                           *

def prompt_file_checker(prompt_file: str) -> bool:
    try:

        with open(os.path.join(f"data/input/{prompt_file}"),
                               "r") as f:
            prompts = json.load(f)
            for p in prompts:

                if (len(p["prompt"]) <= 0):
                    raise ValueError(f"prompt ({p}) is not in the "
                                     "correct format")

    except (FileNotFoundError, json.decoder.JSONDecodeError,
            IndexError, PermissionError, RuntimeError) as e:
        print(f"{r}[ERROR]{rs}: {e}")
        exit()

    except ValueError as e:
        print(f"{r}[ERROR]{rs}: {e}")
        exit()

    except KeyError:
        print(f"{r}[ERROR]{rs}: You must specify exactly “prompt”")
        exit()

    except TypeError:
        print(f"{r}[ERROR]{rs}: The “function_calling_tests.json” file does "
              "not contain a list of dictionaries")
        exit()

    return (True)

# *****************************************************************************
# *                             FUNCTION                                      *
# *                                                                           *

def function_file_checker(function_file: str) -> bool:
    try:

        with open(os.path.join(f"data/input/{function_file}"),
                               "r") as f:
            prompts = json.load(f)
            for p in prompts:

                pass

    except (FileNotFoundError, json.decoder.JSONDecodeError,
            IndexError, PermissionError, RuntimeError) as e:
        print(f"{r}[ERROR]{rs}: {e}")
        exit()

    except ValueError as e:
        print(f"{r}[ERROR]{rs}: {e}")
        exit()

    except KeyError:
        print(f"{r}[ERROR]{rs}: You must specify exactly “prompt”")
        exit()

    except TypeError:
        print(f"{r}[ERROR]{rs}: The “function_calling_tests.json” file does "
              "not contain a list of dictionaries")
        exit()

    return (True)

# *****************************************************************************
# *                              PARSER                                       *
# *                                                                           *

def parser(pf: str, ff: str) -> bool:

    prompt_file = pf
    function_file = ff

    if (prompt_file_checker(prompt_file) and
            function_file_checker(function_file)):
        return (True)
    return (False)
