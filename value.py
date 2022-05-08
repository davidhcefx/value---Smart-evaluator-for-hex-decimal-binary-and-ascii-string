#! /usr/bin/env python3
"""
Smart evaluator for hex/decimal/bin/ascii strings.

$ value 48879
0xbeef
$ value 0xb
0b1011
$ value /bin/sh
0x2f62 0x696e 0x2f73 0x68
$ value 2f62696e
'/bin'
$ value 121 184 255  # RGB values
121 = 0x79
184 = 0xb8
255 = 0xff
$ value , . + -
',' = 0x2c
'.' = 0x2e
'+' = 0x2b
'-' = 0x2d
"""
from typing import List, Set, Iterable, Optional
from math import ceil
from sys import argv


def to_raw(string: str) -> str:
    res = []
    h = ''.join([hex(ord(s))[2:] for s in string])
    for i in range(0, len(h), 4):
        res.append('0x' + h[i:i+4])

    return ' '.join(res)

def _bytes_decode_quote(b: bytes) -> Optional[str]:
    try:
        return f"'{b.decode()}'"
    except UnicodeDecodeError:
        return None

def to_strings(value: int) -> Iterable[str]:
    """Try decoding value with big and/or little endians."""
    byte_size = ceil((len(hex(value)) - 2) / 2)
    return set(filter(bool, map(lambda b: _bytes_decode_quote(b),
                                map(lambda en: value.to_bytes(byte_size, en), ['big', 'little']))))

def _parse_num(string: str, base: int) -> Optional[int]:
    try:
        return int(string, base)
    except ValueError:
        return None

def parse_hex(string: str) -> Optional[int]:
    return _parse_num(string, 16)

def parse_dec(string: str) -> Optional[int]:
    return _parse_num(string, 10)

def parse_oct(string: str) -> Optional[int]:
    return _parse_num(string, 8)

def parse_bin(string: str) -> Optional[int]:
    return _parse_num(string, 2)

# TODO: better function names?
def get_values(string: str) -> Iterable[int]:
    """Return as many candidates as possible."""
    # TODO: oct support
    if string.startswith('0x'):
        return filter(bool, [parse_hex(string[2:])])
    if string.startswith('0b'):
        return filter(bool, [parse_bin(string[2:])])

    # try each base when no prefix
    return set(filter(bool, map(lambda f: f(string), [parse_hex, parse_dec, parse_bin])))

def main(string: str) -> None:
    for value in get_values(string):
        # TODO: better representing ways?
#        print(value)
        print(' = '.join([
            str(value),
            hex(value),
            bin(value),
            *to_strings(value)
        ]))

    print(f"'{string}' = {to_raw(string)}")

if __name__ == '__main__':
    if len(argv) == 1:
        print('Syntax: value STRING ...', __doc__)
        raise SystemExit(1)

    for arg in argv[1:]:
        main(arg)
