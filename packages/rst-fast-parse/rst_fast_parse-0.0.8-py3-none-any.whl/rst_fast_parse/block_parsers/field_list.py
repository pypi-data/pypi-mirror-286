from __future__ import annotations
import re
from typing import Generator
from rst_fast_parse.core import gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_, gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__
from rst_fast_parse.elements import ElementListBase, ListElement, ListItemElement
from rst_fast_parse.regexes.block import gAAAAABmn4MYe1ki7OlnGa_pfQLZer1Mn_eUBQM03gM2nKbfkI6sNHIHzbOXoxu6RgA6dnIWlTJcz3mH_xu4_cljk5vNlm4L5w__
from rst_fast_parse.source import PositiveInt, gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__

def gAAAAABmn4MYjiI2PvhWBsaQCX7EurGDbkU1bvYJlwp6Fye_BS7WMq_eT_6m7e1q7ars2ozFpS8G40KSsZxHhpkyTYHUDp8Vm4hgn0tJlB2Bnhn_4SoQOyw_(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, parent: ElementListBase, context: gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__, /) -> gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_:
    if not (_current_line := source.current_line):
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYB2L_8Y60ejnc1L494XXiqoqAT_42lUybBxCX7YZww6uV6FoEOykFSuVG3v9FT86sMgdXydoGOcNYbJGxgyJz1Q__
    if not (_ := re.match(gAAAAABmn4MYe1ki7OlnGa_pfQLZer1Mn_eUBQM03gM2nKbfkI6sNHIHzbOXoxu6RgA6dnIWlTJcz3mH_xu4_cljk5vNlm4L5w__, _current_line.content)):
        return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYbTItVqOC9JZOWiE_G29NIXwNcyk4sUzasjWjVQD5g8b5i3UiZp59OmXx569CfMSh_FryfS6JjGLYwlCqiq_now__
    items: list[ListItemElement] = []
    for name, content in gAAAAABmn4MYIHIQMSzy7NVOYbIUx4sLsGKHV6_Xnj_6RQrOgwYcLqlDg7ONKoxHrj_IVmNnFWV9mAwxDAhKA9zJnWp5kAPkF2SlQfww4Ytvn2dNb2o4gCo_(source):
        if name.current_line:
            list_item = ListItemElement((name.current_line.line, name.current_line.line if content.last_line is None else content.last_line.line))
            items.append(list_item)
            context.gAAAAABmn4MYzOG10A9UBq5lMrOt2Vql9A7Kd8BJSK8nz7q8stOB0lr21cwE9IUKWXTe5jm7L_ixqKiMrgJk2Qka7ywTjGFrVw__(content, list_item)
    if items:
        parent.append(ListElement('field_list', items))
    return gAAAAABmn4MYeVQtvsR11NdZL0ImOFEuGQJ7dLCZHFF9C4DkFrBrFXccnrLONs0ENOACBViRsG6pXwhnk9VPyeEghIYL9LHL1jnmehbEXsgFTEg0JDSiJQI_.gAAAAABmn4MYiND_Iavkenr2a_ZqIdRy7wJ6zJw6M__RmpmR8yK_l7AxsIOS7h0ZkL_VjHAamiuYgENreXZ6puVFrvYx6i0I5A__

def gAAAAABmn4MYIHIQMSzy7NVOYbIUx4sLsGKHV6_Xnj_6RQrOgwYcLqlDg7ONKoxHrj_IVmNnFWV9mAwxDAhKA9zJnWp5kAPkF2SlQfww4Ytvn2dNb2o4gCo_(source: gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, /) -> Generator[tuple[gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__, gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__], None, None]:
    while (current_line := source.current_line):
        if current_line.is_blank:
            source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__()
            continue
        if (match := re.match(gAAAAABmn4MYe1ki7OlnGa_pfQLZer1Mn_eUBQM03gM2nKbfkI6sNHIHzbOXoxu6RgA6dnIWlTJcz3mH_xu4_cljk5vNlm4L5w__, current_line.content)):
            name_slice = current_line.gAAAAABmn4MYh_UzTYFzYYEALy2nWi1wJzqyt16h7JUfqZhJytjLl8BY10TO82bMXRsZcqJKimz5L212ONIc6ERjZmf6aMW5uQ__(PositiveInt(match.start(1)), PositiveInt(match.end(1))).gAAAAABmn4MYRt8yLBH4jkx6BTT_VzoUrZ_nNp9pRAL6SOkkjVw5J4CDLVrnQ8LmlSdOrYqRHSAexxkFDIPpNRB_9CuQ0W5bXw__()
            body_slice = source.gAAAAABmn4MYTNqh79EcKgIZUtho1Kao6oAD8EVSM5KD4rLEPjlwoKwyZEchGSn_5OmW27927rJos5kMsWi7KvfcXnwI6Q1nVyhmAoFv66P6LWRRR_Khesk_(first_indent=match.end(0), advance=True)
            yield (name_slice, body_slice)
            source.gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__()
        else:
            source.gAAAAABmn4MY5R3t_pLcLit5TwdxnPh1jL5so6P4ttHG3N4aRj_ydeo299Mths_w_X4mn1GdsLyVYMr10MZb4pcJrhnHd3TqKA__()
            break