#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   function.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/11 09:07:49 by bbeaurai            #+#    #+#            #
#   Updated: 2026/06/13 12:02:01 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


"""
Defines the FunctionDef class that represents function metadata including
name, description, parameters, and return types. Provides factory methods
for creating instances from JSON function definitions.
"""

from pydantic import BaseModel, Field
from typing import Any

rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"


class FunctionDef(BaseModel):
    """
    Pydantic model representing a function definition.

    Attributes:
        name: Function name (1-50 characters), typically prefixed with "fn_".
        description: Function description (1-512 characters).
        parameters: List of parameter strings in "name: type" format.
        returns: Return type as a string, or None.
        nb_para: Number of parameters (must be positive).
    """

    name: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=512)
    parameters: list[str] = []
    returns: str | None = None
    nb_para: int = Field(gt=0)

    @classmethod
    def f_create(cls, function: dict[str, Any]) -> "FunctionDef":
        """
        Create a FunctionDef instance from a function dictionary.

        Extract function information from a dictionary and construct a
        FunctionDef.
        Parameters are formatted as "name: type" strings from the input
        dictionary.

        Args:
            function: Dictionary with keys "name", "description", "parameters",
                and "returns". Parameters value must be a dict mapping
                parameter
                names to dicts with "type" keys.

        Returns:
            A new FunctionDef instance.

        Raises:
            ValueError: If validation fails on any field constraints.
            KeyError: If required keys are missing from the function
            dictionary.
            SystemExit: If an error occurs.
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
        """
        Generate a formatted string representation of the function definition.

        Returns:
            String containing formatted name, description, parameters,
            and count.
        """
        return (
            f"name: {self.name}" + "\n"
            f"description: {self.description}" + "\n"
            f"parameters: {', '.join(self.parameters)}" + "\n"
            f"number of parameters {self.nb_para}" + "\n\n"
               )
