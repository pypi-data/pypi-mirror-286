from __future__ import annotations
import re
from rst_fast_parse.block_parsers.fallback import gAAAAABmn4MYf0njqRPTsYiBbt6fiBQSV0TYAaDixMXvMgEhoZ8l5kmC3WL8uNy7GW8mhoSaqftINj2RmQwUyjd0bVjDUVgJXA__
from rst_fast_parse.core import gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_, gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__
from rst_fast_parse.elements import ElementListBase, ListElement, ListItemElement
from rst_fast_parse.regexes.block import gAAAAABmn4MYP_YzlYIRxlrQIxIx8SyTrWKTYJt4_QtNPgitW7CIwxRYd_YzVdSvqRDzRRbEOi6nCS9t9vcA2J_rr_Z5XcplSITGHO0kSRzptBN_w5NlCs8_
from rst_fast_parse.source import gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__

def gAAAAABmn4MYiSx47RSfMznSKy0434f9o7VWKctiu8TLjQNu8wYO3Xv5lctNeYmJJN6WNgR_RR6VdPDrl69_9Y9redwVVVDWjyN_6Aer6_fURiBzB3e4c0I_(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, parent: ElementListBase, context: gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__, /) -> gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_:
    if not (_current_line := source.current_line):
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYB2L_8Y60ejnc1L494XXiqoqAT_42lUybBxCX7YZww6uV6FoEOykFSuVG3v9FT86sMgdXydoGOcNYbJGxgyJz1Q__
    if not (_ := re.match(gAAAAABmn4MYP_YzlYIRxlrQIxIx8SyTrWKTYJt4_QtNPgitW7CIwxRYd_YzVdSvqRDzRRbEOi6nCS9t9vcA2J_rr_Z5XcplSITGHO0kSRzptBN_w5NlCs8_, _current_line.content)):
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYbTItVqOC9JZOWiE_G29NIXwNcyk4sUzasjWjVQD5g8b5i3UiZp59OmXx569CfMSh_FryfS6JjGLYwlCqiq_now__
    items: list[ListItemElement] = []
    while (current_line := source.current_line):
        if current_line.is_blank:
            source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__()
            continue
        if (match := re.match(gAAAAABmn4MYP_YzlYIRxlrQIxIx8SyTrWKTYJt4_QtNPgitW7CIwxRYd_YzVdSvqRDzRRbEOi6nCS9t9vcA2J_rr_Z5XcplSITGHO0kSRzptBN_w5NlCs8_, current_line.content)):
            initial_index = source.current_index
            content = source.gAAAAABmn4MYTNqh79EcKgIZUtho1Kao6oAD8EVSM5KD4rLEPjlwoKwyZEchGSn_5OmW27927rJos5kMsWi7KvfcXnwI6Q1nVyhmAoFv66P6LWRRR_Khesk_(first_indent=match.end(0), advance=True)
            if not content.gAAAAABmn4MYOhdG3jdRtEl14WPRZCpCcMmJQpcmnswQsDsgyhnIlaFBEVJjImyefVR2nmNCYNl9kCrvNqXt1MlEf6S9iUHGag__():
                source.gAAAAABmn4MYINuiuD2MpLdUpsj0dpofZ5MDZXGL24BtQUwkF6Y3v7Qw0g_1GxmzMe83cavfzpZNHPyOnrzsaRjMJdC4OkFNp9SWHVc4zdTzlh0_gOuBg2A_(initial_index)
                if items:
                    parent.append(ListElement('option_list', items))
                return gAAAAABmn4MYf0njqRPTsYiBbt6fiBQSV0TYAaDixMXvMgEhoZ8l5kmC3WL8uNy7GW8mhoSaqftINj2RmQwUyjd0bVjDUVgJXA__(source, parent, context)
            list_item = ListItemElement((current_line.line, current_line.line if content.last_line is None else content.last_line.line))
            items.append(list_item)
            context.gAAAAABmn4MYzOG10A9UBq5lMrOt2Vql9A7Kd8BJSK8nz7q8stOB0lr21cwE9IUKWXTe5jm7L_ixqKiMrgJk2Qka7ywTjGFrVw__(content, list_item)
            source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__()
        else:
            source.gAAAAABmn4MY5R3t_pLcLit5TwdxnPh1jL5so6P4ttHG3N4aRj_ydeo299Mths_w_X4mn1GdsLyVYMr10MZb4pcJrhnHd3TqKA__()
            break
    if items:
        parent.append(ListElement('option_list', items))
    return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__