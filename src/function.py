#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   function.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/11 09:07:49 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/12 10:21:34 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# for param_name, param_def in func.parameters.items():
#     # param_name = "a", param_def.type = "number"
#     # → restreindre les tokens à des valeurs numériques

from pydantic import BaseModel, Field

rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"


class FunctionDef(BaseModel):

    name: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=512)
    parameters: list[str] = []
    returns: str | None = None
    nb_para: int = Field(gt=0)

    @classmethod
    def f_create(cls, function: dict[str, dict]) -> "FunctionDef":

        try:

            parameters = []
            for k, v in function.get("parameters").items():
                parameters.append(f"{k}: {v["type"]}")

            return cls(
                name=function["name"],
                description=function["description"],
                parameters=parameters,
                returns=function["returns"]["type"],
                nb_para=len(parameters),
                      )

        except (ValueError, KeyError) as e:
            print(f"{r}[ERROR]{rs}: {e}")
            exit()

    def show_function(self) -> str:

        return (
            f"name: {self.name}" + "\n"
            f"description: {self.description}" + "\n"
            f"parameters: {", ".join(self.parameters)}" + "\n"
            f"number of parameters {self.nb_para}" + "\n\n"
               )
