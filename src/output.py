#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   output.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/10 16:03:53 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/12 14:15:38 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os
import json  # noqa

from src.parsing import answer_parser

rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"


def gen_display(prompt: str, answer: str) -> None:
    pass


def gen_json_file(prompt: str, answer: str, output_file: str) -> None:

    try:

        with open(os.path.join(f"data/input/{output_file}"), "w") as f:
            print(f)

            {
                "prompt": f"{prompt}",
                "name": f"{a}",  # noqa
                "parameters": f"{parameters}"  # noqa
            }

    except ValueError as e:
        print(f"{r}[ERROR]{rs}: {e}")


def gen_output(prompt: str, answer: str, output_file: str) -> None:

    answer = answer_parser(answer)

    gen_json_file(prompt, answer, output_file)
    gen_display(prompt, answer)
