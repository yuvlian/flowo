from __future__ import annotations
from .models import (
    Attribute,
    Declare,
    Assign,
    Input,
    Output,
    Comment,
    Breakpoint,
    Call,
    If,
    While,
    For,
    Do,
    Type,
    Direction,
    Function,
    Flowgorithm,
    Parameter,
    Statement,
    Display,
)
from .validation import validate_variable_name, validate_expression_target
from typing import List, Set
import base64
from datetime import datetime
import re


class Flow:
    def __init__(self, filename: str | None = None):
        self.model = Flowgorithm()
        self._scope_stack: List[List[Statement]] = []
        self._last_ifs = {}
        self._declared_vars: Set[str] = set()
        self.filename = filename

    @property
    def _current_scope(self) -> List[Statement]:
        if not self._scope_stack:
            raise RuntimeError("No active scope. Start a function first.")
        return self._scope_stack[-1]

    def _add_statement(self, stmt: Statement):
        self._current_scope.append(stmt)
        self._last_ifs[id(self._current_scope)] = stmt if isinstance(stmt, If) else None

    def attribute(self, name: str, value: str) -> Flow:
        self.model.attributes.append(Attribute(name, value))
        return self

    def name(self, value: str) -> Flow:
        return self.attribute("name", value)

    def authors(self, value: str) -> Flow:
        return self.attribute("authors", value)

    def about(self, value: str) -> Flow:
        return self.attribute("about", value)

    def function(
        self, name: str, return_type: Type = Type.NONE, return_variable: str = ""
    ) -> FunctionContext:
        self._declared_vars.clear()
        validate_variable_name(name)
        if return_variable:
            validate_variable_name(return_variable)

        func = Function(name, return_type, return_variable)
        self.model.functions.append(func)
        return FunctionContext(self, func)

    def declare(
        self, name: str, type: Type, array: bool = False, size: str = ""
    ) -> Flow:
        validate_variable_name(name)
        self._add_statement(Declare(name, type, array, size))

        for part in [p.strip() for p in name.split(",")]:
            self._declared_vars.add(part)

        return self

    def _check_var_exists(self, target: str) -> None:
        base_name = re.split(r"\[", target)[0].strip()
        if base_name not in self._declared_vars:
            raise RuntimeError(f"Variable '{base_name}' must be declared before use.")

    def assign(self, variable: str, expression: Display | str) -> Flow:
        validate_expression_target(variable)
        self._check_var_exists(variable)
        self._add_statement(Assign(variable, str(expression)))
        return self

    def input(self, variable: str) -> Flow:
        validate_expression_target(variable)
        self._check_var_exists(variable)
        self._add_statement(Input(variable))
        return self

    def output(self, expression: Display | str, newline: bool = True) -> Flow:
        self._add_statement(Output(str(expression), newline))
        return self

    def comment(self, text: str) -> Flow:
        self._add_statement(Comment(text))
        return self

    def breakpoint(self) -> Flow:
        self._add_statement(Breakpoint())
        return self

    def call(self, expression: Display | str) -> Flow:
        self._add_statement(Call(str(expression)))
        return self

    def if_(self, expression: Display | str) -> ScopeContext:
        stmt = If(str(expression))
        self._add_statement(stmt)
        return ScopeContext(self, stmt.then_statements)

    def else_(self) -> ScopeContext:
        last_if = self._last_ifs.get(id(self._current_scope))
        if not last_if or not isinstance(last_if, If):
            raise RuntimeError("else_() must follow an if_() block in the same scope")
        self._last_ifs[id(self._current_scope)] = None
        return ScopeContext(self, last_if.else_statements)

    def while_(self, expression: Display | str) -> ScopeContext:
        stmt = While(str(expression))
        self._add_statement(stmt)
        return ScopeContext(self, stmt.statements)

    def for_(
        self,
        variable: str,
        start: Display | str,
        end: Display | str,
        direction: Direction = Direction.INC,
        step: Display | str = "1",
    ) -> ScopeContext:
        stmt = For(variable, str(start), str(end), direction, str(step))
        self._add_statement(stmt)
        return ScopeContext(self, stmt.statements)

    def do_(self, expression: Display | str) -> ScopeContext:
        stmt = Do(str(expression))
        self._add_statement(stmt)
        return ScopeContext(self, stmt.statements)

    def build(self) -> str:
        has_saved = any(a.name == "saved" for a in self.model.attributes)
        if not has_saved:
            now = datetime.now()
            saved = now.strftime("%Y-%m-%d %I:%M:%S %p")

            author = "unknown"
            for a in self.model.attributes:
                if a.name == "authors":
                    author = a.value
                    break

            time_part = now.strftime("%Y-%m-%d;%I:%M:%S %p")
            created_str = f"{author};YUVLIAN_WAS_HERE;{time_part};1111"
            edited_str = f"{author};YUVLIAN_WAS_HERE;{time_part};1;1111"

            self.attribute("saved", saved)
            self.attribute("created", base64.b64encode(created_str.encode()).decode())
            self.attribute("edited", base64.b64encode(edited_str.encode()).decode())

        for func in self.model.functions:
            if func.variable and func.type != Type.NONE:
                already_declared = False
                for stmt in func.statements:
                    if isinstance(stmt, Declare):
                        names = [n.strip() for n in stmt.name.split(",")]
                        if func.variable in names:
                            already_declared = True
                            break
                if not already_declared:
                    func.statements.insert(0, Declare(func.variable, func.type))

        return self.model.to_xml()

    def to_fprg(self, filename: str | None = None) -> None:
        target = filename or self.filename
        if not target:
            raise ValueError("No filename provided to to_fprg and none set in Flow")

        xml_string = self.build()
        with open(target, "w", encoding="utf-8") as f:
            f.write(xml_string)
        print(f"Successfully generated {target}")


class FunctionContext:
    def __init__(self, flow: Flow, func: Function):
        self.flow = flow
        self.func = func

    def parameter(self, name: str, type: Type, array: bool = False) -> FunctionContext:
        validate_variable_name(name)
        self.func.parameters.append(Parameter(name, type, array))
        self.flow._declared_vars.add(name)
        return self

    def __enter__(self) -> Flow:
        self.flow._scope_stack.append(self.func.statements)

        if self.func.variable:
            self.flow._declared_vars.add(self.func.variable)

        return self.flow

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flow._scope_stack.pop()
        self.flow._declared_vars.clear()


class ScopeContext:
    def __init__(self, flow: Flow, statements: List[Statement]):
        self.flow = flow
        self.statements = statements

    def __enter__(self) -> Flow:
        self.flow._scope_stack.append(self.statements)
        return self.flow

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        self.flow._scope_stack.pop()
