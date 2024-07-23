from __future__ import annotations
import re
from rst_fast_parse.core import gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_, gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__
from rst_fast_parse.elements import ElementListBase, ListElement, ListItemElement
from rst_fast_parse.regexes.block import gAAAAABmn4MYCW8ldmP0Lm6PF2ndF2Y4DTvOTJmgRvDxtTTeHo7k_BoGCFIqRanw5ZpiJV2m4tOdMzSUG11bCXhqXYLw1Da1p17K2GMkNisSgFlQUOPU2RU_
from rst_fast_parse.source import gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__

def gAAAAABmn4MY2DpOw5CVRtjXO5zyaBixYoehEwyruB0DaFDdDAZzdoNQz7RVWB5sRCeM7J51tCa_N0CU3nPBddz9uHzJkzjzG08x9G_CPjDfqxDVdGMcjhM_(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, parent: ElementListBase, context: gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__, /) -> gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_:
    if not (first_line := source.current_line):
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYB2L_8Y60ejnc1L494XXiqoqAT_42lUybBxCX7YZww6uV6FoEOykFSuVG3v9FT86sMgdXydoGOcNYbJGxgyJz1Q__
    if not (match := re.match(gAAAAABmn4MYCW8ldmP0Lm6PF2ndF2Y4DTvOTJmgRvDxtTTeHo7k_BoGCFIqRanw5ZpiJV2m4tOdMzSUG11bCXhqXYLw1Da1p17K2GMkNisSgFlQUOPU2RU_, first_line.content)):
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYbTItVqOC9JZOWiE_G29NIXwNcyk4sUzasjWjVQD5g8b5i3UiZp59OmXx569CfMSh_FryfS6JjGLYwlCqiq_now__
    symbol: str = match.group(1)
    items: list[ListItemElement] = []
    while (current_line := source.current_line):
        if current_line.is_blank:
            source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__()
            continue
        if (match := re.match(gAAAAABmn4MYCW8ldmP0Lm6PF2ndF2Y4DTvOTJmgRvDxtTTeHo7k_BoGCFIqRanw5ZpiJV2m4tOdMzSUG11bCXhqXYLw1Da1p17K2GMkNisSgFlQUOPU2RU_, current_line.content)):
            next_symbol: str = match.group(1)
            if next_symbol != symbol:
                source.gAAAAABmn4MY5R3t_pLcLit5TwdxnPh1jL5so6P4ttHG3N4aRj_ydeo299Mths_w_X4mn1GdsLyVYMr10MZb4pcJrhnHd3TqKA__()
                break
            first_indent = match.end(0)
            if len(current_line.content) > first_indent:
                content = source.gAAAAABmn4MYFItSm7lWpwX1tP488ltMcGqRC94H5RK1FKb_T0CzSvzyL1SXZdRN8yB9rjxzFrgOHfaFhzc9_D5YWUIHsKTUO_hXzsYAqM2wEIvFjzzD_WY_(first_indent, always_first=True, advance=True)
            else:
                content = source.gAAAAABmn4MYTNqh79EcKgIZUtho1Kao6oAD8EVSM5KD4rLEPjlwoKwyZEchGSn_5OmW27927rJos5kMsWi7KvfcXnwI6Q1nVyhmAoFv66P6LWRRR_Khesk_(first_indent=first_indent, advance=True)
            list_item = ListItemElement((current_line.line, current_line.line if content.last_line is None else content.last_line.line))
            items.append(list_item)
            context.gAAAAABmn4MYzOG10A9UBq5lMrOt2Vql9A7Kd8BJSK8nz7q8stOB0lr21cwE9IUKWXTe5jm7L_ixqKiMrgJk2Qka7ywTjGFrVw__(content, list_item)
            source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__()
        else:
            source.gAAAAABmn4MY5R3t_pLcLit5TwdxnPh1jL5so6P4ttHG3N4aRj_ydeo299Mths_w_X4mn1GdsLyVYMr10MZb4pcJrhnHd3TqKA__()
            break
    if items:
        parent.append(ListElement('bullet_list', items))
    return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__