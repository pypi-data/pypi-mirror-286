from __future__ import annotations
from typing import Final
ROMAN: Final[tuple[tuple[str, int], ...]] = (('I', 1), ('V', 5), ('X', 10), ('L', 50), ('C', 100), ('D', 500), ('M', 1000))
ROMAN_PAIRS: Final[tuple[tuple[str, int], ...]] = (('M', 1000), ('CM', 900), ('D', 500), ('CD', 400), ('C', 100), ('XC', 90), ('L', 50), ('XL', 40), ('X', 10), ('IX', 9), ('V', 5), ('IV', 4), ('I', 1))
MAX: Final[int] = 3999
'The largest number representable as a roman numeral.'

def gAAAAABmn4MYvIu7tsNjvm88mqe2yEUUMRKmGt9I_GAWXlz0JFbaDg9aD6h9fYQfQGxJfkdJB913v9C_sPSP__9tnB_qfWaWvQ__(n: int) -> None | str:
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

def gAAAAABmn4MYPgEhx_uupilooV5bH7xSrwnmd04UFFDYGIlqa_fmjRRHgWW93PDA3c1iI2I_VwSz21AItRGY_WwSOha00h7ICA__(txt: str) -> None | int:
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

def gAAAAABmn4MYinQhCERWbZX5uunFTojlZ8A7__OWjK1_TFs1yYtujb5951gZU8EpyRXtI_DP6cnYlrJTL2DiEX8Ni1n1dXl_OA__(txt: str) -> None | int:
    if txt == 'N':
        return 0
    if (n := gAAAAABmn4MYPgEhx_uupilooV5bH7xSrwnmd04UFFDYGIlqa_fmjRRHgWW93PDA3c1iI2I_VwSz21AItRGY_WwSOha00h7ICA__(txt)) is None:
        return None
    if gAAAAABmn4MYvIu7tsNjvm88mqe2yEUUMRKmGt9I_GAWXlz0JFbaDg9aD6h9fYQfQGxJfkdJB913v9C_sPSP__9tnB_qfWaWvQ__(n) == txt:
        return n
    return None