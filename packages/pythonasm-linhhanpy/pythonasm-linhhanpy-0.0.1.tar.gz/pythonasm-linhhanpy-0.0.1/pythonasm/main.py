#pythonasm

"""
This is a module for ASM...
"""

import re
import os

variables = {'ax': 0, 'bx': 0, 'cx': 0, 'dx': 0}


def add(a, b): return a + b


def subtract(a, b): return a - b


def multiply(a, b): return a * b


def divide(a, b): return a / b if b != 0 else (print("Error:Divisor cannot be 0."), a)[1]


def operation(line):
    add_pattern = re.compile(r'add\s+(\w+),\s*(\w+)')
    sub_pattern = re.compile(r'sub\s+(\w+),\s*(\w+)')
    mul_pattern = re.compile(r'mul\s+(\w+),\s*(\w+)')
    div_pattern = re.compile(r'div\s+(\w+),\s*(\w+)')

    for pattern, operation in [(add_pattern, add), (sub_pattern, subtract), (mul_pattern, multiply), (div_pattern, divide)]:
        match = pattern.match(line)
        if match:
            operand1, operand2 = match.groups()
            if operand1 in variables:
                operand2_value = variables.get(operand2, None)
                if operand2_value is not None:
                    variables[operand1] = operation(variables[operand1], operand2_value)
                else:
                    try:
                        operand2_value = int(operand2)
                        variables[operand1] = operation(variables[operand1], operand2_value)
                    except ValueError:
                        print(f"Error:Operand {operand2} is not defined.")
            else:
                print(f"Error:Operand {operand1} is not defined.")
            return


def check():
    if (variables['ax'] == 4 and isinstance(variables['bx'], int) and variables['bx'] == 1
            and isinstance(variables['cx'], str) and variables['dx'] == len(variables['cx'])):
        print(variables['cx'])
    elif (variables['ax'] == 4 and isinstance(variables['bx'], int) and variables['bx'] == 1
          and isinstance(variables['cx'], str) and variables['dx'] != len(variables['cx'])):
        print("Error:Length does not match.")
    elif variables['ax'] == 3 and variables['bx'] == 0 and isinstance(variables['dx'], int):
        input_str = input()
        if len(input_str) <= variables['dx']:
            variables['cx'] = input_str
        else:
            print("Error:The input string length exceeds the reserved length.")


def asm(filename):
    if not os.path.exists(filename):
        print(f"Error:File {filename} does not exist.")
        return

    with open(filename, 'r') as file:
        lines = file.readlines()

    mov_reg_to_const_pattern = re.compile(r'mov\s+(\w+),\s*(\d+)')
    mov_reg_to_reg_pattern = re.compile(r'mov\s+(\w+),\s*\[?(\w+)\]?\s*')
    db_pattern = re.compile(r'(\w+)\s+db\s+"([^"]*)"')

    for line in lines:
        line = line.strip()

        match = mov_reg_to_const_pattern.match(line)
        if match:
            reg, value = match.groups()
            try:
                variables[reg] = int(value)
            except ValueError:
                print(f"Error:Cannot convert {value} to an integer.")
            continue

        match = mov_reg_to_reg_pattern.match(line)
        if match:
            dest, src = match.groups()
            if src in variables:
                variables[dest] = variables[src]
            else:
                print(f"Warning: Source register {src} is not defined.")
            continue

        match = db_pattern.match(line)
        if match:
            label, value = match.groups()
            variables[label] = value.strip('"')
            continue

        operation(line)
        if re.search(r"nt .*(?:80h|0x80)", line):
            check()




