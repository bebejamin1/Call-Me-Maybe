#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   main.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/04 13:02:05 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/13 10:46:17 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import time
import os

from src.parsing import parser, answer_parser
from src.function import FunctionDef
from src.llm import speak_llm, load_model
from src.output import gen_output, gen_display

rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"


def main() -> None:

    prompt_file = "function_calling_tests.json"
    function_file = "functions_definition.json"
    output_file = "function_calling_results.json"

    list_files = parser(prompt_file, function_file)
    func_list = ""
    list_answer = []

    try:

        if not (prompt_file.endswith(".json")
                and function_file.endswith(".json")
                and output_file.endswith(".json")):
            raise ValueError("One of the input/output files is not a "
                             ".json file")

        for func in list_files[1]:
            func_list += FunctionDef.f_create(func).show_function()

        llm = load_model()

        os.system('cls' if os.name == 'nt' else 'clear')

        start = time.time()

        for prompt in list_files[0]:
            answer = answer_parser(speak_llm(func_list, prompt["prompt"], llm))
            gen_display(prompt["prompt"], answer)
            list_answer.append(answer)

        gen_output(list_files[0], list_answer, output_file)

    except KeyboardInterrupt:
        print("STOP STOPPING ME")

    except RuntimeError as e:
        print(f"{r}[ERROR]{rs}: {e}")

    except AttributeError:
        print(f"{r}[ERROR]{rs}: An issue has been detected in the JSON "
              "function definitions")
        exit()

    except ValueError as e:
        print(f"{r}[ERROR]{rs}: {e}")

    finally:
        end = time.time()
        times = end - start
        if (times > 60):
            print("\n" + f'Elapsed: {times / 60:.2f} minutes' + "\n")
        else:
            print("\n" + f'Elapsed: {times:.2f} seconds' + "\n")


if __name__ == "__main__":
    main()
