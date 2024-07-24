"""Tool classes for function calling."""

import inspect
import re
from dataclasses import dataclass
from importlib import import_module
from typing import Callable, TypedDict


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
    def get_parameter_details(function: Callable) -> ParameterDetails:
        """Get the parameter details from the docstring."""

        doc = inspect.getdoc(function)
        # This should not happen as it should be caught in get_description, but the assert will make mypy happy
        assert doc is not None, "docstring is required."
        details: ParameterDetails = dict()

        regex = re.compile(
            r"^\s*:param\s+((?P<type>\w+)(\s+))?(?P<name>\w+):(\s*)(?P<description>.*)$",
            re.M,
        )
        for match in regex.finditer(doc):
            if match["name"] in details:
                raise ValueError(f"Duplicate parameter name: {match['name']}")
            details[match["name"]] = {
                "name": match["name"],
                "type": match["type"],
                "description": match["description"],
                "required": False,
            }

        return details

    @staticmethod
    def get_parameters(function: Callable) -> ParameterDetails:
        """Get the parameters for the tool function."""

        details = Tool.get_parameter_details(function)
        signature = inspect.signature(function)

        # Since we check for duplication later, we can assume all are documented if the lengths match
        assert len(details) == len(
            signature.parameters
        ), "Count mismatch between docstring `:param`s and signature"

        for name, param in signature.parameters.items():
            # Verify that the parameter is documented
            if name not in details:
                raise ValueError(f"Parameter {name} not documented in the docstring.")

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
