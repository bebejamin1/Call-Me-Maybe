#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   function.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/11 09:07:49 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/11 11:25:41 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# for param_name, param_def in func.parameters.items():
#     # param_name = "a", param_def.type = "number"
#     # → restreindre les tokens à des valeurs numériques

from typing import Literal

from pydantic import BaseModel, Field


class ParamDef(BaseModel):

    AllowedType = Literal[
        "string", "number", "integer", "boolean", "array", "object", "null"
                         ]

    type: AllowedType


class FunctionDef(BaseModel):

    name: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    description: str = Field(min_length=1, max_length=512)
    parameters: dict[str, ParamDef] = {}
    returns: ParamDef = None

    def f_create(function: dict[str, str]) -> None:

        pass
