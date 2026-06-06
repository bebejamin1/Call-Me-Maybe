#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   main.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/04 13:02:05 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/05 15:59:51 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from llm_sdk import Small_LLM_Model
import numpy as np


def main() -> None:
    answer: str = ""  # noqa

    llm = Small_LLM_Model()

    input: str = "quel est la couleur du ciel ?"

    tok = llm.encode(input)
    token = np.array(tok.cpu())

    logits = llm.decode(token)
    print(logits)


if __name__ == "__main__":
    main()
