"""Tool classes for function calling."""

import inspect
import re
from dataclasses import dataclass
from importlib import import_module
from typing import Callable, TypedDict, get_type_hints


class Parameter(TypedDict):
    """Details of a parameter."""

    name: str
    type: str
    description: str
    required: bool


type ParameterDetails = dict[str, Parameter]


@dataclass
class Tool:
    """A tool that can be called via LLMs."""

    name: str
    function: Callable
    description: str
    parameters: ParameterDetails

    def __str__(self) -> str:  # pragma: no cover
        """Get the string representation of the tool."""
        return self.name

    @staticmethod
    def get_tool(mod: str, fn: str) -> Callable:
        """Get a tool."""
        try:
            module = import_module(mod)
            func = getattr(module, fn)
        except AttributeError:
            raise ValueError(f"Function {fn} not found in module {mod}.")
        except ImportError:
            raise ValueError(f"Module {mod} not found.")

        return func

    @staticmethod
    def get_description(function: Callable) -> str:
        """Extract the tool description from the docstring."""
        doc = inspect.getdoc(function)
        if doc is None:
            raise ValueError(f"Function {function} has no docstring.")

        lines = doc.splitlines()
        if not lines:
            raise ValueError(f"Function {function} has no docstring.")

        return lines[0]

    @staticmethod
    def get_parameters(function: Callable) -> ParameterDetails:
        """Get the parameters for the tool function."""

        signature = inspect.signature(function)
        type_hints = get_type_hints(function, include_extras=True)
        details: ParameterDetails = dict()

        for name, param in signature.parameters.items():
            try:
                details[name] = {
                    "name": name,
                    "type": "",
                    "description": type_hints[name].__metadata__,
                    "required": False,
                }
            except AttributeError:
                raise ValueError(f"Parameter {name} missing metadata.")

            # Check whether the parameter is required
            if param.kind in (param.VAR_KEYWORD, param.VAR_POSITIONAL):
                raise ValueError(
                    "Tool functions cannot have unbound parameters like *args or **kwargs."
                )
            if param.kind == param.POSITIONAL_ONLY:
                details[name]["required"] = True
            elif param.kind in (param.POSITIONAL_OR_KEYWORD, param.KEYWORD_ONLY):
                if param.default is param.empty:
                    details[name]["required"] = True
        return details

    @classmethod
    def from_dotted_name(cls, name: str) -> "Tool":
        """Create a tool from a dotted name."""

        module_name, _, function_name = name.rpartition(".")
        if not module_name:
            raise ValueError(
                "Please provide a complete path including the module and function names."
            )

        function = cls.get_tool(module_name, function_name)
        description = cls.get_description(function)
        parameters = cls.get_parameters(function)
        return cls(function_name, function, description, parameters)
