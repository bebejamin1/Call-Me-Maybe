#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   parsing.py                                           :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/05 09:58:26 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/10 16:58:23 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import json
import os

rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"

# *****************************************************************************
# *                              PROMPT                                       *
# *                                                                           *


def prompt_file_checker(prompt_file: str) -> bool:
    try:

        with open(os.path.join(f"data/input/{prompt_file}"), "r") as f:

            prompts = json.load(f)
            if (len(prompts) == 0):
                raise ValueError("The JSON file does not contain any prompts")

            for p in prompts:

                if (len(p["prompt"]) <= 0):
                    raise ValueError(f"prompt ({p}) is not in the "
                                     "correct format")

    except (IndexError, PermissionError, RuntimeError) as e:
        print(f"{r}[ERROR]{rs}: {e}")
        exit()

    except json.decoder.JSONDecodeError:
        print(f"{r}[ERROR]{rs}: The {prompt_file} file is empty")
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

    return (True)

# *****************************************************************************
# *                             FUNCTION                                      *
# *                                                                           *


def function_file_checker(function_file: str) -> bool:
    args = ["name", "description"]
    types = ["string", "number", "integer", "boolean", "array",
             "object", "null"]

    try:

        with open(os.path.join(f"data/input/{function_file}"), "r") as f:

            functions = json.load(f)
            if (len(functions) == 0):
                raise ValueError("The JSON file does not contain any "
                                 "functions")

            for fun in functions:

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

    except (IndexError, PermissionError, RuntimeError) as e:
        print(f"{r}[ERROR]{rs}: {e}")
        exit()

    except json.decoder.JSONDecodeError:
        print(f"{r}[ERROR]{rs}: The {function_file} file is empty")
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
