from __future__ import annotations
import re
from rst_fast_parse.core import gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_, gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__
from rst_fast_parse.elements import BasicElement, ElementListBase
from rst_fast_parse.regexes.block import gAAAAABmn4MYJ_EfUz79Z_l9_175bE2B0ECZxWcJ7n_2gyYRFEVIVNiYLC745VbvFdQ3kvJuQ3cTlhes_c_swlmgg_vG_xjyeQ__, gAAAAABmn4MYJnUwKScUXNZ1Zi2yfMiGvOAW_csKnlqDEeFG9ld8drDogoFvv8pgE1zotgUsPwXDFjH9OUZNbv4_LTVII1WLP5J_2hn_q9ZrqZBGR6US_W4_
from rst_fast_parse.source import gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__

def gAAAAABmn4MYDm4BxCIDWeMRPQaYzJJWpTkJu_JRL5jGS3hC1goT0Vm5NLzm7TCHLVrLpC8QXs0WQCc4Gb0jxtBKE2n_9M0_kbAb_b99yECr0DgacWDl2ps_(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, parent: ElementListBase, context: gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__, /) -> gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_:
    if not (_current_line := source.current_line):
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYB2L_8Y60ejnc1L494XXiqoqAT_42lUybBxCX7YZww6uV6FoEOykFSuVG3v9FT86sMgdXydoGOcNYbJGxgyJz1Q__
    if not re.match(gAAAAABmn4MYJ_EfUz79Z_l9_175bE2B0ECZxWcJ7n_2gyYRFEVIVNiYLC745VbvFdQ3kvJuQ3cTlhes_c_swlmgg_vG_xjyeQ__, _current_line.content):
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYbTItVqOC9JZOWiE_G29NIXwNcyk4sUzasjWjVQD5g8b5i3UiZp59OmXx569CfMSh_FryfS6JjGLYwlCqiq_now__
    if not (table_slice := gAAAAABmn4MYymEFNSa5BmFYRxORWomqyl_SaXZzuXrvWVFVv_w4fXkzYSaNpBrLnGIFz7fhCX5Np1DcWUXtRKs8Fxv6NgdQzV5k0AHOX6Tllweo9rO2m5k_(source)):
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__
    if (first := table_slice.current_line) and (last := table_slice.last_line):
        parent.append(BasicElement('table_simple', (first.line, last.line)))
    return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__

def gAAAAABmn4MYymEFNSa5BmFYRxORWomqyl_SaXZzuXrvWVFVv_w4fXkzYSaNpBrLnGIFz7fhCX5Np1DcWUXtRKs8Fxv6NgdQzV5k0AHOX6Tllweo9rO2m5k_(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__) -> None | gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__:
    if not (first_line := source.current_line):
        return None
    toplen = len(first_line.content.strip())
    borders_found: int = 0
    peek_offset = 1
    last_border_offset: None | int = None
    while (line := source.gAAAAABmn4MYnuVsIy8PjL4QsZm7x_jIvuCslixFijnZNMDMLmL_y8yQ5R8jf2wQkfc_Kh5rwhyugQ0mYlWMW6isWf1Z5_w5bA__(peek_offset)):
        if re.match(gAAAAABmn4MYJnUwKScUXNZ1Zi2yfMiGvOAW_csKnlqDEeFG9ld8drDogoFvv8pgE1zotgUsPwXDFjH9OUZNbv4_LTVII1WLP5J_2hn_q9ZrqZBGR6US_W4_, line.content):
            if len(line.content.strip()) != toplen:
                source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__(peek_offset)
                return None
            borders_found += 1
            last_border_offset = peek_offset
            if borders_found == 2 or not (next_line := source.gAAAAABmn4MYnuVsIy8PjL4QsZm7x_jIvuCslixFijnZNMDMLmL_y8yQ5R8jf2wQkfc_Kh5rwhyugQ0mYlWMW6isWf1Z5_w5bA__(peek_offset + 1)) or next_line.is_blank:
                break
        peek_offset += 1
    else:
        if last_border_offset is not None:
            source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__(last_border_offset)
        else:
            source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__(peek_offset)
        return None
    table_slice = source.gAAAAABmn4MYBPO5vpw99hwEDQsrFFm0nxHCAF1XBNo4m9p69ycMltQ3kbBqJoCj7klxeeRRQu7XULiTM2cHkLzE_hqQ3qH7GA__(0, peek_offset + 1)
    source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__(peek_offset)
    return table_slice