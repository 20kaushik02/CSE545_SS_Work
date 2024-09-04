# CSE 545 pwn.college Dojo

## Project 01 Linux Lifter

### .05 - find

- `find / randomly_placed_file` - way too many files
- read the man page. `find -name randomly_placed_file` found it
- didn't specify a folder to search in tho, ig it's cuz cwd is /

### .06 - find and exec

- "Optional Exercise: Why do they think it worked with `-exec` parameter of the `find` command, but we get permission denied using standalone `cat` command? Hint: SUID bit was set for the `find` command."
- indeed, we see that `/usr/bin/find` has its *setuid* bit set:
![-rwsr-xr-x 1 root root 320160 Feb 18  2020 /usr/bin/find*](ss1.png)
- [see here](https://unix.stackexchange.com/a/389706/595039) for find stuff
- `find / -name random_cant_flag -exec cat {} ';'` worked

### .07 - return code

- `$?` is the return code of the last executed command
- range 0 to 255

### .08 - python

- SUID on python this time

### .11 - search me

- `/challenge/tester.sh` is printing `/flag` but the file is missing
- `/challenge/cp` has SUID bit set
- preliminary find revealed a possible file deep in `/tmp`
- `find /tmp/that/full/path -name flag -exec /challenge/cp {} /flag ';'`

### .12 - hash it out

- used online tool to generate SHA256

### .13 - hash full

- here we go
- a-z, 6 spaces, so 26^6 possibilities
- plaintext is 6 letters, so 48 bits. hash is SHA256 so 256 bits.
- storage per line:`<hash><plaintext>` that's 304 bits, 312 if including newline character
- total storage exceeds 11GB!!
- refinement 1: 256-bit hash is pretty unique. if we cut down on the portion of the hash stored, we should be able to save a ton of space while only slightly increasing the margin of error. let's assume plaintext has to be stored entirely for now, so total per line is 184 bits.
- eh fk it, just generated all permutations. 22GB storage, 20 min to generate, search using VSCode search took a few more minutes

## Project 02 Unwinding Binaries (Reversing)

### .01 - looking inside

- not sure how to use ghidra, didn't seem to work either
- `angr decompile /challenge/run` revealed a `strcmp` with the key, ez

### .02 - the mangler

- 'mangling' is just subtracting 3 from the char's ascii value. so just add 3 to the key

### .03 - xor plus

- mangling is adding 3 then xor with 2. so just xor with 2, then subtract 3

#### lab 2a.02

![lab code snippet](ss2.png)

- ascii values

### .04 - solve for x

- NOTE: angr screwed up, and gave an incorrect result (== instead of !=)
- use ghidra (GUI) or [dogbolt](https://dogbolt.org) for binaries under 2MB
- anyway, math solving:
  - we get a few eqns:
    - v1 = v0 - 24223
    - v3 = 5v2 - 129519
  - use these eqns to reduce from brute-force 4 nested loops to 2 nested loops
  - then verifying the rest gets us one soln
- runtime < 3 seconds

### .05 - extra verification

- angr just straight up hangs lol
- holy sh*t so many if statements
- boils down to byte by byte, check 1 or 0, check +ve or -ve (MSB)
  - 00 - 00110111
  - 01 - 01000111
  - 02 - 01000011
  - 03 - 01010110
  - 04 - 00110100
  - 05 - 01010010
  - 06 - 01011010
  - 07 - 01001001
  - 08 - 01000001
  - 09 - 00110100
  - 10 - 01011001
  - 11 - 00111000
  - 12 - 01111001
  - 13 - 00110011
  - 14 - 01110011
  - 15 - 01001000
  - 16 - 00110101
  - 17 - 00111000
  - 18 - 01101010
  - 19 - 01010111 (binary ninja and hex-rays disagreed on this, binary ninja was right)
- could have automated this smh

### .06 - extra verification II

- first ordered all if statements to get bitwise order of the string (hell.)
- for result to be 0 at the end, just don't modify it at all
- so for each if statement, check which of 0/1 makes it false (find and replace ftw)
- ascii string is 67kW6YnKvTpaqoBX1F8l
- really should have automated this
