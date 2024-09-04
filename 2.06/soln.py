import argparse
import time


def verify(ctx: str) -> bool:
    result = 0

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    if ord(ctx[0]) > 127:  # 0
        result = result | 0x26

    if ord(ctx[0]) & 0x40 != 0:  # 0
        result = result | 0x26

    if ord(ctx[0]) & 0x20 == 0:  # 1
        result = result | 0x27

    if ord(ctx[0]) & 0x10 == 0:  # 1
        result = result | 0x26

    if ord(ctx[0]) & 8 != 0:  # 0
        result = result | 4

    if ord(ctx[0]) & 4 == 0:  # 1
        result = result | 0x11

    if ord(ctx[0]) & 2 == 0:  # 1
        result = result | 5

    if ord(ctx[0]) & 1 != 0:  # 0
        result = result | 0x22

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    if ord(ctx[1]) > 127:  # 0
        result = result | 2

    if ord(ctx[1]) & 0x40 != 0:  # 0
        result = result | 2

    if ord(ctx[1]) & 0x20 == 0:  # 1
        result = result | 0x25

    if ord(ctx[1]) & 0x10 == 0:  # 1
        result = result | 0x12

    if ord(ctx[1]) & 8 != 0:  # 0
        result = result | 0x27

    if ord(ctx[1]) & 4 == 0:  # 1
        result = result | 0x1C

    if ord(ctx[1]) & 2 == 0:  # 1
        result = result | 9

    if ord(ctx[1]) & 1 == 0:  # 1
        result = result | 0x11

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    if ord(ctx[2]) > 127:  # 0
        result = result | 0x11

    if ord(ctx[2]) & 0x40 == 0:  # 1
        result = result | 0x15

    if ord(ctx[2]) & 0x20 == 0:  # 1
        result = result | 0x11

    if ord(ctx[2]) & 0x10 != 0:  # 0
        result = result | 0xD

    if ord(ctx[2]) & 8 == 0:  # 1
        result = result | 0x29

    if ord(ctx[2]) & 4 != 0:  # 0
        result = result | 0x23

    if ord(ctx[2]) & 2 == 0:  # 1
        result = result | 0xD

    if ord(ctx[2]) & 1 == 0:  # 1
        result = result | 0x1C

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    if ord(ctx[3]) > 127:  # 0
        result = result | 0x1E

    if ord(ctx[3]) & 0x40 == 0:  # 1
        result = result | 0x28

    if ord(ctx[3]) & 0x20 != 0:  # 0
        result = result | 0x28

    if ord(ctx[3]) & 0x10 == 0:  # 1
        result = result | 0x14

    if ord(ctx[3]) & 8 != 0:  # 0
        result = result | 0x1F

    if ord(ctx[3]) & 4 == 0:  # 1
        result = result | 0x28

    if ord(ctx[3]) & 2 == 0:  # 1
        result = result | 0x13

    if ord(ctx[3]) & 1 == 0:  # 1
        result = result | 0x2C

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    if ord(ctx[4]) > 127:  # 0
        result = result | 0x19

    if ord(ctx[4]) & 0x40 != 0:  # 0
        result = result | 0x11

    if ord(ctx[4]) & 0x20 == 0:  # 1
        result = result | 0x1F

    if ord(ctx[4]) & 0x10 == 0:  # 1
        result = result | 8

    if ord(ctx[4]) & 8 != 0:  # 0
        result = result | 0x2D

    if ord(ctx[4]) & 4 == 0:  # 1
        result = result | 0x1C

    if ord(ctx[4]) & 2 == 0:  # 1
        result = result | 8

    if ord(ctx[4]) & 1 != 0:  # 0
        result = result | 0x10

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    if ord(ctx[5]) > 127:  # 0
        result = result | 9

    if ord(ctx[5]) & 0x40 == 0:  # 1
        result = result | 0x19

    if ord(ctx[5]) & 0x20 != 0:  # 0
        result = result | 0x1C

    if ord(ctx[5]) & 0x10 == 0:  # 1
        result = result | 0x17

    if ord(ctx[5]) & 8 == 0:  # 1
        result = result | 0x27

    if ord(ctx[5]) & 4 != 0:  # 0
        result = result | 0x18

    if ord(ctx[5]) & 2 != 0:  # 0
        result = result | 0x2D

    if ord(ctx[5]) & 1 == 0:  # 1
        result = result | 0x1A

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    if ord(ctx[6]) > 127:  # 0
        result = result | 0x10

    if ord(ctx[6]) & 0x40 == 0:  # 1
        result = result | 7

    if ord(ctx[6]) & 0x20 == 0:  # 1
        result = result | 0x2B

    if ord(ctx[6]) & 0x10 != 0:  # 0
        result = result | 0x24

    if ord(ctx[6]) & 8 == 0:  # 1
        result = result | 0x15

    if ord(ctx[6]) & 4 == 0:  # 1
        result = result | 0xF

    if ord(ctx[6]) & 2 == 0:  # 1
        result = result | 9

    if ord(ctx[6]) & 1 != 0:  # 0
        result = result | 1

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    if ord(ctx[7]) > 127:  # 0
        result = result | 0x27

    if ord(ctx[7]) & 0x40 == 0:  # 1
        result = result | 0xC

    if ord(ctx[7]) & 0x20 != 0:  # 0
        result = result | 4

    if ord(ctx[7]) & 0x10 != 0:  # 0
        result = result | 0x1A

    if ord(ctx[7]) & 8 == 0:  # 1
        result = result | 0x14

    if ord(ctx[7]) & 4 != 0:  # 0
        result = result | 0x1A

    if ord(ctx[7]) & 2 == 0:  # 1
        result = result | 8

    if ord(ctx[7]) & 1 == 0:  # 1
        result = result | 9

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    if ord(ctx[8]) > 127:  # 0
        result = result | 0x2C

    if ord(ctx[8]) & 0x40 == 0:  # 1
        result = result | 0x16

    if ord(ctx[8]) & 0x20 == 0:  # 1
        result = result | 0x22

    if ord(ctx[8]) & 0x10 == 0:  # 1
        result = result | 0x28

    if ord(ctx[8]) & 8 != 0:  # 0
        result = result | 0x22

    if ord(ctx[8]) & 4 == 0:  # 1
        result = result | 9

    if ord(ctx[8]) & 2 == 0:  # 1
        result = result | 0x17

    if ord(ctx[8]) & 1 != 0:  # 0
        result = result | 0x22

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    if ord(ctx[9]) > 127:  # 0
        result = result | 0x19

    if ord(ctx[9]) & 0x40 == 0:  # 1
        result = result | 0x29

    if ord(ctx[9]) & 0x20 != 0:  # 0
        result = result | 0x2D

    if ord(ctx[9]) & 0x10 == 0:  # 1
        result = result | 0x23

    if ord(ctx[9]) & 8 != 0:  # 0
        result = result | 0x12

    if ord(ctx[9]) & 4 == 0:  # 1
        result = result | 2

    if ord(ctx[9]) & 2 != 0:  # 0
        result = result | 0x11

    if ord(ctx[9]) & 1 != 0:  # 0
        result = result | 4

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    if ord(ctx[10]) > 127:  # 0
        result = result | 0x26

    if ord(ctx[10]) & 0x40 == 0:  # 1
        result = result | 0x15

    if ord(ctx[10]) & 0x20 == 0:  # 1
        result = result | 0xC

    if ord(ctx[10]) & 0x10 == 0:  # 1
        result = 0x1B

    if ord(ctx[10]) & 8 != 0:  # 0
        result = result | 0xD

    if ord(ctx[10]) & 4 != 0:  # 0
        result = result | 0x24

    if ord(ctx[10]) & 2 != 0:  # 0
        result = result | 0x21

    if ord(ctx[10]) & 1 != 0:  # 0
        result = result | 0x23

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    if ord(ctx[0xB]) > 127:  # 0
        result = result | 0x16

    if ord(ctx[0xB]) & 0x40 == 0:  # 1
        result = result | 0x11

    if ord(ctx[0xB]) & 0x20 == 0:  # 1
        result = result | 7

    if ord(ctx[0xB]) & 0x10 != 0:  # 0
        result = result | 0x19

    if ord(ctx[0xB]) & 8 != 0:  # 0
        result = result | 0x1A

    if ord(ctx[0xB]) & 4 != 0:  # 0
        result = result | 0x29

    if ord(ctx[0xB]) & 2 != 0:  # 0
        result = result | 0x23

    if ord(ctx[0xB]) & 1 == 0:  # 1
        result = result | 0x2A

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    if ord(ctx[0xC]) > 127:  # 0
        result = result | 0x2B

    if ord(ctx[0xC]) & 0x40 == 0:  # 1
        result = result | 0x10

    if ord(ctx[0xC]) & 0x20 == 0:  # 1
        result = result | 0x12

    if ord(ctx[0xC]) & 0x10 == 0:  # 1
        result = result | 0x29

    if ord(ctx[0xC]) & 8 != 0:  # 0
        result = result | 3

    if ord(ctx[0xC]) & 4 != 0:  # 0
        result = result | 0x1C

    if ord(ctx[0xC]) & 2 != 0:  # 0
        result = result | 0x11

    if ord(ctx[0xC]) & 1 == 0:  # 1
        result = result | 4

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    if ord(ctx[0xD]) > 127:  # 0
        result = result | 0x16

    if ord(ctx[0xD]) & 0x40 == 0:  # 1
        result = result | 0x21

    if ord(ctx[0xD]) & 0x20 == 0:  # 1
        result = result | 2

    if ord(ctx[0xD]) & 0x10 != 0:  # 0
        result = result | 0x2D

    if ord(ctx[0xD]) & 8 == 0:  # 1
        result = result | 0x1D

    if ord(ctx[0xD]) & 4 == 0:  # 1
        result = result | 0xB

    if ord(ctx[0xD]) & 2 == 0:  # 1
        result = result | 9

    if ord(ctx[0xD]) & 1 == 0:  # 1
        result = result | 0xC

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    if ord(ctx[0xE]) > 127:  # 0
        result = result | 0x24

    if ord(ctx[0xE]) & 0x40 == 0:  # 1
        result = result | 0x12

    if ord(ctx[0xE]) & 0x20 != 0:  # 0
        result = result | 0x22

    if ord(ctx[0xE]) & 0x10 != 0:  # 0
        result = result | 0xE

    if ord(ctx[0xE]) & 8 != 0:  # 0
        result = result | 9

    if ord(ctx[0xE]) & 4 != 0:  # 0
        result = result | 2

    if ord(ctx[0xE]) & 2 == 0:  # 1
        result = result | 0x28

    if ord(ctx[0xE]) & 1 != 0:  # 0
        result = result | 0x2C

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    if ord(ctx[0xF]) > 127:  # 0
        result = result | 0x2B

    if ord(ctx[0xF]) & 0x40 == 0:  # 1
        result = result | 0x27

    if ord(ctx[0xF]) & 0x20 != 0:  # 0
        result = result | 0x21

    if ord(ctx[0xF]) & 0x10 == 0:  # 1
        result = result | 0x1F

    if ord(ctx[0xF]) & 8 == 0:  # 1
        result = result | 9

    if ord(ctx[0xF]) & 4 != 0:  # 0
        result = result | 10

    if ord(ctx[0xF]) & 2 != 0:  # 0
        result = result | 0xC

    if ord(ctx[0xF]) & 1 != 0:  # 0
        result = result | 0x23

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    if ord(ctx[0x10]) > 127:  # 0
        result = result | 7

    if ord(ctx[0x10]) & 0x40 != 0:  # 0
        result = result | 0x2B

    if ord(ctx[0x10]) & 0x20 == 0:  # 1
        result = result | 0x21

    if ord(ctx[0x10]) & 0x10 == 0:  # 1
        result = result | 0x28

    if ord(ctx[0x10]) & 8 != 0:  # 0
        result = result | 0x2B

    if ord(ctx[0x10]) & 4 != 0:  # 0
        result = result | 4

    if ord(ctx[0x10]) & 2 != 0:  # 0
        result = result | 8

    if ord(ctx[0x10]) & 1 == 0:  # 1
        result = result | 0x26

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    if ord(ctx[0x11]) > 127:  # 0
        result = result | 0x1E

    if ord(ctx[0x11]) & 0x40 == 0:  # 1
        result = result | 0x11

    if ord(ctx[0x11]) & 0x20 != 0:  # 0
        result = result | 2

    if ord(ctx[0x11]) & 0x10 != 0:  # 0
        result = result | 0x19

    if ord(ctx[0x11]) & 8 != 0:  # 0
        result = result | 0x29

    if ord(ctx[0x11]) & 4 == 0:  # 1
        result = result | 0x18

    if ord(ctx[0x11]) & 2 == 0:  # 1
        result = result | 3

    if ord(ctx[0x11]) & 1 != 0:  # 0
        result = result | 0x1D

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    if ord(ctx[0x12]) > 127:  # 0
        result = result | 0x1A

    if ord(ctx[0x12]) & 0x40 != 0:  # 0
        result = result | 0x25

    if ord(ctx[0x12]) & 0x20 == 0:  # 1
        result = result | 0x26

    if ord(ctx[0x12]) & 0x10 == 0:  # 1
        result = result | 0x11

    if ord(ctx[0x12]) & 8 == 0:  # 1
        result = result | 0x1A

    if ord(ctx[0x12]) & 4 != 0:  # 0
        result = result | 0x28

    if ord(ctx[0x12]) & 2 != 0:  # 0
        result = result | 0x15

    if ord(ctx[0x12]) & 1 != 0:  # 0
        result = result | 0x10

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

    if ord(ctx[0x13]) > 127:  # 0
        result = result | 0x27

    if ord(ctx[0x13]) & 0x40 == 0:  # 1
        result = result | 0xB

    if ord(ctx[0x13]) & 0x20 == 0:  # 1
        result = result | 0x21

    if ord(ctx[0x13]) & 0x10 != 0:  # 0
        result = result | 0x2C

    if ord(ctx[0x13]) & 8 == 0:  # 1
        result = result | 0x1C

    if ord(ctx[0x13]) & 4 == 0:  # 1
        result = result | 0xD

    if ord(ctx[0x13]) & 2 != 0:  # 0
        result = result | 0x14

    if ord(ctx[0x13]) & 1 != 0:  # 0
        result = result | 0x14

    # 00110110 00110111 01101011 01010111 00110110 01011001 01101110 01001011 01110110 01010100 01110000 01100001 01110001 01101111 01000010 01011000 00110001 01000110 00111000 01101100

    return result == 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--binary_str", required=True, dest="in_str", type=str)
    args = parser.parse_args()

    target_str = "".join([chr(int(x, base=2)) for x in args.in_str.split()])
    print(target_str)

    start_t = time.time()
    if verify(target_str):
        print("OMG")
        print(args.in_str)
        print(target_str)
    end_t = time.time()
    print(f"checked string in {end_t-start_t} seconds")


if __name__ == "__main__":
    main()
