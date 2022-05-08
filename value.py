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
$ value + - , .
'+' = 0x2b
'-' = 0x2d
',' = 0x2c
'.' = 0x2e
"""
from typing import Iterable, Optional
from collections import Counter
from math import ceil
from sys import argv


def to_bytes(string: str) -> str:
    """Convert string to space seperated octates (big endian); two octates a group."""
    _bytes = string.encode()
    return ' '.join(hex(int.from_bytes(_bytes[i:i+2], 'big')) for i in range(0, len(_bytes), 2))

def _bytes_decode_quote(b: bytes) -> Optional[str]:
    try:
        return f"'{b.decode()}'"
    except UnicodeDecodeError:
        return None

def to_strings(value: int) -> Iterable[str]:
    """Try decoding value with big and/or little endian."""
    byte_size = ceil((len(hex(value)) - 2) / 2)
    return Counter(filter(bool, map(lambda b: _bytes_decode_quote(b),  # type: ignore[arg-type,return-value]
                                    map(lambda e: value.to_bytes(byte_size, e), ['big', 'little']))))

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

def get_all_values(string: str) -> Iterable[int]:
    """Return all kinds of candidates, with ordering: Dec, Hex, Oct, Bin."""
    if string.startswith('0x'):
        return filter(bool, [parse_hex(string[2:])])  # type: ignore[list-item]
    if string.startswith('0o'):
        return filter(bool, [parse_oct(string[2:])])  # type: ignore[list-item]
    if string.startswith('0b'):
        return filter(bool, [parse_bin(string[2:])])  # type: ignore[list-item]

    # try each base when no prefix
    return Counter(filter(bool, map(lambda f: f(string),  # type: ignore[arg-type,return-value]
                                    [parse_dec, parse_hex, parse_oct, parse_bin])))

def show_value(string: str) -> None:
    print('Dec | Hex | Oct | Bin | String')
    print('--- | --- | --- | --- | ---')
    for val in get_all_values(string):
        print(' | '.join([str(val), hex(val), oct(val), bin(val), ' or '.join(to_strings(val))]))

    print("{:20} == '{}'\n".format(to_bytes(string), string))


if __name__ == '__main__':
    if len(argv) == 1:
        print('Syntax: value STRING ...', __doc__)
        raise SystemExit(1)

    for arg in argv[1:]:
        show_value(arg)
