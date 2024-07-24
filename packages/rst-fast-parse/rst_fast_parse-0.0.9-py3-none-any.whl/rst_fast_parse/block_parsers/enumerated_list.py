from __future__ import annotations
import re
from typing import Callable, Literal
from typing_extensions import TypeAlias
from rst_fast_parse.core import gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_, gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__
from rst_fast_parse.elements import ElementListBase, ListElement, ListItemElement
from rst_fast_parse.regexes.block import gAAAAABmoAOUCX4qbDAo6ca43j8gQxClIhbGmk2TBfxXidgRyEBusUpZzIAFZtvfheHobJRNBP6_wVtC0m4qzV97aUPcJrN33Q__
from rst_fast_parse.source import gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__
from rst_fast_parse.utils.roman_numerals import gAAAAABmoAOUheb7AR5ukRgAhOML7vVWFHQVM9quOCGlNDg7ko86PogUbGoKXr1km2zeBO5GINjscZ_QIekHOVlPuiYYOWOC5w__

def gAAAAABmoAOUWMukC3xWibby_gWTQjsrg2NXLqBXikahSkcMtU0pJKKOwRPgbuPIdRz0W6_1AQswYpCc7yFZSoCfC251hVSr1K_9Vv9LYIVv1HbvaL2LHNE_(source: gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__, parent: ElementListBase, context: gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__, /) -> gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_:
    if (init_line := source.current_line) is None:
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUjd_6MxHjEtt1TugiZ6yaacbq1nREHVx2Fk2T_2621FG1CjXnhtaIU_bVoJ1U7KN1_WjYt6NyPEGMdldCcwNscQ__
    if (result := gAAAAABmoAOUUMM_b44Qe5aoIv70oxG0wfjqEQIIepuTqcNaKtKmCLWXw7vHvC9AS69hH2ZbLTcHh5Sp9nT6MaX07pt644B0NxtepYJK4IXumtN29UB__WQ_(init_line.content)) is None:
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUproF_iscOFcDNKNx2ui84_7alGaIdXM1oeGJa_ugCTaycwn7oF_8z7vOlFa_DGDwPP5T44koPx_ElivNotdd7A__
    init_format, init_type, init_ordinal, _ = result
    last_auto = init_type == 'auto'
    last_ordinal: int | None = None
    if init_type == 'auto':
        init_type = 'arabic'
    if (next_line := source.gAAAAABmoAOU4MROUYia9kJe75WM4gcw9LvrTZXAqyYK7_Ax0bicP68Y_yrusuxyIyyGjE_JLwwpuAjWfnUpxSISbSe_h_y4IQ__()) and (not next_line.is_blank) and next_line.content[:1].strip() and (not gAAAAABmoAOUUMM_b44Qe5aoIv70oxG0wfjqEQIIepuTqcNaKtKmCLWXw7vHvC9AS69hH2ZbLTcHh5Sp9nT6MaX07pt644B0NxtepYJK4IXumtN29UB__WQ_(next_line.content)):
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUproF_iscOFcDNKNx2ui84_7alGaIdXM1oeGJa_ugCTaycwn7oF_8z7vOlFa_DGDwPP5T44koPx_ElivNotdd7A__
    items: list[ListItemElement] = []
    while (current_line := source.current_line):
        if current_line.is_blank:
            source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__()
            continue
        if (result := gAAAAABmoAOUUMM_b44Qe5aoIv70oxG0wfjqEQIIepuTqcNaKtKmCLWXw7vHvC9AS69hH2ZbLTcHh5Sp9nT6MaX07pt644B0NxtepYJK4IXumtN29UB__WQ_(current_line.content, init_type)) is not None:
            eformat, etype, next_ordinal, char_offset = result
            if eformat != init_format or (etype != 'auto' and (etype != init_type or last_auto or (last_ordinal is not None and next_ordinal != last_ordinal + 1))):
                source.gAAAAABmoAOUXBPdo9OkaxYoAc4gGo8fBfuw88NaQvW9F6dJXeOAGnTz4uetdGLdeffAFTTUljLpCo2l_WvJvzJc40wY5KLzCg__()
                break
            if len(current_line.content) > char_offset:
                content = source.gAAAAABmoAOUs2F_NH1Cb00_oxoXB1TsXtVTVkPYZAHFgA4IyJNmDri28ayNie1nOhlRWjfnUiynPZjRIPY_BJVs29L0xnbPz8e1uLfnnr_lJuL8qmYpNMM_(char_offset, always_first=True, advance=True)
            else:
                content = source.gAAAAABmoAOUrqn_gdTR2OA_oxNqRDfXHdf_AoAj9pIcLZiZCzUC1qCoNCI3jgHyx6fa_OrI5HWOaRLsSVT_EGSzmy5ld108GoCSb3jWHLN0wWbNcgb_f10_(first_indent=char_offset, advance=True)
            list_item = ListItemElement((current_line.line, current_line.line if content.last_line is None else content.last_line.line))
            items.append(list_item)
            context.gAAAAABmoAOUjwOEnh8OvcV78z8zUYoqJJ0Y2TrThUDOYQObmZ9KKZuVx0fs2RHsOQai0Er2b51fz7_55XcSDLfrKPsEXT3Abw__(content, list_item)
            last_auto = etype == 'auto'
            last_ordinal = next_ordinal
            source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__()
        else:
            source.gAAAAABmoAOUXBPdo9OkaxYoAc4gGo8fBfuw88NaQvW9F6dJXeOAGnTz4uetdGLdeffAFTTUljLpCo2l_WvJvzJc40wY5KLzCg__()
            break
    if items:
        parent.append(ListElement('enum_list', items))
    return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__
_ParenType: TypeAlias = Literal['parens', 'rparen', 'period']
_EnumType: TypeAlias = Literal['auto', 'arabic', 'loweralpha', 'upperalpha', 'lowerroman', 'upperroman']
_RE_MATCH_EXPECTED: dict[_EnumType, tuple[str, _EnumType]] = {'auto': ('^[0-9]+$', 'arabic'), 'arabic': ('^[0-9]+$', 'arabic'), 'loweralpha': ('^[a-z]$', 'loweralpha'), 'upperalpha': ('^[A-Z]$', 'upperalpha'), 'lowerroman': ('^[ivxlcdm]+$', 'lowerroman'), 'upperroman': ('^[IVXLCDM]+$', 'upperroman')}
_RE_MATCH_ENUM: tuple[tuple[str, _EnumType], ...] = (('^[0-9]+$', 'arabic'), ('^[a-z]$', 'loweralpha'), ('^[A-Z]$', 'upperalpha'), ('^[ivxlcdm]+$', 'lowerroman'), ('^[IVXLCDM]+$', 'upperroman'))
_ENUM_TO_ORDINAL: dict[_EnumType, Callable[[str], int | None]] = {'auto': lambda t: 1, 'arabic': int, 'loweralpha': lambda t: ord(t) - ord('a') + 1, 'upperalpha': lambda t: ord(t) - ord('A') + 1, 'lowerroman': lambda t: gAAAAABmoAOUheb7AR5ukRgAhOML7vVWFHQVM9quOCGlNDg7ko86PogUbGoKXr1km2zeBO5GINjscZ_QIekHOVlPuiYYOWOC5w__(t.upper()), 'upperroman': lambda t: gAAAAABmoAOUheb7AR5ukRgAhOML7vVWFHQVM9quOCGlNDg7ko86PogUbGoKXr1km2zeBO5GINjscZ_QIekHOVlPuiYYOWOC5w__(t)}

def gAAAAABmoAOUUMM_b44Qe5aoIv70oxG0wfjqEQIIepuTqcNaKtKmCLWXw7vHvC9AS69hH2ZbLTcHh5Sp9nT6MaX07pt644B0NxtepYJK4IXumtN29UB__WQ_(line: str, expected: None | _EnumType=None) -> None | tuple[_ParenType, _EnumType, int, int]:
    if not (match := re.match(gAAAAABmoAOUCX4qbDAo6ca43j8gQxClIhbGmk2TBfxXidgRyEBusUpZzIAFZtvfheHobJRNBP6_wVtC0m4qzV97aUPcJrN33Q__, line)):
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