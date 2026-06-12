#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   main.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/04 13:02:05 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/12 10:44:54 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import numpy as np  # noqa

from src.parsing import parser
from src.function import FunctionDef
from src.llm import speak_llm

rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"


def main() -> None:

    prompt_file = "function_calling_tests.json"
    function_file = "functions_definition.json"
    output_file = "function_calling_results.json"  # noqa

    list_files = parser(prompt_file, function_file)
    func_list = ""

    try:

        for func in list_files[1]:
            func_list += FunctionDef.f_create(func).show_function()
            # func_list.append(FunctionDef.f_create(func).show_function())

        # for prompt in list_files[0]:
        prompt = list_files[0][0]["prompt"]
        speak_llm(func_list, prompt)

    except KeyboardInterrupt:
        print("Termined minish")

    except RuntimeError as e:
        print(f"{r}[ERROR]{rs}: {e}")

    except AttributeError:
        print(f"{r}[ERROR]{rs}: An issue has been detected in the JSON "
              "function definitions")
        exit()


if __name__ == "__main__":
    main()
