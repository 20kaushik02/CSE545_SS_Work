import hashlib
import string
import itertools
import argparse
import time
import json
import re


def gen_perm_cipher(plain_text):
    cipher_text = hashlib.sha256(plain_text.encode("ascii")).hexdigest()
    return cipher_text


def gen_all_perms(
    perm_len=6,
    char_set=string.ascii_lowercase,
    prefix_len=0,
    resuming=False,
    resume_pos=0,
):
    """
    Permutation generator. Can specify length, character set and prefix length to rotate result files.

    Can resume from a specified position as well.

    If resuming, please ensure the other parameters are identical to the previous run. resume_pos is included
    """

    if prefix_len == 0:
        prefix_len = perm_len // 2
    split_len = len(char_set) ** (perm_len - prefix_len)

    print(
        f"Permuting {perm_len}-character strings from {char_set}. Splitting on a {prefix_len}-character prefix."
    )
    if resuming:
        print(f"Resuming from permutation {resume_pos}")

    perms = {}
    for i, item in enumerate(itertools.product(char_set, repeat=perm_len)):
        if resuming and i < resume_pos:
            pass
        perm_plain = "".join(item)
        perm_cipher = gen_perm_cipher(perm_plain)
        perms[perm_plain] = perm_cipher

        if (i + 1) % split_len == 0:
            perms_str = json.dumps(perms, indent=0)[2:-2]
            perms_str = re.sub(r'[":,]', "", perms_str)
            print(f"saving {split_len} permutations...")
            with open(
                f"result/{next(iter(perms.keys()))[:prefix_len]}.perms", "w"
            ) as out_f:
                print(perms_str, file=out_f)
            perms = {}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--perm_len", required=False, default=6, dest="p", type=int
    )
    parser.add_argument(
        "-f", "--prefix_len", required=False, default=0, dest="f", type=int
    )
    parser.add_argument(
        "-c",
        "--char_set",
        required=False,
        default=string.ascii_lowercase,
        dest="chars",
        type=str,
    )
    args = parser.parse_args()

    start_t = time.time()
    gen_all_perms(args.p, args.chars, args.f)
    end_t = time.time()
    print(f"generated all pairs in {end_t-start_t} seconds")
