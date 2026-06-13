#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   llm.py                                               :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/11 15:47:04 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/13 11:43:18 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


"""
Provides functions to load small language models and generate responses
with constrained beam search decoding for function selection tasks.
"""

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

# constrained decoding


def load_model() -> Any:
    """
    Load and initialize the Small LLM Model.

    Attempts to import and instantiate the Small_LLM_Model from the llm_sdk.
    Exits with error message if import fails.

    Returns:
        An instance of Small_LLM_Model from llm_sdk.

    Raises:
        SystemExit: If the llm_sdk import fails.
    """
    try:
        from llm_sdk import Small_LLM_Model  # type: ignore[attr-defined]
        return Small_LLM_Model()
    except (ImportError, NameError):
        print("\n" + f"{r}[ERROR]{rs} You must run the code as follows:"
              "\n" + "uv run main.py or make" + "\n")
        sys.exit(1)


def speak_llm(function: str, prompt: str, llm: Any) -> str:
    """
    Generate LLM response for function selection with constrained decoding.

    Build a specialized prompt that instructs the LLM to select the most
    appropriate function and extract its parameters from a user request.
    Use constrained decoding (beam search with constraint) to generate
    exactly one alternative token at each step until a newline is
    encountered.

    Args:
        function: Formatted string containing available function
            definitions.
        prompt: The user's request text.
        llm: Loaded language model instance with encode, decode, and
            get_logits_from_input_ids methods.

    Returns:
        The LLM-generated response string, stripped of trailing
        whitespace. Expected format: "function_name@arg1:value1@arg2:value2"
        or "no function was found".
    """
    max_new_tokens: int = 100

    system_prompt: str = (
        "You are a function-selection system. Your only goal is to"
        " pick, from the available functions, the one that best "
        "matches the user's request, and to extract its arguments "
        "from that request.\n"
        "Here are the available functions. Each one is described by"
        " its name, its description, its parameters and their "
        "count:\n"
        f"\n{function}\n"
        "For the user's request, you must:\n"
        "- choose the name of the most appropriate function from "
        "the list above\n"
        "- fill in each parameter with the correct value extracted "
        "from the request, respecting its type\n"
        "- You must use the correct names for the function "
        "arguments, If the argument is a put a; if it is n, "
        "put n; and so on.\n\n"
        "If there is no function that matches the prompt, no "
        "function was found"
        "Examples:\n"
        "function_name@arg1:value1@arg2:value2\n"
        "Request: What is the sum of 2 and 3?\n"
        "Response: fn_add_numbers@a:2.0@b:3.0\n"
        "Request:  fw\n"
        "Response: no function was found\n"
        f"Request: {prompt}\n"
        "Response:"
    )

    ids = llm.encode(system_prompt)
    token_ids = ids[0].tolist()
    prompt_len = len(token_ids)

    result = ""
    for _ in range(max_new_tokens):
        logits = np.array(
            llm.get_logits_from_input_ids(token_ids),
            dtype=np.float64)
        max_id = int(np.argmax(logits))
        logits[:] = -np.inf
        logits[max_id] = 0.0
        next_id = int(np.argmax(logits))

        token_ids.append(next_id)
        result = llm.decode(token_ids[prompt_len:])
        if "\n" in result:
            break

    return result.split("\n")[0].strip()
