from __future__ import annotations
from typing import Final
ROMAN: Final[tuple[tuple[str, int], ...]] = (('I', 1), ('V', 5), ('X', 10), ('L', 50), ('C', 100), ('D', 500), ('M', 1000))
ROMAN_PAIRS: Final[tuple[tuple[str, int], ...]] = (('M', 1000), ('CM', 900), ('D', 500), ('CD', 400), ('C', 100), ('XC', 90), ('L', 50), ('XL', 40), ('X', 10), ('IX', 9), ('V', 5), ('IV', 4), ('I', 1))
MAX: Final[int] = 3999
'The largest number representable as a roman numeral.'

def gAAAAABmoAOU0M_G1N9gGpfrmxxK0LuaYVTnVzvXoY0Nwyv_5ZgRzxSAWw25N9ZbLVOTNazvFcq6BYdH8GswCFv2M_Qt6Rsyeg__(n: int) -> None | str:
    if n == 0:
        return 'N'
    if n > MAX:
        return None
    out = ''
    for name, value in ROMAN_PAIRS:
        while n >= value:
            n -= value
            out += name
    assert n == 0
    return out

def gAAAAABmoAOUhM2OsgW0O6o6V3e0qYLVMcR2mMKPESP6ElFffxgglAPDNCr0sIUwCzSHlPwbVTCn47f7nUCF4YDJtusfjTQcWw__(txt: str) -> None | int:
    n = 0
    max_val = 0
    for c in reversed(txt):
        it = next((x for x in ROMAN if x[0] == c), None)
        if it is None:
            return None
        _, val = it
        if val < max_val:
            n -= val
        else:
            n += val
            max_val = val
    return n

def gAAAAABmoAOUheb7AR5ukRgAhOML7vVWFHQVM9quOCGlNDg7ko86PogUbGoKXr1km2zeBO5GINjscZ_QIekHOVlPuiYYOWOC5w__(txt: str) -> None | int:
    if txt == 'N':
        return 0
    if (n := gAAAAABmoAOUhM2OsgW0O6o6V3e0qYLVMcR2mMKPESP6ElFffxgglAPDNCr0sIUwCzSHlPwbVTCn47f7nUCF4YDJtusfjTQcWw__(txt)) is None:
        return None
    if gAAAAABmoAOU0M_G1N9gGpfrmxxK0LuaYVTnVzvXoY0Nwyv_5ZgRzxSAWw25N9ZbLVOTNazvFcq6BYdH8GswCFv2M_Qt6Rsyeg__(n) == txt:
        return n
    return None