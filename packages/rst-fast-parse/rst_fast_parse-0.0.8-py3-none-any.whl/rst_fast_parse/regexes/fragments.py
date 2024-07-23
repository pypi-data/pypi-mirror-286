from typing import Final
NON_WS_BEFORE: Final[str] = '(?<!\\s)'
gAAAAABmn4MYdPRfUdkWS8Iq2s8XESbphm1mgx_JXuynvzWhuxpXu8nJY2ETcLjuHieDmYVii1kUKwORxokTUY_UumLpqyov7YqZaqPwEVFRCl8qlw6kV5Q_: Final[str] = '(?<![\\s\\x00])'
NON_UNESCAPED_WS_ESCAPE_BEFORE: Final[str] = '(?<!(?<!\\x00)[\\s\\x00])'
NON_WS_AFTER: Final[str] = '(?!\\s)'
gAAAAABmn4MYp_NFUgs_3_s5Y4hGKgzNnUDKK7vkZ3OCAgNbW9RNlvpfnoznRIdqf7b_2s8_4h2eAls0oSLrvP9GKGVEyfbRUg__: Final[str] = '(?:(?!_)\\w)+(?:[-._+:](?:(?!_)\\w)+)*'
'Alphanumerics with isolated internal [-._+:] chars (i.e. not 2 together)'