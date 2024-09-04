from typing import Tuple
import hashlib
import random
import string


def gen_plain_cipher() -> Tuple[str, str]:
    plain_text = "".join([random.choice(string.ascii_lowercase) for _ in range(6)])
    cipher_text = hashlib.sha256(plain_text.encode("ascii")).hexdigest()
    return plain_text, cipher_text


def main():
    plain_text, cipher_text = gen_plain_cipher()
    print(f"Please submit the *plain-text string* for the SHA256 hash of \"{cipher_text}\".")
    print("")

    input_str = input("Your answer: ")
    if input_str.strip(" \n\r") == plain_text:
        with open("/flag", "r") as f:
            print("Congrats! Your flag:", f.read())
    else:
        print("Incorrect input. Try again!")


if __name__ == "__main__":
    main()

