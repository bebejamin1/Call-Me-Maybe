#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __main__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/12 15:59:56 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/13 14:38:23 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import argparse
from main import main

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--functions_definition",
                   default="data/input/functions_definition.json")
    p.add_argument("--input",
                   default="data/input/function_calling_tests.json")
    p.add_argument("--output",
                   default="data/output/function_calling_results.json")
    args = p.parse_args()
    main(args.functions_definition, args.input, args.output)
