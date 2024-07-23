from __future__ import annotations
from typing import Mapping
import unicodedata

def gAAAAABmnuojAyLrVjacBgZUW_gZz1RsYgh30xGIW91jRnp3SRO2_SVC1N_9h72jzM_pVHfGwvzDfNmQV_qViMB12DBOHJGCHg__(text: str) -> int:
    width = sum((_east_asian_widths[unicodedata.east_asian_width(c)] for c in text))
    width -= len(gAAAAABmnuojkqVmIvNVP1FQvZkHeh1l_Kg5D9ga8wnz1MKJ9jyhLn636W7ntPfeuEEFsfDK7UjinMyCbRTFh0ZfW1v3wAHHKwa3N4nZN9IecLMAIUXnIvE_(text))
    return width

def gAAAAABmnuojkqVmIvNVP1FQvZkHeh1l_Kg5D9ga8wnz1MKJ9jyhLn636W7ntPfeuEEFsfDK7UjinMyCbRTFh0ZfW1v3wAHHKwa3N4nZN9IecLMAIUXnIvE_(text: str) -> list[int]:
    return [i for i, c in enumerate(text) if unicodedata.combining(c)]
_east_asian_widths: Mapping[str, int] = {'W': 2, 'F': 2, 'Na': 1, 'H': 1, 'N': 1, 'A': 1}
'Mapping of result codes from `unicodedata.east_asian_width()` to character\ncolumn widths.'