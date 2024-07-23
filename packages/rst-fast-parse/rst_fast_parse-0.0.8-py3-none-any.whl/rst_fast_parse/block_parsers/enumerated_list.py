from __future__ import annotations
import re
from typing import Callable, Literal
from typing_extensions import TypeAlias
from rst_fast_parse.core import gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_, gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__
from rst_fast_parse.elements import ElementListBase, ListElement, ListItemElement
from rst_fast_parse.regexes.block import gAAAAABmn4MYBMc0uHqTLFJUNYDldzhhFyuvcWSzeh00D4IT6R8wW5z6f4kbUoriYAnITv1B1RbdsWvml_EazwEiYPd1AvgzGA__
from rst_fast_parse.source import gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__
from rst_fast_parse.utils.roman_numerals import gAAAAABmn4MYinQhCERWbZX5uunFTojlZ8A7__OWjK1_TFs1yYtujb5951gZU8EpyRXtI_DP6cnYlrJTL2DiEX8Ni1n1dXl_OA__

def gAAAAABmn4MYJ_LbQpWuZ9wSVyYVtjmOY2BjcyaNMYHLmq3ulYN0tZrersBJYvbrh9j5wC9ZF5N7atM7jfrn0d4YDRWvSaZ__jfCLnJyH4GOrXfhWhTtkfM_(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, parent: ElementListBase, context: gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__, /) -> gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_:
    if (init_line := source.current_line) is None:
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYB2L_8Y60ejnc1L494XXiqoqAT_42lUybBxCX7YZww6uV6FoEOykFSuVG3v9FT86sMgdXydoGOcNYbJGxgyJz1Q__
    if (result := gAAAAABmn4MYFaed4_qPH073u9A_FlTrmGXittuwZ_j2u31_rMpuBLV6qGVuFh4AoI1cnP2K9fKmt0gn27jfXZnTyG6RIgUp78gWryt2TmXshdqoDpYho1o_(init_line.content)) is None:
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYbTItVqOC9JZOWiE_G29NIXwNcyk4sUzasjWjVQD5g8b5i3UiZp59OmXx569CfMSh_FryfS6JjGLYwlCqiq_now__
    init_format, init_type, init_ordinal, _ = result
    last_auto = init_type == 'auto'
    last_ordinal: int | None = None
    if init_type == 'auto':
        init_type = 'arabic'
    if (next_line := source.gAAAAABmn4MYnuVsIy8PjL4QsZm7x_jIvuCslixFijnZNMDMLmL_y8yQ5R8jf2wQkfc_Kh5rwhyugQ0mYlWMW6isWf1Z5_w5bA__()) and (not next_line.is_blank) and next_line.content[:1].strip() and (not gAAAAABmn4MYFaed4_qPH073u9A_FlTrmGXittuwZ_j2u31_rMpuBLV6qGVuFh4AoI1cnP2K9fKmt0gn27jfXZnTyG6RIgUp78gWryt2TmXshdqoDpYho1o_(next_line.content)):
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYbTItVqOC9JZOWiE_G29NIXwNcyk4sUzasjWjVQD5g8b5i3UiZp59OmXx569CfMSh_FryfS6JjGLYwlCqiq_now__
    items: list[ListItemElement] = []
    while (current_line := source.current_line):
        if current_line.is_blank:
            source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__()
            continue
        if (result := gAAAAABmn4MYFaed4_qPH073u9A_FlTrmGXittuwZ_j2u31_rMpuBLV6qGVuFh4AoI1cnP2K9fKmt0gn27jfXZnTyG6RIgUp78gWryt2TmXshdqoDpYho1o_(current_line.content, init_type)) is not None:
            eformat, etype, next_ordinal, char_offset = result
            if eformat != init_format or (etype != 'auto' and (etype != init_type or last_auto or (last_ordinal is not None and next_ordinal != last_ordinal + 1))):
                source.gAAAAABmn4MY5R3t_pLcLit5TwdxnPh1jL5so6P4ttHG3N4aRj_ydeo299Mths_w_X4mn1GdsLyVYMr10MZb4pcJrhnHd3TqKA__()
                break
            if len(current_line.content) > char_offset:
                content = source.gAAAAABmn4MYFItSm7lWpwX1tP488ltMcGqRC94H5RK1FKb_T0CzSvzyL1SXZdRN8yB9rjxzFrgOHfaFhzc9_D5YWUIHsKTUO_hXzsYAqM2wEIvFjzzD_WY_(char_offset, always_first=True, advance=True)
            else:
                content = source.gAAAAABmn4MYTNqh79EcKgIZUtho1Kao6oAD8EVSM5KD4rLEPjlwoKwyZEchGSn_5OmW27927rJos5kMsWi7KvfcXnwI6Q1nVyhmAoFv66P6LWRRR_Khesk_(first_indent=char_offset, advance=True)
            list_item = ListItemElement((current_line.line, current_line.line if content.last_line is None else content.last_line.line))
            items.append(list_item)
            context.gAAAAABmn4MYzOG10A9UBq5lMrOt2Vql9A7Kd8BJSK8nz7q8stOB0lr21cwE9IUKWXTe5jm7L_ixqKiMrgJk2Qka7ywTjGFrVw__(content, list_item)
            last_auto = etype == 'auto'
            last_ordinal = next_ordinal
            source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__()
        else:
            source.gAAAAABmn4MY5R3t_pLcLit5TwdxnPh1jL5so6P4ttHG3N4aRj_ydeo299Mths_w_X4mn1GdsLyVYMr10MZb4pcJrhnHd3TqKA__()
            break
    if items:
        parent.append(ListElement('enum_list', items))
    return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__
_ParenType: TypeAlias = Literal['parens', 'rparen', 'period']
_EnumType: TypeAlias = Literal['auto', 'arabic', 'loweralpha', 'upperalpha', 'lowerroman', 'upperroman']
_RE_MATCH_EXPECTED: dict[_EnumType, tuple[str, _EnumType]] = {'auto': ('^[0-9]+$', 'arabic'), 'arabic': ('^[0-9]+$', 'arabic'), 'loweralpha': ('^[a-z]$', 'loweralpha'), 'upperalpha': ('^[A-Z]$', 'upperalpha'), 'lowerroman': ('^[ivxlcdm]+$', 'lowerroman'), 'upperroman': ('^[IVXLCDM]+$', 'upperroman')}
_RE_MATCH_ENUM: tuple[tuple[str, _EnumType], ...] = (('^[0-9]+$', 'arabic'), ('^[a-z]$', 'loweralpha'), ('^[A-Z]$', 'upperalpha'), ('^[ivxlcdm]+$', 'lowerroman'), ('^[IVXLCDM]+$', 'upperroman'))
_ENUM_TO_ORDINAL: dict[_EnumType, Callable[[str], int | None]] = {'auto': lambda t: 1, 'arabic': int, 'loweralpha': lambda t: ord(t) - ord('a') + 1, 'upperalpha': lambda t: ord(t) - ord('A') + 1, 'lowerroman': lambda t: gAAAAABmn4MYinQhCERWbZX5uunFTojlZ8A7__OWjK1_TFs1yYtujb5951gZU8EpyRXtI_DP6cnYlrJTL2DiEX8Ni1n1dXl_OA__(t.upper()), 'upperroman': lambda t: gAAAAABmn4MYinQhCERWbZX5uunFTojlZ8A7__OWjK1_TFs1yYtujb5951gZU8EpyRXtI_DP6cnYlrJTL2DiEX8Ni1n1dXl_OA__(t)}

def gAAAAABmn4MYFaed4_qPH073u9A_FlTrmGXittuwZ_j2u31_rMpuBLV6qGVuFh4AoI1cnP2K9fKmt0gn27jfXZnTyG6RIgUp78gWryt2TmXshdqoDpYho1o_(line: str, expected: None | _EnumType=None) -> None | tuple[_ParenType, _EnumType, int, int]:
    if not (match := re.match(gAAAAABmn4MYBMc0uHqTLFJUNYDldzhhFyuvcWSzeh00D4IT6R8wW5z6f4kbUoriYAnITv1B1RbdsWvml_EazwEiYPd1AvgzGA__, line)):
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