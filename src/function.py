#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   function.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/11 09:07:49 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/13 14:47:59 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Pydantic model for function definitions loaded from JSON."""

from pydantic import BaseModel, Field
from typing import Any

rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"


class FunctionDef(BaseModel):

    """Validated representation of a function definition from JSON.

    Attributes:
        name: Function name prefixed with fn_.
        description: Human-readable description.
        parameters: List of "param: type" strings.
        returns: Return type string, or None.
        nb_para: Number of parameters.
    """

    name: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=512)
    parameters: list[str] = []
    returns: str | None = None
    nb_para: int = Field(ge=0)

    @classmethod
    def f_create(cls, function: dict[str, Any]) -> "FunctionDef":

        """Build a FunctionDef from a raw function definition dictionary.

        Args:
            function: Dict with name, description, parameters, returns.

        Returns:
            A new FunctionDef instance.
        """
        try:

            parameters: list[str] = []
            param_dict: dict[str, dict[str, str]] = function["parameters"]
            for k, v in param_dict.items():
                parameters.append(f"{k}: {v['type']}")

            return_dict: dict[str, str] = function["returns"]
            return cls(
                name=function["name"],
                description=function["description"],
                parameters=parameters,
                returns=return_dict["type"],
                nb_para=len(parameters),
                      )

        except (ValueError, KeyError) as e:
            print(f"{r}[ERROR]{rs}: {e}")
            exit()

    def show_function(self) -> str:
        """Return a formatted string with name, description, and parameters.

        Returns:
            Multi-line string describing the function for LLM prompting.
        """

        return (
            f"name: {self.name}" + "\n"
            f"description: {self.description}" + "\n"
            f"parameters: {', '.join(self.parameters)}" + "\n"
            f"number of parameters {self.nb_para}" + "\n\n"
               )
