#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   llm.py                                               :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/11 15:47:04 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/14 08:56:59 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os
import sys
import json
import numpy as np
from typing import Any

os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"
os.environ["HF_HUB_VERBOSITY"] = "error"

rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"

_BPE_MAP = str.maketrans({"Ġ": " ", "Ċ": "\n"})


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


def _build_name_trie(
        sp: str, functions: list[dict[str, Any]], llm: Any) -> dict[int, Any]:
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
    trie: dict[int, Any] = {}
    for name in valid_names:
        tokens = llm.encode(sp + " " + name)[0].tolist()[prompt_len:]
        node = trie
        for tok in tokens:
            if tok not in node:
                node[tok] = {}
            node = node[tok]
    return trie


def _build_type_valid_tokens(
        vocab: dict[str, int], ptype: str) -> set[int]:
    """Return the set of token IDs valid for a given parameter type.

    Works like _build_name_trie but for value tokens: scans the vocabulary
    and keeps every token whose decoded characters are all legal for ptype.

    Args:
        vocab: BPE token string -> token ID mapping (from vocab file).
        ptype: Parameter type ('number', 'integer', 'boolean', 'string').

    Returns:
        Set of token IDs that can legally appear inside a value of ptype.
    """
    num_chars: set[str] = set("0123456789.+-eE")
    int_chars: set[str] = set("0123456789-")
    bool_words: set[str] = {"true", "false", "True", "False"}

    valid: set[int] = set()
    for bpe_str, tok_id in vocab.items():
        actual = bpe_str.translate(_BPE_MAP)
        stripped = actual.strip()
        if not stripped:
            continue
        if ptype == "number" and all(c in num_chars for c in stripped):
            valid.add(tok_id)
        elif ptype == "integer" and all(c in int_chars for c in stripped):
            valid.add(tok_id)
        elif ptype == "boolean" and stripped in bool_words:
            valid.add(tok_id)
        elif ptype == "string":
            valid.add(tok_id)
    return valid


def speak_llm(function: str, prompt: str, llm: Any,
              functions: list[dict[str, Any]]) -> str:
    """Select a function via constrained decoding and return the raw response.

    Phase 1 — function name: a trie restricts tokens to valid function names.
    Phase 2 — argument values: for each value segment (between ':' and the
    next '@' or newline), tokens are masked to those valid for the declared
    parameter type, mirroring the trie approach used for names.

    Args:
        function: Formatted string of available function definitions.
        prompt: The user's natural language request.
        llm: Loaded language model instance.
        functions: List of function definition dicts.

    Returns:
        String like 'fn_name@arg1:val1@arg2:val2' or 'no function was found'.
    """
    max_new_tokens: int = 150

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
    token_ids: list[int] = ids[0].tolist()
    prompt_len = len(token_ids)

    name_trie = _build_name_trie(sp, functions, llm)
    current_node: dict[int, Any] | None = name_trie
    name_done = False

    vocab_path: str = llm.get_path_to_vocab_file()
    with open(vocab_path, "r", encoding="utf-8") as vf:
        vocab: dict[str, int] = json.load(vf)

    type_tokens: dict[str, set[int]] = {
        ptype: _build_type_valid_tokens(vocab, ptype)
        for ptype in ("number", "integer", "boolean", "string")
    }
    at_nl_toks: set[int] = {
        tid for bpe, tid in vocab.items()
        if "@" in bpe.translate(_BPE_MAP) or "\n" in bpe.translate(_BPE_MAP)
    }

    selected_func: dict[str, Any] | None = None
    param_types: list[str] = []

    result = ""
    for _ in range(max_new_tokens):
        logits = np.array(
            llm.get_logits_from_input_ids(token_ids), dtype=np.float64)

        if not name_done and current_node is not None:
            valid_next = set(current_node.keys())
            mask = np.full(len(logits), -np.inf)
            for tok in valid_next:
                mask[tok] = logits[tok]
            logits = mask

        elif name_done and selected_func is not None:
            partial: str = llm.decode(token_ids[prompt_len:])
            parts = partial.split("@")

            if len(parts) > 1:
                last_seg = parts[-1]
                in_value = ":" in last_seg
                if in_value:
                    arg_idx = len(parts) - 2
                    if arg_idx < len(param_types):
                        ptype = param_types[arg_idx]
                        valid = type_tokens.get(ptype, set()) | at_nl_toks
                        mask = np.full(len(logits), -np.inf)
                        for tok in valid:
                            if tok < len(logits):
                                mask[tok] = logits[tok]
                        logits = mask

        next_id = int(np.argmax(logits))
        token_ids.append(next_id)

        if not name_done and current_node is not None:
            current_node = current_node.get(next_id)
            if not current_node:
                name_done = True
                generated: str = llm.decode(token_ids[prompt_len:]).strip()
                selected_func = next(
                    (f for f in functions if f["name"] == generated), None)
                if selected_func:
                    param_types = [
                        v["type"]
                        for v in selected_func["parameters"].values()
                    ]

        result = llm.decode(token_ids[prompt_len:])
        if "\n" in result:
            break

    return result.split("\n")[0].strip()
