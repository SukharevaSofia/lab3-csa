from __future__ import annotations

import json
import re
import sys

from exceptions import CompileError, ParsingError
from isa import (
    get_isa_by_instruction,
    get_variable_data,
    is_label,
    is_number,
    is_register,
    is_variable_declaration,
    register_to_index,
    remove_comments,
    to_number,
)
from typeguard import typechecked


@typechecked
def run_translator(source: str, target: str):
    try:
        code: list[str] = read_file(source)
        struct = parse(code)
        write_file(target, struct)

    except ParsingError as error:
        print(error.msg, file=sys.stderr)
    except CompileError as error:
        print(error.msg, file=sys.stderr)


@typechecked
def parse(code: list[str]) -> str:
    program_struct: list[dict] = []
    data_struct: list[dict] = []
    addresses: dict[str, int] = {}
    data_size = 0

    code_gen(code, program_struct, addresses, data_struct, data_size)
    replace_to_address(program_struct, addresses)

    return json.dumps({"program": program_struct, "data": data_struct})


@typechecked
def code_gen(
    code: list[str], program_struct: list[dict], addresses: dict[str, int], data_struct: list[dict], data_size: int
):
    for line in code:
        line = line.strip()
        line = remove_comments(line)

        if len(line) == 0:
            continue

        if is_variable_declaration(line):
            variable_name, variable_value = get_variable_data(line)
            addresses[variable_name] = data_size
            data_size += len(variable_value) + 1

            data_struct.append({"variable_data": variable_value})
            continue

        if is_label(line):
            index = line.index(":")
            label_name = line[0:index]
            addresses[label_name] = len(program_struct)
            continue

        line = re.split("[\n ]", line)
        data = list(filter(lambda x: x != "", line))

        instr = data[0]
        args = data[1:]

        isa = get_isa_by_instruction(instr)

        if not isa.validate(args):
            raise ParsingError(f"CouldNotInterpretCommand:{line}")

        replace_numbers(args)

        program_struct.append({"instr": isa.identity, "args": args})


@typechecked
def replace_to_address(
    struct: list[dict],
    addresses: dict[str, int],
):
    for instruction in struct:
        args = instruction["args"]
        instruction_name = instruction["instr"]

        if instruction_name == "ldc" and not isinstance(args[1], int):
            if args[1] not in addresses.keys():
                raise ParsingError("VariableNameNotFound")

            args[1] = addresses[args[1]]
            continue

        for i in range(0, len(args)):
            if not isinstance(args[i], int) and is_label(args[i]):
                if args[i] not in addresses.keys():
                    raise ParsingError(f"NoLabelNamed:{args[i]}")

                args[i] = addresses[args[i]]


@typechecked
def replace_numbers(args: list):
    for i in range(0, len(args)):
        if is_register(args[i]):
            args[i] = register_to_index(args[i])

        elif is_number(args[i]):
            args[i] = to_number(args[i])


@typechecked
def validate_args_length(args: list[str]):
    assert len(args) == 2


@typechecked
def read_file(file_name: str) -> list[str]:
    with open(file_name) as file:
        return file.readlines()


@typechecked
def write_file(file_name: str, data: str):
    with open(file_name, "w") as file:
        file.write(data)


if __name__ == "__main__":
    assert len(sys.argv) == 3
    _, source_file_name, target_file_name = sys.argv
    run_translator(source_file_name, target_file_name)
