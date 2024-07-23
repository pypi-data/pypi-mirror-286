import re
from rst_fast_parse.core import gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_, gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__
from rst_fast_parse.elements import ElementListBase, ListElement, ListItemElement
from rst_fast_parse.regexes.block import gAAAAABmn4MYDMxc3EqOQPWrgKVndlu2TW7BiCOym_t9wmZ6ssqH0oBCq2UO6uHaGBuv7KX5z7AmJdhX40NKuM7QHtyzpKSFyQ__
from rst_fast_parse.source import gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__

def gAAAAABmn4MYdbya_P_Fnx4jHD09dyCS4iDEilPOYwOgkmIyOnJ7z9IwVslaUaEylh1iNxJaJ3EtnGHKnSqWb_YDM7__XKxZ5EYVl8K8JGQDhOwvMF4Gdqw_(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, parent: ElementListBase, _context: gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__, /) -> gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_:
    if not (_current_line := source.current_line):
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYB2L_8Y60ejnc1L494XXiqoqAT_42lUybBxCX7YZww6uV6FoEOykFSuVG3v9FT86sMgdXydoGOcNYbJGxgyJz1Q__
    if not (_ := re.match(gAAAAABmn4MYDMxc3EqOQPWrgKVndlu2TW7BiCOym_t9wmZ6ssqH0oBCq2UO6uHaGBuv7KX5z7AmJdhX40NKuM7QHtyzpKSFyQ__, _current_line.content)):
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYbTItVqOC9JZOWiE_G29NIXwNcyk4sUzasjWjVQD5g8b5i3UiZp59OmXx569CfMSh_FryfS6JjGLYwlCqiq_now__
    items: list[ListItemElement] = []
    while (current_line := source.current_line):
        if (match := re.match(gAAAAABmn4MYDMxc3EqOQPWrgKVndlu2TW7BiCOym_t9wmZ6ssqH0oBCq2UO6uHaGBuv7KX5z7AmJdhX40NKuM7QHtyzpKSFyQ__, current_line.content)):
            indent_length = match.end(0)
            content = source.gAAAAABmn4MYTNqh79EcKgIZUtho1Kao6oAD8EVSM5KD4rLEPjlwoKwyZEchGSn_5OmW27927rJos5kMsWi7KvfcXnwI6Q1nVyhmAoFv66P6LWRRR_Khesk_(first_indent=indent_length, until_blank=True, advance=True)
            list_item = ListItemElement((current_line.line, current_line.line if content.last_line is None else content.last_line.line))
            items.append(list_item)
            source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__()
        else:
            source.gAAAAABmn4MY5R3t_pLcLit5TwdxnPh1jL5so6P4ttHG3N4aRj_ydeo299Mths_w_X4mn1GdsLyVYMr10MZb4pcJrhnHd3TqKA__()
            break
    if items:
        parent.append(ListElement('line_block', items))
    return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__