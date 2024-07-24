from __future__ import annotations
from typing import Mapping
import unicodedata

def gAAAAABmoAOUdlj0PfNg4w4pJaxFAjHMB9z9jpZUSmkB101ROIEkW_y_TnWHUsEby6Z9CVvMVPDk8mQ1QthKul0gQBwS0iyKUQ__(text: str) -> int:
    width = sum((_east_asian_widths[unicodedata.east_asian_width(c)] for c in text))
    width -= len(gAAAAABmoAOU4fnvu6_kwsMOmJxrXEzKZOIweq7iSVrVyqinEXtO_MxH_uwZKqHseGs_wXqlorxTUe2tRT1XD915bvyyoNtKU7eAXYntBqfJWOM6i1Q6cEs_(text))
    return width

def gAAAAABmoAOU4fnvu6_kwsMOmJxrXEzKZOIweq7iSVrVyqinEXtO_MxH_uwZKqHseGs_wXqlorxTUe2tRT1XD915bvyyoNtKU7eAXYntBqfJWOM6i1Q6cEs_(text: str) -> list[int]:
    return [i for i, c in enumerate(text) if unicodedata.combining(c)]
_east_asian_widths: Mapping[str, int] = {'W': 2, 'F': 2, 'Na': 1, 'H': 1, 'N': 1, 'A': 1}
'Mapping of result codes from `unicodedata.east_asian_width()` to character\ncolumn widths.'