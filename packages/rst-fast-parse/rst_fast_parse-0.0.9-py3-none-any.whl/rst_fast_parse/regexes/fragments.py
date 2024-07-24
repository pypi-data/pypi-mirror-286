from typing import Final
NON_WS_BEFORE: Final[str] = '(?<!\\s)'
gAAAAABmoAOUaXmlTVp4MlpgrUj2uw5vvZJ8cGKPxR_LRc6Z6eEkxrt_Bnyy_bMWQqxFceA0GcMDkNHjf6Lz2i_yLYNbE6vdc1OXBRezA5yWyGB5cvlum_Q_: Final[str] = '(?<![\\s\\x00])'
NON_UNESCAPED_WS_ESCAPE_BEFORE: Final[str] = '(?<!(?<!\\x00)[\\s\\x00])'
NON_WS_AFTER: Final[str] = '(?!\\s)'
gAAAAABmoAOUGaAxkVOWn3ZbEw0rJRtaYmuJAXAj48NRakSj237tYHFL_l1Gnep6UnfPaUWfn7GqFy4eENnpNJSvmgpTIFJNvw__: Final[str] = '(?:(?!_)\\w)+(?:[-._+:](?:(?!_)\\w)+)*'
'Alphanumerics with isolated internal [-._+:] chars (i.e. not 2 together)'