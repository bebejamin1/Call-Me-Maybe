#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   llm.py                                               :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/11 15:47:04 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/13 14:47:48 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os
import sys
import numpy as np
from typing import Any

os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"
os.environ["HF_HUB_VERBOSITY"] = "error"

rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"


def load_model() -> Any:
    """Load and return a Small_LLM_Model instance.

    Returns:
        An instance of Small_LLM_Model from llm_sdk.
    """

    try:
        from llm_sdk import Small_LLM_Model  # type: ignore[attr-defined]
        return Small_LLM_Model()
    except (ImportError, NameError):
        print("\n" + f"{r}[ERROR]{rs} You must run the code as follows:"
              "\n" + "uv run main.py or make" + "\n")
        sys.exit(1)


def _build_name_trie(sp: str, functions: list[dict], llm: Any) -> dict:
    """Build a trie of token sequences for valid function names.

    Args:
        sp: System prompt string used for encoding context.
        functions: List of function definition dicts.
        llm: Loaded language model instance.

    Returns:
        Trie mapping token IDs to sub-tries.
    """

    valid_names = [f["name"] for f in functions] + ["no function was found"]
    prompt_len = len(llm.encode(sp)[0].tolist())
    trie: dict = {}
    for name in valid_names:
        tokens = llm.encode(sp + " " + name)[0].tolist()[prompt_len:]
        node = trie
        for tok in tokens:
            if tok not in node:
                node[tok] = {}
            node = node[tok]
    return trie


def speak_llm(function: str, prompt: str, llm: Any,
              functions: list[dict]) -> str:
    """Select a function via constrained decoding and return the raw response.

    Args:
        function: Formatted string of available function definitions.
        prompt: The user's natural language request.
        llm: Loaded language model instance.
        functions: List of function definition dicts.

    Returns:
        String like "fn_name@arg1:val1" or "no function was found".
    """

    max_new_tokens: int = 100

    sp: str = ("You are a function-selection system. Your only goal is to"
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
               "request, respecting its type " + "\n\n"
               "If there is no function that matches the prompt, no "
               "function was found"
               "You must use the correct function argument names: if the "
               "argument is `a`, use `a`; if it's `n`, use `n`; if it's "
               "`template`, use `template`, and so on." + "\n"
               "Examples:" + "\n"
               "function_name@arg1:value1@arg2:value2"
               "Request: \"What is the sum of 2 and 3?\"" + "\n"
               "Response: fn_add_numbers@a:2.0@b:3.0" + "\n"
               "Request: \" fw'\"" + "\n"
               "Response: no function was found" + "\n"
               f"Request: \"{prompt}\"" + "\n"
               "Response:")

    ids = llm.encode(sp)
    token_ids = ids[0].tolist()
    prompt_len = len(token_ids)

    trie = _build_name_trie(sp, functions, llm)
    current_node: dict | None = trie
    constrained = True

    result = ""
    for _ in range(max_new_tokens):
        logits = np.array(
            llm.get_logits_from_input_ids(token_ids),
            dtype=np.float64)

        if constrained and current_node:
            valid_next = set(current_node.keys())
            mask = np.full(len(logits), -np.inf)
            for tok in valid_next:
                mask[tok] = logits[tok]
            logits = mask

        next_id = int(np.argmax(logits))
        token_ids.append(next_id)

        if constrained and current_node is not None:
            current_node = current_node.get(next_id)
            if not current_node:
                constrained = False

        result = llm.decode(token_ids[prompt_len:])
        if "\n" in result:
            break

    return (result.split("\n")[0].strip())
