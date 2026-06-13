#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   output.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/10 16:03:53 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/13 14:48:30 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os
import json
from typing import Any

bn = "\033[0;33m"
be = "\033[38;5;67m"
rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"


def gen_display(prompt: Any, answer: list[Any]) -> None:
    """Print prompt and function call result to stdout.

    Args:
        prompt: The user's request string.
        answer: List of [function_name, params_dict].
    """

    if isinstance(prompt, list):
        return None

    print("\n" + "".center(79, "="))
    print(f" {bn + prompt + rs} ".center(79 + len(rs + bn), "="))

    print("\n" + f"{be + answer[0] + rs}")
    for k, v in answer[1].items():
        print(f"{be}{k}: {v}{rs}")


def gen_json_file(prompt: list[dict[str, Any]], answer: list[Any],
                  output_file: str) -> None:
    """Write prompts and answers to a JSON file at output_file.

    Args:
        prompt: List of prompt dicts with a "prompt" key.
        answer: List of [function_name, params_dict].
        output_file: Destination file path.
    """

    list_output: list[dict[str, Any]] = []

    try:

        for pro, ans in zip(prompt, answer):
            list_output.append({
                "prompt": pro["prompt"],
                "name": ans[0],
                "parameters": ans[1]
                    })
        parent = os.path.dirname(output_file)
        if parent:
            os.makedirs(parent, exist_ok=True)

        with open(output_file, "w") as f:
            json.dump(list_output, f, indent=2)

    except ValueError as e:
        print(f"{r}[ERROR]{rs}: {e}")


def gen_output(prompt: list[dict[str, Any]], answer: list[Any],
               output_file: str) -> None:
    """Write function calling results to output_file.

    Args:
        prompt: List of prompt dicts.
        answer: List of [function_name, params_dict].
        output_file: Destination file path.
    """

    gen_json_file(prompt, answer, output_file)
