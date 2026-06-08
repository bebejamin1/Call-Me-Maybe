#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   main.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/04 13:02:05 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/08 10:12:01 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from llm_sdk import Small_LLM_Model
import numpy as np
import sys

# The sky is -> blue
# Capital of France is -> Paris


# def main() -> None:
#     llm = Small_LLM_Model()

#     text: str = "la couleur du ciel est"

#     ids = llm.encode(text)

#     logits = llm.get_logits_from_input_ids(ids[0].tolist())

#     best_token_id = int(np.argmax(logits))

#     answer = llm.decode([best_token_id])

#     print(answer)

def main() -> None:
    llm = Small_LLM_Model()

    text: str = "La coleur du ciel est "
    max_new_tokens: int = 100

    ids = llm.encode(text)
    token_ids = ids[0].tolist()

    try:

        for _ in range(max_new_tokens):
            logits = llm.get_logits_from_input_ids(token_ids)
            next_id = int(np.argmax(logits))
            token_ids.append(next_id)
            answer = llm.decode(token_ids)

            print("\033[H\033[2J", end="", flush=True)
            print(answer)
            print(f"Token: ({_})")

    except KeyboardInterrupt:
        print("Termined minish")


if __name__ == "__main__":
    main()
