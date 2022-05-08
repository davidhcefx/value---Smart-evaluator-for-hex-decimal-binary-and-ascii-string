from typing import List, Tuple
import re
import value
import pytest


def both_appear_same_line(text1: str, text2: str, lines: List[str]) -> bool:
    for line in lines:
        if text1 in line and text2 in line:
            return True
    return False

def remove_comments(line: str) -> str:
    return re.sub(r' # [^\'"]+$', '', line)

def parse_testcase(testcase: str) -> Tuple[List[str], List[str]]:
    """Parse a doctest single testcase; return the input args and expect ouputs."""
    lines = testcase.split('\n')
    return (remove_comments(lines[0]).split(), lines[1:])

def test_doc(capfd):
    """Test with testcases within the module doc."""
    for testcase in value.__doc__.split('\n$ ')[1:]:
        args, expected = parse_testcase(testcase)
        for arg, exp in zip(args[1:], expected):
            value.show_value(arg)
            assert both_appear_same_line(arg, exp.split(' = ')[-1],
                                         capfd.readouterr().out.split('\n'))
