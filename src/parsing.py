#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   parsing.py                                           :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/05 09:58:26 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/13 15:21:14 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import json
from typing import Any, cast

rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"


# *****************************************************************************
# *                              PROMPT                                       *
# *                                                                           *

def prompt_file_checker(prompt_file: str) -> list[dict[str, str]]:
    """Load and validate prompts from a JSON file.

    Args:
        prompt_file: Path to the JSON file containing prompts.

    Returns:
        List of validated prompt dictionaries.
    """
    try:

        with open(prompt_file, "r") as f:

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
        print(f"{r}[ERROR]{rs}: The {prompt_file} file is empty or misspelled")
        exit()

    except FileNotFoundError:
        print(f"{r}[ERROR]{rs}: File not found: {prompt_file}")
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

    return cast(list[dict[str, str]], prompts)


# *****************************************************************************
# *                             FUNCTION                                      *
# *                                                                           *

def function_file_checker(function_file: str) -> list[dict[str, Any]]:
    """Load and validate function definitions from a JSON file.

    Args:
        function_file: Path to the JSON file containing functions.

    Returns:
        List of validated function definition dictionaries.
    """

    args = ["name", "description"]
    types = ["string", "number", "integer", "boolean", "array",
             "object", "null"]
    valid_char = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "_"]

    try:

        with open(function_file, "r") as f:

            functions = json.load(f)
            if (len(functions) == 0):
                raise ValueError("The JSON file does not contain any "
                                 "functions")

            for fun in functions:

                if not (fun["name"].startswith("fn_")):
                    raise ValueError("Function names must begin with fn_")

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
                                             f"{fun['returns']}")

    except (IndexError, PermissionError, RuntimeError) as e:
        print(f"{r}[ERROR]{rs}: {e}")
        exit()

    except json.decoder.JSONDecodeError:
        print(f"{r}[ERROR]{rs}: The {function_file} file is empty "
              "or misspelled")
        exit()

    except FileNotFoundError:
        print(f"{r}[ERROR]{rs}: File not found: {function_file}")
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

    return cast(list[dict[str, Any]], functions)


# *****************************************************************************
# *                              PARSER                                       *
# *                                                                           *

def parser(
        pf: str,
        ff: str
) -> list[list[dict[str, Any]]]:
    """Return [prompts, functions] loaded from pf and ff.

    Args:
        pf: Path to the prompt file.
        ff: Path to the function definitions file.

    Returns:
        List of [prompts, functions].
    """
    return [prompt_file_checker(pf), function_file_checker(ff)]


# *****************************************************************************
# *                           ANSWER PARSER                                   *
# *                                                                           *

def answer_parser(answer: str, function: list[dict[Any, Any]]) -> list[Any]:
    """Parse 'fn_name@arg:val' LLM response into [name, params_dict].

    Args:
        answer: Raw LLM response string.
        function: List of function definition dicts.

    Returns:
        List of [function_name, params_dict].
    """
    list_answer: list[Any] = []
    dict_param: dict[str, Any] = {}

    try:

        answer_parts = answer.strip().split("@")
        if not answer_parts:
            return ["", {}]

        list_answer.append(answer_parts[0])

        for a in answer_parts[1:]:

            if ":" not in a:
                continue
            key, value = a.split(":", 1)

            for func in function:
                if (func["name"] == answer_parts[0]):
                    if (func["parameters"][key]["type"] == "number"):
                        dict_param[key] = float(value)
                    elif (func["parameters"][key]["type"] == "integer"):
                        dict_param[key] = int(value)
                    elif (func["parameters"][key]["type"] == "boolean"):
                        dict_param[key] = value.strip().lower() == "true"
                    else:
                        dict_param[key] = value.strip(" ").strip("\"")

            if not key:
                continue

        list_answer.append(dict_param)
    except (KeyError, IndexError):
        print("\n" + f"{r}[ERROR]{rs}: "
              "Function parameters cannot contain an “@” or \":\"")
        exit()

    return (list_answer)
