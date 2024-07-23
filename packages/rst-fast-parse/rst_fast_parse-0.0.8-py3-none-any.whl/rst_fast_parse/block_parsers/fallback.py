from __future__ import annotations
import re
from rst_fast_parse.core import gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_, gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__
from rst_fast_parse.elements import BasicElement, ElementListBase, ListElement, ListItemElement, TitleElement
from rst_fast_parse.regexes.block import gAAAAABmn4MY5lbLiSs8y3JYDWnKGJjN7yBM2XsuvFMIRV0g5PYDi4FZwWAQXfNtMHsk9xhhnpqllxbs_51t_XEEDsJBB5riaMa78Y634X7dmZet25M8aZM_, gAAAAABmn4MYCW8ldmP0Lm6PF2ndF2Y4DTvOTJmgRvDxtTTeHo7k_BoGCFIqRanw5ZpiJV2m4tOdMzSUG11bCXhqXYLw1Da1p17K2GMkNisSgFlQUOPU2RU_, gAAAAABmn4MY2xt9YAU0GdZbvz5vKFSMu53NGN9ICvaETNxp1HGtWVrDotaei31WSMmEPNrnrP3_tKAWyt8MxaOydJz3dmXlsw__, gAAAAABmn4MYBMc0uHqTLFJUNYDldzhhFyuvcWSzeh00D4IT6R8wW5z6f4kbUoriYAnITv1B1RbdsWvml_EazwEiYPd1AvgzGA__, gAAAAABmn4MYzrqgjWV6q5ZPmKVLVMg9ipe0uySnXKqC__3MZmD0mHNkVdK77OkMwCDDTTncDhpppZbvA5uP8_ORJrofI3ddYg__, gAAAAABmn4MYe1ki7OlnGa_pfQLZer1Mn_eUBQM03gM2nKbfkI6sNHIHzbOXoxu6RgA6dnIWlTJcz3mH_xu4_cljk5vNlm4L5w__, gAAAAABmn4MYDMxc3EqOQPWrgKVndlu2TW7BiCOym_t9wmZ6ssqH0oBCq2UO6uHaGBuv7KX5z7AmJdhX40NKuM7QHtyzpKSFyQ__, gAAAAABmn4MY_3hPtFWIo0drAvqlufm_DwsbCe7aFfIy_huqiY_r7q4jOfddPwOhKfRfgwfhqEDG4oHmVZi5aJowtdGLbYPF4klNK_fAxKAoalpMWx_u4XY_, gAAAAABmn4MYP_YzlYIRxlrQIxIx8SyTrWKTYJt4_QtNPgitW7CIwxRYd_YzVdSvqRDzRRbEOi6nCS9t9vcA2J_rr_Z5XcplSITGHO0kSRzptBN_w5NlCs8_, gAAAAABmn4MYKB_xBfM_jQaYUagdl207K_YFinV9u6cpSMtPJBxRSsv8pmqaL7EerswEotiytXd54usQxwKYbisEiQ6G9cQABZBCuWsovj2MUf3y_5axbOw_, gAAAAABmn4MYC_QhVLTGQ8ghtvPvFgoHLaRdsMPAsNOLtRJRcRiZ1JLEGRvJTcf5Cj88Qn3mtss1b_hkoQmC0sSIbFdEuidjxkCL4QwsM82ByBLdOk8Gcf0_, gAAAAABmn4MYhI_WK9Okytdn8sOGXdkGRDjCXMHydmMONsk_XoTuAPl2ovw0WRoXUhZkQzMIJm7zy6XFjotFALIpGTAOoxOxEw__, gAAAAABmn4MYJ_EfUz79Z_l9_175bE2B0ECZxWcJ7n_2gyYRFEVIVNiYLC745VbvFdQ3kvJuQ3cTlhes_c_swlmgg_vG_xjyeQ__
from rst_fast_parse.source import gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__, gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__
from rst_fast_parse.utils.column_widths import gAAAAABmn4MYEeKfT3g7Tt0786gqEQVIvODiI1yMH6lkPmfc_CH6hYRwmVAXC8d7n2yQSIG2EOlMEVLO0BVMsJ_kDLNhAtE53g__

def gAAAAABmn4MYf0njqRPTsYiBbt6fiBQSV0TYAaDixMXvMgEhoZ8l5kmC3WL8uNy7GW8mhoSaqftINj2RmQwUyjd0bVjDUVgJXA__(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, parent: ElementListBase, context: gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__, /) -> gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_:
    if not (current_line := source.current_line):
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYB2L_8Y60ejnc1L494XXiqoqAT_42lUybBxCX7YZww6uV6FoEOykFSuVG3v9FT86sMgdXydoGOcNYbJGxgyJz1Q__
    next_line = source.gAAAAABmn4MYnuVsIy8PjL4QsZm7x_jIvuCslixFijnZNMDMLmL_y8yQ5R8jf2wQkfc_Kh5rwhyugQ0mYlWMW6isWf1Z5_w5bA__()
    if next_line is None or next_line.is_blank:
        gAAAAABmn4MY7Hp15oOlA_nnYJeJwUqolrLJgfqXaJyRqzEYSFtjxvtP2CapGKgxCO3VuuOeKE0TuxoQQQGjgHlFOW8COjw8_bgq6fDaU_EGQ4Mk6zVmSjY_(current_line, source, parent, context)
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__
    if next_line.content and next_line.content[0] == ' ':
        gAAAAABmn4MYm9_DQQJzk2EMBX4jIZ5uwXqpcYR12_lXfR5k_hx4QcMBV6biX_dMGgxFQFSpq7tA0lMbbnv0xvipb0_HDrwQjxr9OVDTUbDed6iuQEr32c4_(source, parent, context)
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__
    min_marker_length = 4
    if re.match(gAAAAABmn4MYC_QhVLTGQ8ghtvPvFgoHLaRdsMPAsNOLtRJRcRiZ1JLEGRvJTcf5Cj88Qn3mtss1b_hkoQmC0sSIbFdEuidjxkCL4QwsM82ByBLdOk8Gcf0_, next_line.content):
        title = current_line.content.rstrip()
        underline = next_line.content.rstrip()
        if gAAAAABmn4MYEeKfT3g7Tt0786gqEQVIvODiI1yMH6lkPmfc_CH6hYRwmVAXC8d7n2yQSIG2EOlMEVLO0BVMsJ_kDLNhAtE53g__(title) > len(underline):
            if len(underline) < min_marker_length:
                gAAAAABmn4MYZhtJK_NOLpsGSmDLtqJMlDbE3NSF2nOm4Lw9GRgOK_b7a3GFtgWsev0Xwvsawvcnk_Zz6dYgBPtXVLkw0VA12tfaBn7MNRSQrFtPtRdzSkA_(source, parent, context)
                return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__
        if not context.allow_titles:
            source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__()
            return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__
        source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__()
        parent.append(TitleElement(False, underline[0], title, (current_line.line, next_line.line)))
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__
    gAAAAABmn4MYZhtJK_NOLpsGSmDLtqJMlDbE3NSF2nOm4Lw9GRgOK_b7a3GFtgWsev0Xwvsawvcnk_Zz6dYgBPtXVLkw0VA12tfaBn7MNRSQrFtPtRdzSkA_(source, parent, context)
    return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__

def gAAAAABmn4MY7Hp15oOlA_nnYJeJwUqolrLJgfqXaJyRqzEYSFtjxvtP2CapGKgxCO3VuuOeKE0TuxoQQQGjgHlFOW8COjw8_bgq6fDaU_EGQ4Mk6zVmSjY_(current_line: gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__, source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, parent: ElementListBase, context: gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__, /) -> None:
    paragraph_line = current_line.rstrip()
    literal_block_next = re.search(gAAAAABmn4MY_3hPtFWIo0drAvqlufm_DwsbCe7aFfIy_huqiY_r7q4jOfddPwOhKfRfgwfhqEDG4oHmVZi5aJowtdGLbYPF4klNK_fAxKAoalpMWx_u4XY_, paragraph_line.content)
    parent.append(BasicElement('paragraph', (paragraph_line.line, paragraph_line.line)))
    if literal_block_next:
        gAAAAABmn4MYIxtXQobq8lxiEYJOIO5JM_id2j5sl2QbpZyEUjwcz3emDsUWd_xCU_GU2BWTFf82lyvffgXJjVF3b8jo2JlNjA__(source, parent, context)

def gAAAAABmn4MYZhtJK_NOLpsGSmDLtqJMlDbE3NSF2nOm4Lw9GRgOK_b7a3GFtgWsev0Xwvsawvcnk_Zz6dYgBPtXVLkw0VA12tfaBn7MNRSQrFtPtRdzSkA_(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, parent: ElementListBase, context: gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__, /) -> None:
    if (_current_line := source.current_line) is None:
        return None
    text_slice = source.gAAAAABmn4MYN5fGTBtjkUSAK88BGCHj32eexJat8C6LIe2pvXYMPXoTllZAwHYRpp4BTBfoaXMXJA2YWPp1ccyLeYleLA4AkQ__(stop_on_indented=True, advance=True)
    text_content = text_slice.gAAAAABmn4MYX16pqDitorWR8Tz1Q6cSgqYSppnPIItwkJTZxUhhW0mHgM3ad9ZMW1_KdiUg84Tp6EMD2j25XLY_NM4VXHsYAw__().rstrip()
    literal_block_next = re.search(gAAAAABmn4MY_3hPtFWIo0drAvqlufm_DwsbCe7aFfIy_huqiY_r7q4jOfddPwOhKfRfgwfhqEDG4oHmVZi5aJowtdGLbYPF4klNK_fAxKAoalpMWx_u4XY_, text_content)
    if (first := text_slice.current_line) and (last := text_slice.last_line):
        parent.append(BasicElement('paragraph', (first.line, last.line)))
    if literal_block_next:
        gAAAAABmn4MYIxtXQobq8lxiEYJOIO5JM_id2j5sl2QbpZyEUjwcz3emDsUWd_xCU_GU2BWTFf82lyvffgXJjVF3b8jo2JlNjA__(source, parent, context)
    return None

def gAAAAABmn4MYIxtXQobq8lxiEYJOIO5JM_id2j5sl2QbpZyEUjwcz3emDsUWd_xCU_GU2BWTFf82lyvffgXJjVF3b8jo2JlNjA__(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, parent: ElementListBase, context: gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__, /) -> None:
    original_index = source.current_index
    source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__()
    block_slice = source.gAAAAABmn4MY_yfqwBsRYQF3i6B4ejtA8c7PHNAe7ywGMgPEB1VSuXCI5XaNxcmX8C908AIn05EG2lE2SBQZbHS1EvFCVvXtNQ__(advance=True).gAAAAABmn4MYjOcyJS7Ldn32tRtXR6IwmXjGm_DVJ3LT5jhCkFGwbf9xT2HhZK978cjTJze42Q6ELwdxT4_4rHcg0jyLd5Q1lIvDIIlrRy1ZNwYs8Pzk_eQ_()
    if not block_slice.gAAAAABmn4MYOhdG3jdRtEl14WPRZCpCcMmJQpcmnswQsDsgyhnIlaFBEVJjImyefVR2nmNCYNl9kCrvNqXt1MlEf6S9iUHGag__():
        source.gAAAAABmn4MYINuiuD2MpLdUpsj0dpofZ5MDZXGL24BtQUwkF6Y3v7Qw0g_1GxmzMe83cavfzpZNHPyOnrzsaRjMJdC4OkFNp9SWHVc4zdTzlh0_gOuBg2A_(original_index)
        peek_index = 2
        while (next_line := source.gAAAAABmn4MYnuVsIy8PjL4QsZm7x_jIvuCslixFijnZNMDMLmL_y8yQ5R8jf2wQkfc_Kh5rwhyugQ0mYlWMW6isWf1Z5_w5bA__(peek_index)) and next_line.is_blank:
            peek_index += 1
        if (next_line := source.gAAAAABmn4MYnuVsIy8PjL4QsZm7x_jIvuCslixFijnZNMDMLmL_y8yQ5R8jf2wQkfc_Kh5rwhyugQ0mYlWMW6isWf1Z5_w5bA__(peek_index)) and re.match(gAAAAABmn4MYKB_xBfM_jQaYUagdl207K_YFinV9u6cpSMtPJBxRSsv8pmqaL7EerswEotiytXd54usQxwKYbisEiQ6G9cQABZBCuWsovj2MUf3y_5axbOw_, next_line.content):
            quote_char = next_line.content[0]
            source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__(peek_index - 1)
            lines = []
            while (next_line := source.gAAAAABmn4MYnuVsIy8PjL4QsZm7x_jIvuCslixFijnZNMDMLmL_y8yQ5R8jf2wQkfc_Kh5rwhyugQ0mYlWMW6isWf1Z5_w5bA__(1)) and next_line.content and (next_line.content[0] == quote_char):
                lines.append(next_line)
                source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__()
            block_slice = gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__(lines)
        else:
            return None
    if (first := block_slice.current_line) and (last := block_slice.last_line):
        parent.append(BasicElement('literal_block', (first.line, last.line)))

def gAAAAABmn4MYm9_DQQJzk2EMBX4jIZ5uwXqpcYR12_lXfR5k_hx4QcMBV6biX_dMGgxFQFSpq7tA0lMbbnv0xvipb0_HDrwQjxr9OVDTUbDed6iuQEr32c4_(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, parent: ElementListBase, context: gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__, /) -> None:
    items: list[ListItemElement] = []
    while (first_line := source.current_line):
        if items:
            if first_line.is_blank:
                source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__()
                continue
            if first_line.content[0] == ' ' or any((re.match(regex, first_line.content) for regex in (gAAAAABmn4MYCW8ldmP0Lm6PF2ndF2Y4DTvOTJmgRvDxtTTeHo7k_BoGCFIqRanw5ZpiJV2m4tOdMzSUG11bCXhqXYLw1Da1p17K2GMkNisSgFlQUOPU2RU_, gAAAAABmn4MYBMc0uHqTLFJUNYDldzhhFyuvcWSzeh00D4IT6R8wW5z6f4kbUoriYAnITv1B1RbdsWvml_EazwEiYPd1AvgzGA__, gAAAAABmn4MYe1ki7OlnGa_pfQLZer1Mn_eUBQM03gM2nKbfkI6sNHIHzbOXoxu6RgA6dnIWlTJcz3mH_xu4_cljk5vNlm4L5w__, gAAAAABmn4MYP_YzlYIRxlrQIxIx8SyTrWKTYJt4_QtNPgitW7CIwxRYd_YzVdSvqRDzRRbEOi6nCS9t9vcA2J_rr_Z5XcplSITGHO0kSRzptBN_w5NlCs8_, gAAAAABmn4MY2xt9YAU0GdZbvz5vKFSMu53NGN9ICvaETNxp1HGtWVrDotaei31WSMmEPNrnrP3_tKAWyt8MxaOydJz3dmXlsw__, gAAAAABmn4MYDMxc3EqOQPWrgKVndlu2TW7BiCOym_t9wmZ6ssqH0oBCq2UO6uHaGBuv7KX5z7AmJdhX40NKuM7QHtyzpKSFyQ__, gAAAAABmn4MYhI_WK9Okytdn8sOGXdkGRDjCXMHydmMONsk_XoTuAPl2ovw0WRoXUhZkQzMIJm7zy6XFjotFALIpGTAOoxOxEw__, gAAAAABmn4MYJ_EfUz79Z_l9_175bE2B0ECZxWcJ7n_2gyYRFEVIVNiYLC745VbvFdQ3kvJuQ3cTlhes_c_swlmgg_vG_xjyeQ__, gAAAAABmn4MYzrqgjWV6q5ZPmKVLVMg9ipe0uySnXKqC__3MZmD0mHNkVdK77OkMwCDDTTncDhpppZbvA5uP8_ORJrofI3ddYg__, gAAAAABmn4MY5lbLiSs8y3JYDWnKGJjN7yBM2XsuvFMIRV0g5PYDi4FZwWAQXfNtMHsk9xhhnpqllxbs_51t_XEEDsJBB5riaMa78Y634X7dmZet25M8aZM_, gAAAAABmn4MYC_QhVLTGQ8ghtvPvFgoHLaRdsMPAsNOLtRJRcRiZ1JLEGRvJTcf5Cj88Qn3mtss1b_hkoQmC0sSIbFdEuidjxkCL4QwsM82ByBLdOk8Gcf0_))):
                source.gAAAAABmn4MY5R3t_pLcLit5TwdxnPh1jL5so6P4ttHG3N4aRj_ydeo299Mths_w_X4mn1GdsLyVYMr10MZb4pcJrhnHd3TqKA__()
                break
        if (next_line := source.gAAAAABmn4MYnuVsIy8PjL4QsZm7x_jIvuCslixFijnZNMDMLmL_y8yQ5R8jf2wQkfc_Kh5rwhyugQ0mYlWMW6isWf1Z5_w5bA__()):
            if next_line.content and next_line.content[0] == ' ':
                source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__()
            else:
                source.gAAAAABmn4MY5R3t_pLcLit5TwdxnPh1jL5so6P4ttHG3N4aRj_ydeo299Mths_w_X4mn1GdsLyVYMr10MZb4pcJrhnHd3TqKA__()
                break
        else:
            source.gAAAAABmn4MY5R3t_pLcLit5TwdxnPh1jL5so6P4ttHG3N4aRj_ydeo299Mths_w_X4mn1GdsLyVYMr10MZb4pcJrhnHd3TqKA__()
            break
        definition = first_line
        description = source.gAAAAABmn4MY_yfqwBsRYQF3i6B4ejtA8c7PHNAe7ywGMgPEB1VSuXCI5XaNxcmX8C908AIn05EG2lE2SBQZbHS1EvFCVvXtNQ__(advance=True)
        list_item = ListItemElement((definition.line, definition.line if description.last_line is None else description.last_line.line))
        items.append(list_item)
        context.gAAAAABmn4MYzOG10A9UBq5lMrOt2Vql9A7Kd8BJSK8nz7q8stOB0lr21cwE9IUKWXTe5jm7L_ixqKiMrgJk2Qka7ywTjGFrVw__(description, list_item)
        source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__()
    if items:
        parent.append(ListElement('definition_list', items))