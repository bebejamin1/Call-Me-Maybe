#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   output.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/10 16:03:53 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/13 11:43:13 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


"""
Handles formatting and displaying function calling results, and generates
JSON output files with the inference results.
"""

import os
import json
from typing import Any

bn = "\033[0;33m"
be = "\033[38;5;67m"
rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"


def gen_display(prompt: Any, answer: list[Any]) -> None:
    """
    Display the prompt and LLM response in formatted output.

    Print the user's prompt and the parsed function name with its parameters
    to stdout with color formatting. Skip output if prompt is a list.

    Args:
        prompt: The user's request string (or list to skip output).
        answer: A list containing [function_name_str, parameters_dict].
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
    """
    Write results to a JSON output file.

    Combine prompts and answers into a structured format and write to a JSON
    file.
    Create parent directories if needed.

    Args:
        prompt: List of prompt dictionaries, each with a "prompt" key.
        answer: List of answer lists, each containing
        [function_name, params_dict].
        output_file: Path to the output JSON file.

    Raises:
        ValueError: If there is an error writing the JSON file.
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
    """
    Generate output file with function calling results.

    Wrapper function that calls gen_json_file to write results.

    Args:
        prompt: List of prompt dictionaries.
        answer: List of answer lists with function names and parameters.
        output_file: Path to the output JSON file.
    """
    gen_json_file(prompt, answer, output_file)
