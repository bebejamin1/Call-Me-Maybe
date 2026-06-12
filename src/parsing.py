#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   parsing.py                                           :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/05 09:58:26 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/12 10:02:20 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import json
import os

rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"

# *****************************************************************************
# *                              PROMPT                                       *
# *                                                                           *


def prompt_file_checker(prompt_file: str) -> list[dict]:
    try:

        with open(os.path.join(f"data/input/{prompt_file}"), "r") as f:

            prompts = json.load(f)
            if (len(prompts) == 0):
                raise ValueError("The JSON file does not contain any prompts")

            for p in prompts:

                if (len(p["prompt"]) <= 0):
                    raise ValueError(f"prompt ({p}) is not in the "
                                     "correct format")

            return (prompts)

    except (IndexError, PermissionError, RuntimeError) as e:
        print(f"{r}[ERROR]{rs}: {e}")
        exit()

    except json.decoder.JSONDecodeError:
        print(f"{r}[ERROR]{rs}: The {prompt_file} file is empty or misspelled")
        exit()

    except FileNotFoundError:
        print(f"{r}[ERROR]{rs}: Please create the following folders:" + "\n"
              f"data/input/{prompt_file}")
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

# *****************************************************************************
# *                             FUNCTION                                      *
# *                                                                           *


def function_file_checker(function_file: str) -> list[dict]:
    args = ["name", "description"]
    types = ["string", "number", "integer", "boolean", "array",
             "object", "null"]
    valid_char = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "_"]

    try:

        with open(os.path.join(f"data/input/{function_file}"), "r") as f:

            functions = json.load(f)
            if (len(functions) == 0):
                raise ValueError("The JSON file does not contain any "
                                 "functions")

            for fun in functions:

                for n in fun["name"]:
                    if (n not in valid_char):
                        raise ValueError("Function names must be in "
                                         "snake_case format")

                for a in args:
                    if not (isinstance(fun[a], str) and len(fun[a]) > 0):
                        raise ValueError(f"in {fun[a]} The argument is not a "
                                         "string or is empty")

                for v in fun["parameters"].values():

                    for k, t in v.items():
                        if (k != "type"):
                            raise ValueError("Parameters must be of a "
                                             f"specific type \"{k}\": \"{t}\"")

                    if (v["type"] not in types):
                        raise ValueError("Function parameters must be "
                                         "prototyped as follows: " + "\n"
                                         f"{v}")

                    for k, v in fun["returns"].items():
                        if (k != "type" or v not in types):
                            raise ValueError("The return is incorrect" + "\n"
                                             f"{fun["returns"]}")

            return (functions)

    except (IndexError, PermissionError, RuntimeError) as e:
        print(f"{r}[ERROR]{rs}: {e}")
        exit()

    except json.decoder.JSONDecodeError:
        print(f"{r}[ERROR]{rs}: The {function_file} file is empty "
              "or misspelled")
        exit()

    except FileNotFoundError:
        print(f"{r}[ERROR]{rs}: Please create the following folders:" + "\n"
              f"data/input/{function_file}")
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

# *****************************************************************************
# *                              PARSER                                       *
# *                                                                           *


def parser(pf: str, ff: str) -> list[list]:

    return [prompt_file_checker(pf), function_file_checker(ff)]
