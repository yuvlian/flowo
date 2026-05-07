from __future__ import annotations
import xml.etree.ElementTree as ET
from enum import StrEnum
from dataclasses import dataclass, field
from typing import List, Protocol


class Display(Protocol):
    def __str__(self) -> str: ...


class Type(StrEnum):
    INTEGER = "Integer"
    REAL = "Real"
    STRING = "String"
    BOOLEAN = "Boolean"
    NONE = "None"


class Direction(StrEnum):
    INC = "inc"
    DEC = "dec"


@dataclass
class Attribute:
    name: str
    value: str


@dataclass
class Parameter:
    name: str
    type: Type
    array: bool = False


@dataclass
class Statement:
    pass


@dataclass
class Declare(Statement):
    name: str
    type: Type
    array: bool = False
    size: str = ""


@dataclass
class Assign(Statement):
    variable: str
    expression: str


@dataclass
class Input(Statement):
    variable: str


@dataclass
class Output(Statement):
    expression: str
    newline: bool = True


@dataclass
class Comment(Statement):
    text: str


@dataclass
class Breakpoint(Statement):
    pass


@dataclass
class Call(Statement):
    expression: str


@dataclass
class If(Statement):
    expression: str
    then_statements: List[Statement] = field(default_factory=list)
    else_statements: List[Statement] = field(default_factory=list)


@dataclass
class While(Statement):
    expression: str
    statements: List[Statement] = field(default_factory=list)


@dataclass
class For(Statement):
    variable: str
    start: str
    end: str
    direction: Direction = Direction.INC
    step: str = "1"
    statements: List[Statement] = field(default_factory=list)


@dataclass
class Do(Statement):
    expression: str
    statements: List[Statement] = field(default_factory=list)


@dataclass
class Function:
    name: str
    type: Type = Type.NONE
    variable: str = ""
    parameters: List[Parameter] = field(default_factory=list)
    statements: List[Statement] = field(default_factory=list)


@dataclass
class Flowgorithm:
    fileversion: str = "4.2"
    attributes: List[Attribute] = field(default_factory=list)
    functions: List[Function] = field(default_factory=list)

    def to_xml(self) -> str:
        root = ET.Element("flowgorithm", {"fileversion": self.fileversion})

        attrs_el = ET.SubElement(root, "attributes")
        for attr in self.attributes:
            ET.SubElement(
                attrs_el, "attribute", {"name": attr.name, "value": attr.value}
            )

        for func in self.functions:
            func_el = ET.SubElement(
                root,
                "function",
                {"name": func.name, "type": func.type.value, "variable": func.variable},
            )

            params_el = ET.SubElement(func_el, "parameters")
            for param in func.parameters:
                ET.SubElement(
                    params_el,
                    "parameter",
                    {
                        "name": param.name,
                        "type": param.type.value,
                        "array": str(param.array),
                    },
                )

            body_el = ET.SubElement(func_el, "body")
            self._render_statements(body_el, func.statements)

        return self._prettify(root)

    def _render_statements(
        self, parent: ET.Element, statements: List[Statement]
    ) -> None:
        for stmt in statements:
            if isinstance(stmt, Declare):
                ET.SubElement(
                    parent,
                    "declare",
                    {
                        "name": stmt.name,
                        "type": stmt.type.value,
                        "array": str(stmt.array),
                        "size": stmt.size,
                    },
                )
            elif isinstance(stmt, Assign):
                ET.SubElement(
                    parent,
                    "assign",
                    {"variable": stmt.variable, "expression": stmt.expression},
                )
            elif isinstance(stmt, Input):
                ET.SubElement(parent, "input", {"variable": stmt.variable})
            elif isinstance(stmt, Output):
                ET.SubElement(
                    parent,
                    "output",
                    {"expression": stmt.expression, "newline": str(stmt.newline)},
                )
            elif isinstance(stmt, Comment):
                ET.SubElement(parent, "comment", {"text": stmt.text})
            elif isinstance(stmt, Breakpoint):
                ET.SubElement(parent, "breakpoint")
            elif isinstance(stmt, Call):
                ET.SubElement(parent, "call", {"expression": stmt.expression})
            elif isinstance(stmt, If):
                if_el = ET.SubElement(parent, "if", {"expression": stmt.expression})
                then_el = ET.SubElement(if_el, "then")
                self._render_statements(then_el, stmt.then_statements)
                else_el = ET.SubElement(if_el, "else")
                self._render_statements(else_el, stmt.else_statements)
            elif isinstance(stmt, While):
                while_el = ET.SubElement(
                    parent, "while", {"expression": stmt.expression}
                )
                self._render_statements(while_el, stmt.statements)
            elif isinstance(stmt, For):
                for_el = ET.SubElement(
                    parent,
                    "for",
                    {
                        "variable": stmt.variable,
                        "start": stmt.start,
                        "end": stmt.end,
                        "direction": stmt.direction.value,
                        "step": stmt.step,
                    },
                )
                self._render_statements(for_el, stmt.statements)
            elif isinstance(stmt, Do):
                do_el = ET.SubElement(parent, "do", {"expression": stmt.expression})
                self._render_statements(do_el, stmt.statements)

    def _prettify(self, elem: ET.Element) -> str:
        from xml.dom import minidom

        rough_string = ET.tostring(elem, "utf-8")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="    ")
