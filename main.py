#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   main.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/04 13:02:05 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/08 10:57:10 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import numpy as np

g = "\033[32m\033[1m\033[1m"
r = "\033[31m\033[5m\033[1m"
rp = "\033[31m"
bn = "\033[0;33m"
be = "\033[38;5;67m"
rs = "\033[0m"

try:

    from llm_sdk import Small_LLM_Model

except (ImportError, NameError):
        print("\n" + f"{r}[ERROR]{rs} You must run the code as follows:"
              "\n" + f"{be}uv run main.py{rs} or {be}make{rs}" + "\n")
        exit()

# The sky is -> blue
# Capital of France is -> Paris

def main() -> None:
    llm = Small_LLM_Model()

    text: str = "/"
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
