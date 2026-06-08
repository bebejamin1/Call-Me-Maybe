#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   parsing.py                                           :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/05 09:58:26 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/08 11:23:06 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import json
import os

# verif answer est vide

_ROOT = os.path.join(os.path.dirname(__file__), "..")

def json_checker() -> bool:
    try:

        with open(os.path.join(_ROOT,
                               "data/input/function_calling_tests.json"),
                               "r") as f:
            prompt = json.load(f)
            print(prompt[0])

    except (FileNotFoundError, json.decoder.JSONDecodeError, IndexError) as e:
        print(e)
        return (False)

    return (True)

json_checker()
