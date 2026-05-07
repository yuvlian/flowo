from __future__ import annotations
from .models import Display

# Constants
PI: str = "pi"
TRUE: str = "true"
FALSE: str = "false"


# Mathematics
def Abs(n: Display | str) -> str:
    return f"Abs({n})"


def Arcsin(n: Display | str) -> str:
    return f"Arcsin({n})"


def Arccos(n: Display | str) -> str:
    return f"Arccos({n})"


def Arctan(n: Display | str) -> str:
    return f"Arctan({n})"


def Cos(n: Display | str) -> str:
    return f"Cos({n})"


def Int(n: Display | str) -> str:
    return f"Int({n})"


def Ln(n: Display | str) -> str:
    return f"Ln({n})"


def Log(n: Display | str) -> str:
    return f"Log({n})"


def Log10(n: Display | str) -> str:
    return f"Log10({n})"


def Sgn(n: Display | str) -> str:
    return f"Sgn({n})"


def Sin(n: Display | str) -> str:
    return f"Sin({n})"


def Sqrt(n: Display | str) -> str:
    return f"Sqrt({n})"


def Tan(n: Display | str) -> str:
    return f"Tan({n})"


# Reserved for Future Use
def Arccosh(n: Display | str) -> str:
    raise NotImplementedError("Arccosh is reserved for future use in Flowgorithm")


def Cosh(n: Display | str) -> str:
    raise NotImplementedError("Cosh is reserved for future use in Flowgorithm")


def Arcsinh(n: Display | str) -> str:
    raise NotImplementedError("Arcsinh is reserved for future use in Flowgorithm")


def Sinh(n: Display | str) -> str:
    raise NotImplementedError("Sinh is reserved for future use in Flowgorithm")


def Arctanh(n: Display | str) -> str:
    raise NotImplementedError("Arctanh is reserved for future use in Flowgorithm")


def Tanh(n: Display | str) -> str:
    raise NotImplementedError("Tanh is reserved for future use in Flowgorithm")


# Strings
def Len(s: Display | str) -> str:
    return f"Len({s})"


def Char(s: Display | str, i: Display | str) -> str:
    return f"Char({s}, {i})"


# Data Type Conversion
def ToChar(n: Display | str) -> str:
    return f"ToChar({n})"


def ToCode(c: Display | str) -> str:
    return f"ToCode({c})"


def ToFixed(r: Display | str, i: Display | str) -> str:
    return f"ToFixed({r}, {i})"


def ToInteger(n: Display | str) -> str:
    return f"ToInteger({n})"


def ToReal(n: Display | str) -> str:
    return f"ToReal({n})"


def ToString(n: Display | str) -> str:
    return f"ToString({n})"


# Other
def EOF() -> str:
    return "EOF()"


def Random(n: Display | str) -> str:
    return f"Random({n})"


def Size(a: Display | str) -> str:
    return f"Size({a})"
