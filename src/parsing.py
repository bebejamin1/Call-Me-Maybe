#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   parsing.py                                           :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/05 09:58:26 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/08 16:42:33 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import json
import os

rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"

# verif answer est vide / permission

def json_checker(prompt_file: str, function_file: str) -> bool:
    try:

        with open(os.path.join(f"data/input/{prompt_file}"),
                               "r") as f:
            prompts = json.load(f)
            for p in prompts:
                print(p.keys(), p.values())

                if (p.keys() != "prompt" and len(p.values()) <= 0):
                    raise ValueError(f"prompt ({p}) is not in the "
                                     "correct format")

    except (FileNotFoundError, json.decoder.JSONDecodeError,
            IndexError, PermissionError) as e:
        print(f"{r}[ERROR]{rs}: {e}")
        return (False)

    except ValueError as e:
        print(f"{r}[ERROR]{rs}: {e}")
        return (False)

    return (True)

def parser(pf: str, ff: str, ) -> bool:

    prompt_file = pf
    function_file = ff

    if (json_checker(prompt_file, function_file)):
        return (True)
    return (False)


print(parser("function_calling_tests.json", "functions_definition.json"))
