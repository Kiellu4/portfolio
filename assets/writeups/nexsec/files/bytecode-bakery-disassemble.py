#!/usr/bin/env python3
import struct

blob = open("recipe.bin", "rb").read()
assert blob[:4] == b"BAKE"
version, input_len, code_len = struct.unpack("<BBH", blob[4:8])
code = blob[8:8 + code_len]
print("version", version, "input_len", input_len, "code_len", code_len)

names = {0x01:"PUSH",0x02:"LOAD",0x03:"ADD",0x04:"SUB",0x05:"XOR",0x06:"ROL",0x07:"EQ",0x08:"JNZ",0x09:"JMP",0x0A:"FAIL",0x0B:"OK",0x0C:"DUP",0x0D:"AND"}
pc = 0
while pc < len(code):
    start = pc; op = code[pc]; pc += 1; arg = ""
    if op == 0x01: arg = f"{code[pc]:#04x}"; pc += 1
    elif op == 0x02: arg = f"ing[{code[pc]}]"; pc += 1
    elif op in (0x08, 0x09): arg = f"{code[pc] | (code[pc+1] << 8):#06x}"; pc += 2
    print(f"{start:04x}: {names.get(op, f'?{op:#x}'):5} {arg}")
