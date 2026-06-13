#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   output.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/10 16:03:53 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/13 09:50:39 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os
import json

g = "\033[32m\033[1m\033[1m"
rp = "\033[31m"
bn = "\033[0;33m"
be = "\033[38;5;67m"
rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"


def gen_display(prompt: str, answer: str) -> None:

    if (isinstance(prompt, list)):
        return (None)

    print("\n" + "".center(79, "="))
    print(f" {prompt} ".center(79, "="))

    print("\n" + f"{answer[0]}")
    for k, v in answer[1].items():
        print(f"{k}: {v}")


def gen_json_file(prompt: str, answer: str, output_file: str) -> None:
    list_output = []

    try:

        for pro, ans in zip(prompt, answer):
            list_output.append({
                "prompt": f"{pro['prompt']}",
                "name": ans[0],
                "parameters": ans[1]
                    })
        if not (os.path.exists("data/output")):
            os.mkdir(os.path.join("data/output"))

        with open(os.path.join(f"data/output/{output_file}"), "w") as f:
            json.dump(list_output, f, indent=2)

    except ValueError as e:
        print(f"{r}[ERROR]{rs}: {e}")


def gen_output(prompt: str, answer: list, output_file: str) -> None:

    gen_json_file(prompt, answer, output_file)
