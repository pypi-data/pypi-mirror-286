from __future__ import annotations
import re
from rst_fast_parse.block_parsers.fallback import gAAAAABmn4MYf0njqRPTsYiBbt6fiBQSV0TYAaDixMXvMgEhoZ8l5kmC3WL8uNy7GW8mhoSaqftINj2RmQwUyjd0bVjDUVgJXA__
from rst_fast_parse.core import gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_, gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__
from rst_fast_parse.elements import ElementListBase, TitleElement, TransitionElement
from rst_fast_parse.regexes.block import gAAAAABmn4MYC_QhVLTGQ8ghtvPvFgoHLaRdsMPAsNOLtRJRcRiZ1JLEGRvJTcf5Cj88Qn3mtss1b_hkoQmC0sSIbFdEuidjxkCL4QwsM82ByBLdOk8Gcf0_
from rst_fast_parse.source import gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__, gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__
from rst_fast_parse.utils.column_widths import gAAAAABmn4MYEeKfT3g7Tt0786gqEQVIvODiI1yMH6lkPmfc_CH6hYRwmVAXC8d7n2yQSIG2EOlMEVLO0BVMsJ_kDLNhAtE53g__

def gAAAAABmn4MYDpZTxiaE7CGI5VSv_zmHjfm_pbMEAAVICSEMMZdJ0Br40iF8yTm3osG4ZqM7GgSYBEVqFWtCu7_RUS3TXk69__zGCqE16ML0YvR_Jjik4rY_(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, parent: ElementListBase, context: gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__, /) -> gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_:
    if not (current_line := source.current_line):
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYB2L_8Y60ejnc1L494XXiqoqAT_42lUybBxCX7YZww6uV6FoEOykFSuVG3v9FT86sMgdXydoGOcNYbJGxgyJz1Q__
    if not (match := re.match(gAAAAABmn4MYC_QhVLTGQ8ghtvPvFgoHLaRdsMPAsNOLtRJRcRiZ1JLEGRvJTcf5Cj88Qn3mtss1b_hkoQmC0sSIbFdEuidjxkCL4QwsM82ByBLdOk8Gcf0_, current_line.content)):
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYbTItVqOC9JZOWiE_G29NIXwNcyk4sUzasjWjVQD5g8b5i3UiZp59OmXx569CfMSh_FryfS6JjGLYwlCqiq_now__
    marker = match.string.strip()
    marker_char = marker[0]
    marker_length = len(marker)
    min_marker_length = 4
    if not context.allow_titles:
        if marker == '::':
            return gAAAAABmn4MYf0njqRPTsYiBbt6fiBQSV0TYAaDixMXvMgEhoZ8l5kmC3WL8uNy7GW8mhoSaqftINj2RmQwUyjd0bVjDUVgJXA__(source, parent, context)
        if marker_length < min_marker_length:
            return gAAAAABmn4MYf0njqRPTsYiBbt6fiBQSV0TYAaDixMXvMgEhoZ8l5kmC3WL8uNy7GW8mhoSaqftINj2RmQwUyjd0bVjDUVgJXA__(source, parent, context)
        parent.append(gAAAAABmn4MYaCdar4YBqWP8JVaYUMZPZGw1lE5zGiI8hO4sZ5ck8pTXl7iLhECbsgxiSyWWiw6IFJcnOn4_WMyJsIl46HM2RQ__(marker_char, current_line))
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__
    next_line = source.gAAAAABmn4MYnuVsIy8PjL4QsZm7x_jIvuCslixFijnZNMDMLmL_y8yQ5R8jf2wQkfc_Kh5rwhyugQ0mYlWMW6isWf1Z5_w5bA__()
    if next_line is None or next_line.is_blank:
        if marker_length < min_marker_length:
            return gAAAAABmn4MYf0njqRPTsYiBbt6fiBQSV0TYAaDixMXvMgEhoZ8l5kmC3WL8uNy7GW8mhoSaqftINj2RmQwUyjd0bVjDUVgJXA__(source, parent, context)
        parent.append(gAAAAABmn4MYaCdar4YBqWP8JVaYUMZPZGw1lE5zGiI8hO4sZ5ck8pTXl7iLhECbsgxiSyWWiw6IFJcnOn4_WMyJsIl46HM2RQ__(marker_char, current_line))
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__
    if re.match(gAAAAABmn4MYC_QhVLTGQ8ghtvPvFgoHLaRdsMPAsNOLtRJRcRiZ1JLEGRvJTcf5Cj88Qn3mtss1b_hkoQmC0sSIbFdEuidjxkCL4QwsM82ByBLdOk8Gcf0_, next_line.content):
        if marker_length < min_marker_length:
            return gAAAAABmn4MYf0njqRPTsYiBbt6fiBQSV0TYAaDixMXvMgEhoZ8l5kmC3WL8uNy7GW8mhoSaqftINj2RmQwUyjd0bVjDUVgJXA__(source, parent, context)
        parent.append(gAAAAABmn4MYaCdar4YBqWP8JVaYUMZPZGw1lE5zGiI8hO4sZ5ck8pTXl7iLhECbsgxiSyWWiw6IFJcnOn4_WMyJsIl46HM2RQ__(marker_char, current_line))
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__
    next_next_line = source.gAAAAABmn4MYnuVsIy8PjL4QsZm7x_jIvuCslixFijnZNMDMLmL_y8yQ5R8jf2wQkfc_Kh5rwhyugQ0mYlWMW6isWf1Z5_w5bA__(2)
    if next_next_line is None:
        if marker_length < min_marker_length:
            return gAAAAABmn4MYf0njqRPTsYiBbt6fiBQSV0TYAaDixMXvMgEhoZ8l5kmC3WL8uNy7GW8mhoSaqftINj2RmQwUyjd0bVjDUVgJXA__(source, parent, context)
        parent.append(gAAAAABmn4MYaCdar4YBqWP8JVaYUMZPZGw1lE5zGiI8hO4sZ5ck8pTXl7iLhECbsgxiSyWWiw6IFJcnOn4_WMyJsIl46HM2RQ__(marker_char, current_line))
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__
    if (underline_match := re.match(gAAAAABmn4MYC_QhVLTGQ8ghtvPvFgoHLaRdsMPAsNOLtRJRcRiZ1JLEGRvJTcf5Cj88Qn3mtss1b_hkoQmC0sSIbFdEuidjxkCL4QwsM82ByBLdOk8Gcf0_, next_next_line.content)) is None:
        if marker_length < min_marker_length:
            return gAAAAABmn4MYf0njqRPTsYiBbt6fiBQSV0TYAaDixMXvMgEhoZ8l5kmC3WL8uNy7GW8mhoSaqftINj2RmQwUyjd0bVjDUVgJXA__(source, parent, context)
        parent.append(gAAAAABmn4MYaCdar4YBqWP8JVaYUMZPZGw1lE5zGiI8hO4sZ5ck8pTXl7iLhECbsgxiSyWWiw6IFJcnOn4_WMyJsIl46HM2RQ__(marker_char, current_line))
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__
    underline = underline_match.string.rstrip()
    if marker != underline:
        if marker_length < min_marker_length:
            return gAAAAABmn4MYf0njqRPTsYiBbt6fiBQSV0TYAaDixMXvMgEhoZ8l5kmC3WL8uNy7GW8mhoSaqftINj2RmQwUyjd0bVjDUVgJXA__(source, parent, context)
        parent.append(gAAAAABmn4MYaCdar4YBqWP8JVaYUMZPZGw1lE5zGiI8hO4sZ5ck8pTXl7iLhECbsgxiSyWWiw6IFJcnOn4_WMyJsIl46HM2RQ__(marker_char, current_line))
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__
    title = next_line.content.rstrip()
    if gAAAAABmn4MYEeKfT3g7Tt0786gqEQVIvODiI1yMH6lkPmfc_CH6hYRwmVAXC8d7n2yQSIG2EOlMEVLO0BVMsJ_kDLNhAtE53g__(title) > marker_length:
        if marker_length < min_marker_length:
            return gAAAAABmn4MYf0njqRPTsYiBbt6fiBQSV0TYAaDixMXvMgEhoZ8l5kmC3WL8uNy7GW8mhoSaqftINj2RmQwUyjd0bVjDUVgJXA__(source, parent, context)
    source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__(2)
    parent.append(TitleElement(True, marker[0], title, (current_line.line, next_next_line.line)))
    return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__

def gAAAAABmn4MYaCdar4YBqWP8JVaYUMZPZGw1lE5zGiI8hO4sZ5ck8pTXl7iLhECbsgxiSyWWiw6IFJcnOn4_WMyJsIl46HM2RQ__(style: str, line: gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__) -> TransitionElement:
    return TransitionElement(style, (line.line, line.line))