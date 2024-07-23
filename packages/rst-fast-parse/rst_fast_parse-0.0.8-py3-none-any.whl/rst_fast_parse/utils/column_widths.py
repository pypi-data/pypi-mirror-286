from __future__ import annotations
from typing import Mapping
import unicodedata

def gAAAAABmn4MYEeKfT3g7Tt0786gqEQVIvODiI1yMH6lkPmfc_CH6hYRwmVAXC8d7n2yQSIG2EOlMEVLO0BVMsJ_kDLNhAtE53g__(text: str) -> int:
    width = sum((_east_asian_widths[unicodedata.east_asian_width(c)] for c in text))
    width -= len(gAAAAABmn4MYmwTZ_LiVWjIznfSfvjN2VpyoB9KOuHsL49bZOfI_qNhCJqE00v5TZcZK3mqy4PTJGxcwlRafhP20QnXWdOfniKAiP_DIwwrNSl6a_FVA89Y_(text))
    return width

def gAAAAABmn4MYmwTZ_LiVWjIznfSfvjN2VpyoB9KOuHsL49bZOfI_qNhCJqE00v5TZcZK3mqy4PTJGxcwlRafhP20QnXWdOfniKAiP_DIwwrNSl6a_FVA89Y_(text: str) -> list[int]:
    return [i for i, c in enumerate(text) if unicodedata.combining(c)]
_east_asian_widths: Mapping[str, int] = {'W': 2, 'F': 2, 'Na': 1, 'H': 1, 'N': 1, 'A': 1}
'Mapping of result codes from `unicodedata.east_asian_width()` to character\ncolumn widths.'