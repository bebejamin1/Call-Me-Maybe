#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   function.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/11 09:07:49 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/11 14:17:54 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# for param_name, param_def in func.parameters.items():
#     # param_name = "a", param_def.type = "number"
#     # → restreindre les tokens à des valeurs numériques

from typing import Literal

from pydantic import BaseModel, Field

AllowedType = Literal[
    "string", "number", "integer", "boolean", "array", "object", "null"
                     ]

_TYPE_MAP: dict[str, str] = {
    "number": "float",
    "integer": "int",
    "string": "str",
    "boolean": "bool",
    "array": "list",
    "object": "dict",
    "null": "None",
}


class ParamDef(BaseModel):

    type: AllowedType


class FunctionDef(BaseModel):

    name: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    description: str = Field(min_length=1, max_length=512)
    parameters: dict[str, ParamDef] = {}
    returns: ParamDef | None = None
    nb_para: int = Field(gt=0)

    def f_create(self, function: dict[str, dict]) -> None:

        try:

            self.name = function["name"]
            self.description = function["description"]

            for p in function["parameters"]:
                print(p)

        except ValueError as e:
            print(e)
