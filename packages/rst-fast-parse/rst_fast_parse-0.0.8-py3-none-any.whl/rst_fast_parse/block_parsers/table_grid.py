from __future__ import annotations
import re
from rst_fast_parse.core import gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_, gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__
from rst_fast_parse.elements import BasicElement, ElementListBase
from rst_fast_parse.regexes.block import gAAAAABmn4MYhI_WK9Okytdn8sOGXdkGRDjCXMHydmMONsk_XoTuAPl2ovw0WRoXUhZkQzMIJm7zy6XFjotFALIpGTAOoxOxEw__
from rst_fast_parse.source import gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__, gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__

def gAAAAABmn4MYIsoclEK1tw6vXCcDurr4GCWFCs2kLsCk3zJCps_WnJIL1sffD_gtQlpLhz9HAZwNetrlKht8JSmiOEaVVKD9XafGYOVkq1H8ZsfQp5Jvc_s_(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, parent: ElementListBase, context: gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__, /) -> gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_:
    if not (_current_line := source.current_line):
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYB2L_8Y60ejnc1L494XXiqoqAT_42lUybBxCX7YZww6uV6FoEOykFSuVG3v9FT86sMgdXydoGOcNYbJGxgyJz1Q__
    if not re.match(gAAAAABmn4MYhI_WK9Okytdn8sOGXdkGRDjCXMHydmMONsk_XoTuAPl2ovw0WRoXUhZkQzMIJm7zy6XFjotFALIpGTAOoxOxEw__, _current_line.content):
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYbTItVqOC9JZOWiE_G29NIXwNcyk4sUzasjWjVQD5g8b5i3UiZp59OmXx569CfMSh_FryfS6JjGLYwlCqiq_now__
    if not (table_slice := gAAAAABmn4MYJ0OUrRojMOoEg3AMWDDN7gSRUj9_tuHkEr5YyCg2EAZFraZPc5MtHv2Q_JfxuhOVM2TSE3Eh_Gss3Mpr_Puo1_fNrDdGfdPgj968RtIT_z0_(source)):
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__
    if (first := table_slice.current_line) and (last := table_slice.last_line):
        parent.append(BasicElement('table_grid', (first.line, last.line)))
    return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__

def gAAAAABmn4MYJ0OUrRojMOoEg3AMWDDN7gSRUj9_tuHkEr5YyCg2EAZFraZPc5MtHv2Q_JfxuhOVM2TSE3Eh_Gss3Mpr_Puo1_fNrDdGfdPgj968RtIT_z0_(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__) -> None | gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__:
    original_source_index = source.current_index
    block = source.gAAAAABmn4MYN5fGTBtjkUSAK88BGCHj32eexJat8C6LIe2pvXYMPXoTllZAwHYRpp4BTBfoaXMXJA2YWPp1ccyLeYleLA4AkQ__(stop_on_indented=True, advance=True)
    if not (first_line := block.current_line):
        return None
    lines: list[gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__] = []
    for line in block.gAAAAABmn4MYtQdD5Kq_sQq6lten_TCnNCIEv_zgwsDrry6cnx1S3_yD_NmuuuUl5oZoiPko9j_juDAmF9b5yuY6T1zdwux2MQ__():
        if not (line.content.startswith('+') or line.content.startswith('|')):
            source.gAAAAABmn4MYINuiuD2MpLdUpsj0dpofZ5MDZXGL24BtQUwkF6Y3v7Qw0g_1GxmzMe83cavfzpZNHPyOnrzsaRjMJdC4OkFNp9SWHVc4zdTzlh0_gOuBg2A_(original_source_index + len(lines) - 1)
            break
        lines.append(line.rstrip())
    if not re.match(gAAAAABmn4MYhI_WK9Okytdn8sOGXdkGRDjCXMHydmMONsk_XoTuAPl2ovw0WRoXUhZkQzMIJm7zy6XFjotFALIpGTAOoxOxEw__, lines[-1].content):
        for i in range(len(lines) - 2, 1, -1):
            if re.match(gAAAAABmn4MYhI_WK9Okytdn8sOGXdkGRDjCXMHydmMONsk_XoTuAPl2ovw0WRoXUhZkQzMIJm7zy6XFjotFALIpGTAOoxOxEw__, lines[i].content):
                del lines[i + 1:]
                source.gAAAAABmn4MYINuiuD2MpLdUpsj0dpofZ5MDZXGL24BtQUwkF6Y3v7Qw0g_1GxmzMe83cavfzpZNHPyOnrzsaRjMJdC4OkFNp9SWHVc4zdTzlh0_gOuBg2A_(original_source_index + len(lines) - 2)
                break
        else:
            return None
    width = len(first_line.content.rstrip())
    for line in lines:
        if len(line.content) != width:
            return None
        if not (line.content.endswith('+') or line.content.endswith('|')):
            return None
    return gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__(lines)