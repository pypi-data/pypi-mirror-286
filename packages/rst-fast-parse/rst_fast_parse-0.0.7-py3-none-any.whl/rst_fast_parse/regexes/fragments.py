from typing import Final
NON_WS_BEFORE: Final[str] = '(?<!\\s)'
gAAAAABmnuojdqDdqooqn0WESQ_Ep2CMAJv3BVn0QmuMhCrYP7B7fT1hUFh2KVC0TysevT6niEK10WkGt3u24eP1vv1fS3Q53dWg3_QwRmLOXEYESjQG_ok_: Final[str] = '(?<![\\s\\x00])'
NON_UNESCAPED_WS_ESCAPE_BEFORE: Final[str] = '(?<!(?<!\\x00)[\\s\\x00])'
NON_WS_AFTER: Final[str] = '(?!\\s)'
gAAAAABmnuojD7BFIPGBXIamkjQNTG0GLPkISNiBUyA1_FVicw867gvftCi7_tN_61kMS4y__kd6s215EP1ZT6clpfAU9ckvVg__: Final[str] = '(?:(?!_)\\w)+(?:[-._+:](?:(?!_)\\w)+)*'
'Alphanumerics with isolated internal [-._+:] chars (i.e. not 2 together)'