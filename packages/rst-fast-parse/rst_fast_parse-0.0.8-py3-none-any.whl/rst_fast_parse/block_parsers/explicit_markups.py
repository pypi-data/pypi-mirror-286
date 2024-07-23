from __future__ import annotations
import re
from rst_fast_parse.core import gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_, gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__
from rst_fast_parse.elements import BasicElement, DirectiveElement, ElementListBase
from rst_fast_parse.regexes.block import gAAAAABmn4MYzrqgjWV6q5ZPmKVLVMg9ipe0uySnXKqC__3MZmD0mHNkVdK77OkMwCDDTTncDhpppZbvA5uP8_ORJrofI3ddYg__, gAAAAABmn4MYCVgq6fG6mh7n4Ym9Ozt_3dJcQOszSAIuxo768J0FUBN3jwk_Ri9_RJAoT_cV14l84bqMtCBgnfukzv4ZBEEHK1yST13mfEufkFQZvdBlBtM_, gAAAAABmn4MYWcn4ZWYWhwVAnYSAKBLhWPSwpi5SmELEPQ_fWiGZnb1gWFUa7aMsocSsrq8pEoRU3pwY0RGY01K4rYBRaLv0W9cX5pTZ6PMpAj0Bz9y65_c_, gAAAAABmn4MYfTqlK5ZkaUk_5_vBDwoJPgK4iNT3PAtqZcm_HetEcbTBDT4jYE9tBEMycyRvSXW0eNvAur3ZiqPiLOsautwjdxFGHga_kyVBU05xgw81Qgs_, gAAAAABmn4MY89Ts_G3DPybrQjBpWIYvxULuva1oO63F__yhL91ar6RMyWFeY11rHXumDlO5Gfqm3VQNj4m7iGxiLD_wlEok8FTJ7UH0uzGvboy74FJaPOA_, gAAAAABmn4MY_GPUhwWBH4CKVE_cL2FP9pbN7HBEgmMrh585Yej6JpZgzLWfOj375fGXEODkhs0UugOKHG9r9e8q5C26009_Lbfm7fUhWpLSFJBLKFk3pvU_
from rst_fast_parse.source import PositiveInt, gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__

def gAAAAABmn4MYGTbQJXby_cFntbJEBcvGkYOPU542DNwL0IIQvUJNiTuAIa1XvWQn2dxnDzKNlc8bvd1hEOG_I3nWNz_VT0_whUCEfmZ9W_lSSNOR4IF9LG0_(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, parent: ElementListBase, context: gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__, /) -> gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_:
    if not (current_line := source.current_line):
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYB2L_8Y60ejnc1L494XXiqoqAT_42lUybBxCX7YZww6uV6FoEOykFSuVG3v9FT86sMgdXydoGOcNYbJGxgyJz1Q__
    if not (init_match := re.match(gAAAAABmn4MYzrqgjWV6q5ZPmKVLVMg9ipe0uySnXKqC__3MZmD0mHNkVdK77OkMwCDDTTncDhpppZbvA5uP8_ORJrofI3ddYg__, current_line.content)):
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYbTItVqOC9JZOWiE_G29NIXwNcyk4sUzasjWjVQD5g8b5i3UiZp59OmXx569CfMSh_FryfS6JjGLYwlCqiq_now__
    if (match := re.match(gAAAAABmn4MYfTqlK5ZkaUk_5_vBDwoJPgK4iNT3PAtqZcm_HetEcbTBDT4jYE9tBEMycyRvSXW0eNvAur3ZiqPiLOsautwjdxFGHga_kyVBU05xgw81Qgs_, current_line.content)):
        gAAAAABmn4MY0dupuFrIogwb53gdd14qk8mTeF16SpfgSvPT0ev4KLIUe9Dd_pd30VAs4eTi0Twx5TBubpUSLJBdXIuT8vh37g__(source, parent, context, match)
    elif (match := re.match(gAAAAABmn4MYCVgq6fG6mh7n4Ym9Ozt_3dJcQOszSAIuxo768J0FUBN3jwk_Ri9_RJAoT_cV14l84bqMtCBgnfukzv4ZBEEHK1yST13mfEufkFQZvdBlBtM_, current_line.content)):
        gAAAAABmn4MYi8VmM51gB5ah1E942MioGNU7Qe7EH7uJjKMa7a7t_oGQpMy3_DB25PENjaxOUI_Zc_93qpx3dUwPXmZ_VMsaoQ__(source, parent, context, match)
    elif (match := re.match(gAAAAABmn4MY_GPUhwWBH4CKVE_cL2FP9pbN7HBEgmMrh585Yej6JpZgzLWfOj375fGXEODkhs0UugOKHG9r9e8q5C26009_Lbfm7fUhWpLSFJBLKFk3pvU_, current_line.content)):
        gAAAAABmn4MYRQLS2fbqkrtIv7oMw27oriLxLRidF8zu7OJLVBpILKc0_jdSvAUSh4V4iLMw8ILa4Q_tJxAB8upwgACNbQpBTyaFw6Wikj_eq4IEDF0YNlc_(source, parent, context, match)
    elif (match := re.match(gAAAAABmn4MY89Ts_G3DPybrQjBpWIYvxULuva1oO63F__yhL91ar6RMyWFeY11rHXumDlO5Gfqm3VQNj4m7iGxiLD_wlEok8FTJ7UH0uzGvboy74FJaPOA_, current_line.content)):
        gAAAAABmn4MYZv6hpvyjq3Bafpmma6BXpk3VJzrgf_kq_00G2apQZ5tZBDJUTyaR7P_xfrwXcyuyXYIVCEjF4moz9D7LN_kNgrL77HE8yOoKKSXtnzc27ws_(source, parent, context, match)
    elif (match := re.match(gAAAAABmn4MYWcn4ZWYWhwVAnYSAKBLhWPSwpi5SmELEPQ_fWiGZnb1gWFUa7aMsocSsrq8pEoRU3pwY0RGY01K4rYBRaLv0W9cX5pTZ6PMpAj0Bz9y65_c_, current_line.content)):
        gAAAAABmn4MYdkgtnGylhfhwJmYCeW8jUrFneP8E8hUORlveDU2Uco5uvDbf_WoQo_RuXBA132CGAJNPK54NbjgqCK6oT2JPRw__(source, parent, context, match)
    else:
        gAAAAABmn4MY2_nKzr8esdNYNy9C7fgG0iENSXO_1cePoCRuGx3KBHwLXgwCdKwVvNBx6SkG9tuOHv826BKjjwR9dvSGCrxv0A__(source, parent, context, init_match.end(0))
    return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__

def gAAAAABmn4MY0dupuFrIogwb53gdd14qk8mTeF16SpfgSvPT0ev4KLIUe9Dd_pd30VAs4eTi0Twx5TBubpUSLJBdXIuT8vh37g__(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, parent: ElementListBase, context: gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__, match: re.Match[str]) -> None:
    first = source.current_line
    slice = source.gAAAAABmn4MYTNqh79EcKgIZUtho1Kao6oAD8EVSM5KD4rLEPjlwoKwyZEchGSn_5OmW27927rJos5kMsWi7KvfcXnwI6Q1nVyhmAoFv66P6LWRRR_Khesk_(first_indent=match.end(0), advance=True)
    last = slice.last_line if slice.last_line is not None else source.current_line
    if first and last:
        parent.append(BasicElement('footnote', (first.line, last.line)))

def gAAAAABmn4MYi8VmM51gB5ah1E942MioGNU7Qe7EH7uJjKMa7a7t_oGQpMy3_DB25PENjaxOUI_Zc_93qpx3dUwPXmZ_VMsaoQ__(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, parent: ElementListBase, context: gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__, match: re.Match[str]) -> None:
    first = source.current_line
    slice = source.gAAAAABmn4MYTNqh79EcKgIZUtho1Kao6oAD8EVSM5KD4rLEPjlwoKwyZEchGSn_5OmW27927rJos5kMsWi7KvfcXnwI6Q1nVyhmAoFv66P6LWRRR_Khesk_(first_indent=match.end(0), advance=True)
    last = slice.last_line if slice.last_line is not None else source.current_line
    if first and last:
        parent.append(BasicElement('citation', (first.line, last.line)))

def gAAAAABmn4MYRQLS2fbqkrtIv7oMw27oriLxLRidF8zu7OJLVBpILKc0_jdSvAUSh4V4iLMw8ILa4Q_tJxAB8upwgACNbQpBTyaFw6Wikj_eq4IEDF0YNlc_(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, parent: ElementListBase, context: gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__, match: re.Match[str]) -> None:
    first = source.current_line
    slice = source.gAAAAABmn4MYTNqh79EcKgIZUtho1Kao6oAD8EVSM5KD4rLEPjlwoKwyZEchGSn_5OmW27927rJos5kMsWi7KvfcXnwI6Q1nVyhmAoFv66P6LWRRR_Khesk_(first_indent=match.end(0), until_blank=True, advance=True, strip_indent=False)
    last = slice.last_line if slice.last_line is not None else source.current_line
    if first and last:
        parent.append(BasicElement('link_target', (first.line, last.line)))

def gAAAAABmn4MYZv6hpvyjq3Bafpmma6BXpk3VJzrgf_kq_00G2apQZ5tZBDJUTyaR7P_xfrwXcyuyXYIVCEjF4moz9D7LN_kNgrL77HE8yOoKKSXtnzc27ws_(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, parent: ElementListBase, context: gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__, match: re.Match[str]) -> None:
    first = source.current_line
    slice = source.gAAAAABmn4MYTNqh79EcKgIZUtho1Kao6oAD8EVSM5KD4rLEPjlwoKwyZEchGSn_5OmW27927rJos5kMsWi7KvfcXnwI6Q1nVyhmAoFv66P6LWRRR_Khesk_(first_indent=match.end(0), strip_indent=False, advance=True)
    last = slice.last_line if slice.last_line is not None else source.current_line
    if first and last:
        parent.append(BasicElement('substitution_def', (first.line, last.line)))

def gAAAAABmn4MYdkgtnGylhfhwJmYCeW8jUrFneP8E8hUORlveDU2Uco5uvDbf_WoQo_RuXBA132CGAJNPK54NbjgqCK6oT2JPRw__(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, parent: ElementListBase, context: gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__, match: re.Match[str]) -> None:
    first = source.current_line
    slice = source.gAAAAABmn4MYTNqh79EcKgIZUtho1Kao6oAD8EVSM5KD4rLEPjlwoKwyZEchGSn_5OmW27927rJos5kMsWi7KvfcXnwI6Q1nVyhmAoFv66P6LWRRR_Khesk_(first_indent=match.end(0), strip_top=False, advance=True)
    last = slice.last_line if slice.last_line is not None else source.current_line
    if first and last:
        parent.append(DirectiveElement(match.group(1), (first.line, last.line)))

def gAAAAABmn4MY2_nKzr8esdNYNy9C7fgG0iENSXO_1cePoCRuGx3KBHwLXgwCdKwVvNBx6SkG9tuOHv826BKjjwR9dvSGCrxv0A__(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, parent: ElementListBase, _: gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__, first_indent: int) -> None:
    if not source.current_line:
        return
    first = source.current_line
    if (next_line := source.gAAAAABmn4MYnuVsIy8PjL4QsZm7x_jIvuCslixFijnZNMDMLmL_y8yQ5R8jf2wQkfc_Kh5rwhyugQ0mYlWMW6isWf1Z5_w5bA__(1)) is not None and next_line.is_blank:
        first_indent = PositiveInt(first_indent)
        if source.current_line.gAAAAABmn4MYh_UzTYFzYYEALy2nWi1wJzqyt16h7JUfqZhJytjLl8BY10TO82bMXRsZcqJKimz5L212ONIc6ERjZmf6aMW5uQ__(first_indent).is_blank:
            parent.append(BasicElement('comment', (first.line, first.line)))
            return
    slice = source.gAAAAABmn4MYTNqh79EcKgIZUtho1Kao6oAD8EVSM5KD4rLEPjlwoKwyZEchGSn_5OmW27927rJos5kMsWi7KvfcXnwI6Q1nVyhmAoFv66P6LWRRR_Khesk_(first_indent=first_indent, strip_bottom=True, advance=True)
    if (last := slice.last_line):
        parent.append(BasicElement('comment', (first.line, last.line)))