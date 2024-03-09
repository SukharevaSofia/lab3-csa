#!/usr/bin/env python3

import array
import json
import logging
import sys

from errors import ParsingError


def read_code(file_name):
    with open(file_name, encoding="utf-8") as file:
        return json.loads(file.read())


class Alu:
    def __init__(self):
        self.left = 0
        self.right = 0
        self.out = 0

    def inc(self):
        self.out = self.left + 1

    def dec(self):
        self.out = self.left - 1

    def add(self):
        self.out = self.left + self.right

    def sub(self):
        self.out = self.left - self.right

    def mul(self):
        self.out = self.left * self.right

    def div(self):
        self.out = int(self.left / self.right)

    def mod(self):
        self.out = self.left % self.right

    def bit_or(self):
        self.out = self.left | self.right

    def bit_and(self):
        self.out = self.left & self.right

    def out(self):
        return self.out


class DataPath:
    def __init__(self, buffer_in, init_data):
        self.memory = array.array("q", (0 for x in range(2**20)))
        self.addr = 0

        self.regfile = array.array("q", (0 for x in range(16)))

        self.alu = Alu()

        self.input = buffer_in
        self.output = []
        for x in init_data:
            s = x["variable_data"]
            self.memory[self.addr] = len(s)
            self.addr += 1
            for i in range(len(s)):
                self.memory[self.addr] = ord(s[i])
                self.addr += 1

    def route_toreg(self, reg):
        self.regfile[reg] = self.alu.out

    def next_in(self):
        return next(self.input)

    def latch_addr(self):
        self.addr = self.alu.out

    def load_from_addr(self):
        self.alu.out = self.memory[self.addr]

    def write_to_addr(self):
        self.memory[self.addr] = self.alu.out

    def mux_left(self, signal):
        self.alu.left = self.regfile[signal]
        self.alu.out = self.alu.left

    def mux_right(self, signal):
        self.alu.right = self.regfile[signal]

    def __repr__(self):
        return "DataPath: regs = {}".format(self.regfile.tolist())


class ControlUnit:
    def __init__(self, program, data_path):
        self.program = program
        self.pc = 0
        self.dp = data_path

    def write_pc(self, val):
        self.pc = val

    def inc_pc(self):
        self.pc += 1

    def decoder(self, instr):
        opcode = instr["instr"]
        args = instr["args"]

        match opcode:
            case "jump":
                self.write_pc(args[0])

            case "jge":
                if self.dp.regfile[args[0]] >= 0:
                    self.write_pc(args[1])

            case "jne":
                if self.dp.regfile[args[0]] != 0:
                    self.write_pc(args[1])

            case "jeq":
                if self.dp.regfile[args[0]] == 0:
                    self.write_pc(args[1])

            case "in":
                self.dp.regfile[args[0]] = ord(self.dp.next_in())

            case "out":
                self.dp.output.append(chr(self.dp.regfile[args[0]]))

            case "outn":
                self.dp.output.append(str(self.dp.regfile[args[0]]))

            case "mov":
                self.dp.mux_left(args[1])
                self.dp.regfile[args[0]] = self.dp.alu.out

            case "ldc":
                self.dp.regfile[args[0]] = args[1]

            case "ld":
                self.dp.mux_left(args[1])
                self.dp.latch_addr()
                self.dp.load_from_addr()
                self.dp.route_toreg(args[0])

            case "sv":
                self.dp.mux_left(args[1])
                self.dp.latch_addr()
                self.dp.mux_left(args[0])
                self.dp.write_to_addr()

            case "inc":
                self.dp.mux_left(args[0])
                self.dp.alu.inc()
                self.dp.route_toreg(args[0])

            case "dec":
                self.dp.mux_left(args[0])
                self.dp.alu.dec()
                self.dp.route_toreg(args[0])

            case "add":
                self.dp.mux_left(args[0])
                self.dp.mux_right(args[1])
                self.dp.alu.add()
                self.dp.route_toreg(args[0])

            case "sub":
                self.dp.mux_left(args[0])
                self.dp.mux_right(args[1])
                self.dp.alu.sub()
                self.dp.route_toreg(args[0])

            case "mul":
                self.dp.mux_left(args[0])
                self.dp.mux_right(args[1])
                self.dp.alu.mul()
                self.dp.route_toreg(args[0])

            case "div":
                self.dp.mux_left(args[0])
                self.dp.mux_right(args[1])
                self.dp.alu.div()
                self.dp.route_toreg(args[0])

            case "mod":
                self.dp.mux_left(args[0])
                self.dp.mux_right(args[1])
                self.dp.alu.mod()
                self.dp.route_toreg(args[0])

            case "hlt":
                raise StopIteration

            case _:
                raise ParsingError(instr)

    def primary_loop(self):
        while True:
            logging.debug(repr(self))
            instr = self.program[self.pc]
            self.inc_pc()
            self.decoder(instr)

    def __repr__(self):
        own = "ControlUnit: IP={}".format(self.pc)
        dp = repr(self.dp)
        instr = self.program[self.pc]
        instr = "address: {}, instr: {}, args: {}".format(
            self.pc, instr["instr"], instr["args"])
        return "\n{} {}\n{}\n".format(own, dp, instr)


def simulation(code, input_tokens, init_data):
    data_path = DataPath(input_tokens, init_data)
    control_unit = ControlUnit(code, data_path)

    try:
        control_unit.primary_loop()
    except StopIteration:
        pass

    out = data_path.output

    logging.info("output_buffer: %s", out)
    return "".join(out)


def run_vm(code_file_path, input_file_path):
    in_bin = read_code(code_file_path)
    code = in_bin["program"]
    data = in_bin["data"]
    with open(input_file_path, encoding="utf-8") as file:
        input_text = file.read()
        token = []
        for char in input_text:
            token.append(char)

    print(simulation(code, iter(token), data), end="")


if __name__ == "__main__":
    assert len(sys.argv) == 3
    _, target_file_name, input_file_name = sys.argv
    logging.getLogger().setLevel(logging.DEBUG)
    logging.basicConfig(
        filename="./golden/logs/example.log",
        filemode="w",
        format="%(levelname)-7s %(module)s:%(funcName)-13s %(message)s",
    )
    run_vm(target_file_name, input_file_name)
