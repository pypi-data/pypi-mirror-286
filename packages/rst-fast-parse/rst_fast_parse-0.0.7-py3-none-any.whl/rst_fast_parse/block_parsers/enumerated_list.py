from __future__ import annotations
import re
from typing import Callable, Literal
from typing_extensions import TypeAlias
from rst_fast_parse.core import gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_, gAAAAABmnuojyVOa__SFl52_gl5XSUoa6WT6zDtvviRWWFizGdPPVlComyZy1vRGpEh8_otsfmmSedteHWUAmThA0ExDLAlJng__
from rst_fast_parse.elements import ElementListBase, ListElement, ListItemElement
from rst_fast_parse.regexes.block import gAAAAABmnuojvIt_PpjJr24RLliunuY0LyDk1Gsm0ZgIwAQQad_jpiKnFYOcbXahn6zbWc_P1_8ZhvEGC7i8nNe2_N_YiBUDCA__
from rst_fast_parse.source import gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__
from rst_fast_parse.utils.roman_numerals import gAAAAABmnuojvk55__1FoKuPUSJj0JGmFG4j_wfqZ_XmxAVqhXiVcWgo6StNCL3V21DIhnruy5KTchqpvoxo0EwXkMqDcyCUWg__

def gAAAAABmnuojaLTymOKdK7gZCIcztKfsJZm8VQ7wxPqA__CNC2EaAu4hYohdhOMu_KSCJnJSHFBCrgIylPOM0L_vi88YKtuHN_zMddHQuZOMy0sneaZQ8_M_(source: gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__, parent: ElementListBase, context: gAAAAABmnuojyVOa__SFl52_gl5XSUoa6WT6zDtvviRWWFizGdPPVlComyZy1vRGpEh8_otsfmmSedteHWUAmThA0ExDLAlJng__, /) -> gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_:
    if (init_line := source.current_line) is None:
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuoj3aryYICdV_DRXww7_sB4t47whKoHzQbi63L259co7hXyWE0ipEj7HxYbUAe60Pyz7XEQS8izK2QkZQBfWccvGA__
    if (result := gAAAAABmnuojqx8cwcV7NPrzQnSOfcfZN7aPgqkosPs0yvrMPmocr70siYknpdWU0E7wWvV7WzZwUSivhWg45dGPbtLPqKcVk74Ql2aFTjseNH6eIjzr5J4_(init_line.content)) is None:
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojR_bJJWp1wWXX31xmpSl2WA0iZ_2vj_rM1BM92DiLOoC4J721_7xFn9SMsRxwfsPt9SqBKEJ_kEySibY1UPR4pA__
    init_format, init_type, init_ordinal, _ = result
    last_auto = init_type == 'auto'
    last_ordinal: int | None = None
    if init_type == 'auto':
        init_type = 'arabic'
    if (next_line := source.gAAAAABmnuojE1KGsr0TOFHaREF1loYgV0lWiRlfD2YdF5asAdfPtOfBkAv_9JkPtm8YOU_PzWoISZ4FTPPO1DO1m6oXqtClug__()) and (not next_line.is_blank) and next_line.content[:1].strip() and (not gAAAAABmnuojqx8cwcV7NPrzQnSOfcfZN7aPgqkosPs0yvrMPmocr70siYknpdWU0E7wWvV7WzZwUSivhWg45dGPbtLPqKcVk74Ql2aFTjseNH6eIjzr5J4_(next_line.content)):
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojR_bJJWp1wWXX31xmpSl2WA0iZ_2vj_rM1BM92DiLOoC4J721_7xFn9SMsRxwfsPt9SqBKEJ_kEySibY1UPR4pA__
    items: list[ListItemElement] = []
    while (current_line := source.current_line):
        if current_line.is_blank:
            source.gAAAAABmnuojVTLADCMhqSUy7AGOzFTv5zQO7PfrX9LR3rUNi_CB4ZCiOXdZh9_VenkdmSFTLhtSCRIzFtgq8r_N1_HDY6BEXQ__()
            continue
        if (result := gAAAAABmnuojqx8cwcV7NPrzQnSOfcfZN7aPgqkosPs0yvrMPmocr70siYknpdWU0E7wWvV7WzZwUSivhWg45dGPbtLPqKcVk74Ql2aFTjseNH6eIjzr5J4_(current_line.content, init_type)) is not None:
            eformat, etype, next_ordinal, char_offset = result
            if eformat != init_format or (etype != 'auto' and (etype != init_type or last_auto or (last_ordinal is not None and next_ordinal != last_ordinal + 1))):
                source.gAAAAABmnuojFuII4OCpHZwcIp1Y0A24sqLJdbVvUiEzZecco_KkrjXr9hNj_sIm4wrObGlr4MgBd_mhW0lRDBvwBKTFizqhOg__()
                break
            if len(current_line.content) > char_offset:
                content = source.gAAAAABmnuojpySrbzuZYeTbEo3VhgV4NCdu0GmdD4iQGou5kgHjcagNjvBWTUvijeI_CSD_kGirgiU6LWwIvH4BJcG9ljlua8ypcTHzhjAmikp085G_g18_(char_offset, always_first=True, advance=True)
            else:
                content = source.gAAAAABmnuojE0sYzkyFiqkGch85WYnsBvxpSsWEDOAyu6fnrOTGmq5i8vxuUbKHNHIbgq92u_ta1r_465lW6tMmp2ZI4EIybmsXLwScIEmasFmGdTUvFq4_(first_indent=char_offset, advance=True)
            list_item = ListItemElement((current_line.line, current_line.line if content.last_line is None else content.last_line.line))
            items.append(list_item)
            last_auto = etype == 'auto'
            last_ordinal = next_ordinal
            source.gAAAAABmnuojVTLADCMhqSUy7AGOzFTv5zQO7PfrX9LR3rUNi_CB4ZCiOXdZh9_VenkdmSFTLhtSCRIzFtgq8r_N1_HDY6BEXQ__()
        else:
            source.gAAAAABmnuojFuII4OCpHZwcIp1Y0A24sqLJdbVvUiEzZecco_KkrjXr9hNj_sIm4wrObGlr4MgBd_mhW0lRDBvwBKTFizqhOg__()
            break
    if items:
        parent.append(ListElement('enum_list', items))
    return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojtU2CTonP1efvRT0U3D0L4E8tQyVcnyaVUqjd_dBklWx22oUnxvHWm2H7oC1AQawAgtG_0_w_D1HolzhKwUking__
_ParenType: TypeAlias = Literal['parens', 'rparen', 'period']
_EnumType: TypeAlias = Literal['auto', 'arabic', 'loweralpha', 'upperalpha', 'lowerroman', 'upperroman']
_RE_MATCH_EXPECTED: dict[_EnumType, tuple[str, _EnumType]] = {'auto': ('^[0-9]+$', 'arabic'), 'arabic': ('^[0-9]+$', 'arabic'), 'loweralpha': ('^[a-z]$', 'loweralpha'), 'upperalpha': ('^[A-Z]$', 'upperalpha'), 'lowerroman': ('^[ivxlcdm]+$', 'lowerroman'), 'upperroman': ('^[IVXLCDM]+$', 'upperroman')}
_RE_MATCH_ENUM: tuple[tuple[str, _EnumType], ...] = (('^[0-9]+$', 'arabic'), ('^[a-z]$', 'loweralpha'), ('^[A-Z]$', 'upperalpha'), ('^[ivxlcdm]+$', 'lowerroman'), ('^[IVXLCDM]+$', 'upperroman'))
_ENUM_TO_ORDINAL: dict[_EnumType, Callable[[str], int | None]] = {'auto': lambda t: 1, 'arabic': int, 'loweralpha': lambda t: ord(t) - ord('a') + 1, 'upperalpha': lambda t: ord(t) - ord('A') + 1, 'lowerroman': lambda t: gAAAAABmnuojvk55__1FoKuPUSJj0JGmFG4j_wfqZ_XmxAVqhXiVcWgo6StNCL3V21DIhnruy5KTchqpvoxo0EwXkMqDcyCUWg__(t.upper()), 'upperroman': lambda t: gAAAAABmnuojvk55__1FoKuPUSJj0JGmFG4j_wfqZ_XmxAVqhXiVcWgo6StNCL3V21DIhnruy5KTchqpvoxo0EwXkMqDcyCUWg__(t)}

def gAAAAABmnuojqx8cwcV7NPrzQnSOfcfZN7aPgqkosPs0yvrMPmocr70siYknpdWU0E7wWvV7WzZwUSivhWg45dGPbtLPqKcVk74Ql2aFTjseNH6eIjzr5J4_(line: str, expected: None | _EnumType=None) -> None | tuple[_ParenType, _EnumType, int, int]:
    if not (match := re.match(gAAAAABmnuojvIt_PpjJr24RLliunuY0LyDk1Gsm0ZgIwAQQad_jpiKnFYOcbXahn6zbWc_P1_8ZhvEGC7i8nNe2_N_YiBUDCA__, line)):
        return None
    fmt: _ParenType
    for fmt in ('parens', 'rparen', 'period'):
        if (submatch := match.group(fmt)):
            text: str = submatch[:-1]
            if fmt == 'parens':
                text = text[1:]
            break
    else:
        raise RuntimeError(f'enumerator format not matched: {line!r}')
    sequence: None | _EnumType = None
    if text == '#':
        sequence = 'auto'
    elif expected is not None:
        regex, result = _RE_MATCH_EXPECTED[expected]
        if re.match(regex, text):
            sequence = result
    elif text == 'i':
        sequence = 'lowerroman'
    elif text == 'I':
        sequence = 'upperroman'
    if sequence is None:
        for regex, result in _RE_MATCH_ENUM:
            if re.match(regex, text):
                sequence = result
                break
        else:
            raise RuntimeError(f'enumerator sequence not matched: {text!r}')
    if (ordinal := _ENUM_TO_ORDINAL[sequence](text)) is None:
        return None
    return (fmt, sequence, ordinal, match.end(0))