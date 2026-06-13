#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   llm.py                                               :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/11 15:47:04 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/13 08:13:01 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os
import numpy as np

os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"
os.environ["HF_HUB_VERBOSITY"] = "error"


g = "\033[32m\033[1m\033[1m"
rp = "\033[31m"
bn = "\033[0;33m"
be = "\033[38;5;67m"
rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"


def speak_llm(function: str, prompt: str) -> str:

    max_new_tokens: int = 100
    prompt: str = ("You are a function-selection system. Your only goal is to"
                   " pick, from the available functions, the one that best "
                   "matches the "
                   "user's request, and to extract its arguments from that "
                   "request." + "\n"
                   "Here are the available functions. Each one is described by"
                   " its name, its description, its parameters and their "
                   "count:" + "\n"
                   "\n" + f"{function}" + "\n"
                   "For the user's request, you must:" + "\n"
                   "- choose the name of the most appropriate function from "
                   "the list above\n"
                   "- fill in each parameter with the correct value extracted "
                   "from the "
                   "request, respecting its type " + "\n"
                   "- You must use the correct names for the "
                   "function arguments, "
                   "If the argument is “a” put “a”; if it's “n,” "
                   "put “n”; and so on." + "\n\n"
                   "If there is no function that matches the prompt, no "
                   "function was found"
                   "Examples:" + "\n"
                   "function_name@arg1:value1@arg2:value2" + "\n"
                   "Request: \"What is the sum of 2 and 3?\"" + "\n"
                   "Response: fn_add_numbers@a:2.0@b:3.0" + "\n"
                   "Request: \" fw'\"" + "\n"
                   "Response: no function was found" + "\n"
                   f"Request: \"{prompt}\"" + "\n"
                   "Response:")

    try:

        from llm_sdk import Small_LLM_Model

        llm = Small_LLM_Model()

        ids = llm.encode(prompt)
        token_ids = ids[0].tolist()
        prompt_len = len(token_ids)

        for _ in range(max_new_tokens):
            logits = np.array(llm.get_logits_from_input_ids(token_ids),
                              dtype=np.float64)
            max_id = int(np.argmax(logits))
            logits[:] = -np.inf
            logits[max_id] = 0.0
            next_id = int(np.argmax(logits))

            token_ids.append(next_id)
            answer = llm.decode(token_ids[prompt_len:])
            if "\n" in answer:
                break

        return (answer.split("\n")[0].strip())

    except (ImportError, NameError):
        print("\n" + f"{r}[ERROR]{rs} You must run the code as follows:"
              "\n" + f"{be}uv run main.py{rs} or {be}make{rs}" + "\n")
        exit()
