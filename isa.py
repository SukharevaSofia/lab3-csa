from __future__ import annotations

import enum
import string
import typing

from exceptions import CompileError, ParsingError
from typeguard import typechecked

registers: list[str] = [f"r{i}" for i in range(16)]


class Isa(enum.Enum):
    ADD: typing.ClassVar = (
        {
            "identity": "add",
            "number_of_arguments": 2,
            "validate": lambda args: len(args) == 2 and is_register(args[0]) and is_register(args[1]),
        },
    )

    SUB: typing.ClassVar = {
        "identity": "sub",
        "number_of_arguments": 2,
        "validate": lambda args: len(args) == 2 and is_register(args[0]) and is_register(args[1]),
    }

    MUL: typing.ClassVar = {
        "identity": "mul",
        "number_of_arguments": 2,
        "validate": lambda args: len(args) == 2 and is_register(args[0]) and is_register(args[1]),
    }

    INC: typing.ClassVar = {
        "identity": "inc",
        "number_of_arguments": 1,
        "validate": lambda args: len(args) == 1 and is_register(args[0]),
    }

    DEC: typing.ClassVar = {
        "identity": "dec",
        "number_of_arguments": 1,
        "validate": lambda args: len(args) == 1 and is_register(args[0]),
    }

    DIV: typing.ClassVar = {
        "identity": "div",
        "number_of_arguments": 2,
        "validate": lambda args: len(args) == 2 and is_register(args[0]) and is_register(args[1]),
    }

    MOD: typing.ClassVar = {
        "identity": "mod",
        "number_of_arguments": 2,
        "validate": lambda args: len(args) == 2 and is_register(args[0]) and is_register(args[1]),
    }

    AND: typing.ClassVar = {
        "identity": "and",
        "number_of_arguments": 2,
        "validate": lambda args: len(args) == 2 and is_register(args[0]) and is_register(args[1]),
    }

    OR: typing.ClassVar = {
        "identity": "or",
        "number_of_arguments": 2,
        "validate": lambda args: len(args) == 2 and is_register(args[0]) and is_register(args[1]),
    }

    MOV: typing.ClassVar = {
        "identity": "mov",
        "number_of_arguments": 2,
        "validate": lambda args: len(args) == 2 and is_register(args[0]) and is_register(args[1]),
    }

    LD: typing.ClassVar = {
        "identity": "ld",
        "number_of_arguments": 2,
        "validate": lambda args: len(args) == 2 and is_register(args[0]) and is_register(args[1]),
    }

    LDC: typing.ClassVar = {
        "identity": "ldc",
        "number_of_arguments": 2,
        "validate": lambda args: len(args) == 2 and is_register(args[0]) and (is_number(args[1]) or is_string(args[1])),
    }

    IN: typing.ClassVar = {
        "identity": "in",
        "number_of_arguments": 1,
        "validate": lambda args: len(args) == 1 and is_register(args[0]),
    }

    OUT: typing.ClassVar = {
        "identity": "out",
        "number_of_arguments": 1,
        "validate": lambda args: len(args) == 1 and is_register(args[0]),
    }

    OUTN: typing.ClassVar = {
        "identity": "outn",
        "number_of_arguments": 1,
        "validate": lambda args: len(args) == 1 and is_register(args[0]),
    }

    SV: typing.ClassVar = {
        "identity": "sv",
        "number_of_arguments": 2,
        "validate": lambda args: len(args) == 2 and is_register(args[0]) and is_register(args[1]),
    }

    JUMP: typing.ClassVar = {
        "identity": "jump",
        "number_of_arguments": 1,
        "validate": lambda args: len(args) == 1 and (not is_register(args[0])),
    }

    JGE: typing.ClassVar = {
        "identity": "jge",
        "number_of_arguments": 2,
        "validate": lambda args: len(args) == 2 and is_register(args[0]) and is_label(args[1]),
    }

    JNE: typing.ClassVar = {
        "identity": "jne",
        "number_of_arguments": 2,
        "validate": lambda args: len(args) == 2 and is_register(args[0]) and is_label(args[1]),
    }

    JEQ: typing.ClassVar = {
        "identity": "jeq",
        "number_of_arguments": 2,
        "validate": lambda args: len(args) == 2 and is_register(args[0]) and is_label(args[1]),
    }

    HLT: typing.ClassVar = {"identity": "hlt", "number_of_arguments": 0, "validate": lambda args: len(args) == 0}

    @typechecked
    def __init__(self, vals: dict):
        self.identity = vals["identity"]
        self.number_of_arguments = vals["number_of_arguments"]
        self.validate = vals["validate"]

    def get_validate(self):
        return self.validate


@typechecked
def get_isa_by_instruction(instr: str) -> Isa:
    for isa in list(Isa):
        if isa.identity == instr:
            return isa

    raise ParsingError(f"InstructionNotFound:{instr}")


@typechecked
def is_register(arg: str) -> bool:
    for reg in registers:
        if reg == arg:
            return True

    return False


@typechecked
def is_label(arg: str) -> bool:
    return len(arg) > 1 and arg[0] == "_" and is_string(arg[1:-1])


@typechecked
def is_number(arg: str) -> bool:
    if is_hex(arg):
        return True

    return str.isnumeric(arg) if arg[0] != "-" else str.isnumeric(arg[1:])


def is_hex(arg: str) -> bool:
    if len(arg) <= 2 or (arg[0] != "-" and arg[1] != "x") or (arg[0] == "-" and arg[2] != "x"):
        return False

    start_index = 2 if arg[0] != "-" else 3
    hex_digits = set(string.hexdigits)
    return all(arg[i] in hex_digits for i in range(start_index, len(arg)))


@typechecked
def is_string(arg: str) -> bool:
    for char in arg:
        if not char.isupper() and not char == "_" and not char.isdigit():
            return False

    return True


@typechecked
def is_variable_declaration(arg: str) -> bool:
    if arg.count(":") == 0 or arg.count('"') != 2:
        return False

    index = arg.index(":")

    if not is_string(arg[0:index]):
        return False

    if arg[index + 1] != '"' and arg[-1] != '"':
        return False

    return True


@typechecked
def register_to_index(reg: str) -> int:
    for i in range(0, len(registers)):
        if registers[i] == reg:
            return i

    raise CompileError("nar")


@typechecked
def to_number(arg: str) -> int:
    if is_hex(arg):
        if arg[0] == "-":
            return -int(arg[3:], 16)

        return int(arg[2:], 16)

    if is_number(arg):
        if arg[0] == "-":
            return -int(arg[1:])

        return int(arg)

    raise CompileError("nan")


@typechecked
def remove_comments(arg: str) -> str:
    return arg if arg.count(";") == 0 else arg[: arg.index(";")].strip()


@typechecked
def get_variable_data(arg: str) -> tuple[str, str]:
    if not is_variable_declaration:
        ParsingError("navd")

    index = arg.index(":")
    variable_name = arg[:index]

    index = arg.index('"')
    variable_value = arg[index + 1 : -1]

    return variable_name, variable_value
