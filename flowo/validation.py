from __future__ import annotations
import re
from typing import Set

RESERVED_WORDS: Set[str] = {
    "and",
    "false",
    "mod",
    "not",
    "or",
    "pi",
    "true",
    "boolean",
    "integer",
    "real",
    "string",
    "abs",
    "cos",
    "random",
    "tan",
    "tostring",
    "arccos",
    "int",
    "sgn",
    "tochar",
    "toreal",
    "arcsin",
    "len",
    "sin",
    "tocode",
    "arctan",
    "log",
    "size",
    "tofixed",
    "char",
    "log10",
    "sqrt",
    "tointeger",
    "arccosh",
    "cosh",
    "arcsinh",
    "sinh",
    "arctanh",
    "tanh",
    "ln",
    "eof",
}


def validate_variable_name(name: str) -> None:
    parts = [p.strip() for p in name.split(",")]
    for part in parts:
        _validate_single_name(part)


def _validate_single_name(name: str) -> None:
    if not name:
        raise ValueError("Variable name cannot be empty")

    if name[0].isdigit():
        raise ValueError(f"Variable name '{name}' cannot start with a number")

    if not name.isalnum():
        raise ValueError(
            f"Variable name '{name}' cannot contain symbols or underscores (no snake_case)"
        )

    if name.lower() in RESERVED_WORDS:
        raise ValueError(f"Variable name '{name}' is a reserved keyword in Flowgorithm")


def validate_expression_target(target: str) -> None:
    match = re.match(r"^([a-zA-Z][a-zA-Z0-9]*)(\[.*\])?$", target)
    if not match:
        raise ValueError(f"Invalid variable or array access: '{target}'")

    base_name = match.group(1)
    _validate_single_name(base_name)
