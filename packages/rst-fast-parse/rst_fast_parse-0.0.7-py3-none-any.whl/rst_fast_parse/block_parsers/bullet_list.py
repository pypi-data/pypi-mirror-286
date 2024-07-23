from __future__ import annotations
import re
from rst_fast_parse.core import gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_, gAAAAABmnuojyVOa__SFl52_gl5XSUoa6WT6zDtvviRWWFizGdPPVlComyZy1vRGpEh8_otsfmmSedteHWUAmThA0ExDLAlJng__
from rst_fast_parse.elements import ElementListBase, ListElement, ListItemElement
from rst_fast_parse.regexes.block import gAAAAABmnuojHw_cBLhpC5HnThcFbZWML2VskxNGSeoCAVih5xyov_EHHcGI7L2ia3rUNbJ66yrYQf3Q45k_soXF57Jif8bQs_iRzabMAPSXHBDtTgabDMg_
from rst_fast_parse.source import gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__

def gAAAAABmnuojOCzhm3bvQlUeNv1XkKLVDcibvllTFBKrTlAwsucCM4LnE4_jeGod2x2Tyf4x_h1Ce9fMMopT_4tFfKemIjkpfhzijcSDWdr5YtXGByeAHjg_(source: gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__, parent: ElementListBase, context: gAAAAABmnuojyVOa__SFl52_gl5XSUoa6WT6zDtvviRWWFizGdPPVlComyZy1vRGpEh8_otsfmmSedteHWUAmThA0ExDLAlJng__, /) -> gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_:
    if not (first_line := source.current_line):
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuoj3aryYICdV_DRXww7_sB4t47whKoHzQbi63L259co7hXyWE0ipEj7HxYbUAe60Pyz7XEQS8izK2QkZQBfWccvGA__
    if not (match := re.match(gAAAAABmnuojHw_cBLhpC5HnThcFbZWML2VskxNGSeoCAVih5xyov_EHHcGI7L2ia3rUNbJ66yrYQf3Q45k_soXF57Jif8bQs_iRzabMAPSXHBDtTgabDMg_, first_line.content)):
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojR_bJJWp1wWXX31xmpSl2WA0iZ_2vj_rM1BM92DiLOoC4J721_7xFn9SMsRxwfsPt9SqBKEJ_kEySibY1UPR4pA__
    symbol: str = match.group(1)
    items: list[ListItemElement] = []
    while (current_line := source.current_line):
        if current_line.is_blank:
            source.gAAAAABmnuojVTLADCMhqSUy7AGOzFTv5zQO7PfrX9LR3rUNi_CB4ZCiOXdZh9_VenkdmSFTLhtSCRIzFtgq8r_N1_HDY6BEXQ__()
            continue
        if (match := re.match(gAAAAABmnuojHw_cBLhpC5HnThcFbZWML2VskxNGSeoCAVih5xyov_EHHcGI7L2ia3rUNbJ66yrYQf3Q45k_soXF57Jif8bQs_iRzabMAPSXHBDtTgabDMg_, current_line.content)):
            next_symbol: str = match.group(1)
            if next_symbol != symbol:
                source.gAAAAABmnuojFuII4OCpHZwcIp1Y0A24sqLJdbVvUiEzZecco_KkrjXr9hNj_sIm4wrObGlr4MgBd_mhW0lRDBvwBKTFizqhOg__()
                break
            first_indent = match.end(0)
            if len(current_line.content) > first_indent:
                content = source.gAAAAABmnuojpySrbzuZYeTbEo3VhgV4NCdu0GmdD4iQGou5kgHjcagNjvBWTUvijeI_CSD_kGirgiU6LWwIvH4BJcG9ljlua8ypcTHzhjAmikp085G_g18_(first_indent, always_first=True, advance=True)
            else:
                content = source.gAAAAABmnuojE0sYzkyFiqkGch85WYnsBvxpSsWEDOAyu6fnrOTGmq5i8vxuUbKHNHIbgq92u_ta1r_465lW6tMmp2ZI4EIybmsXLwScIEmasFmGdTUvFq4_(first_indent=first_indent, advance=True)
            list_item = ListItemElement((current_line.line, current_line.line if content.last_line is None else content.last_line.line))
            items.append(list_item)
            source.gAAAAABmnuojVTLADCMhqSUy7AGOzFTv5zQO7PfrX9LR3rUNi_CB4ZCiOXdZh9_VenkdmSFTLhtSCRIzFtgq8r_N1_HDY6BEXQ__()
        else:
            source.gAAAAABmnuojFuII4OCpHZwcIp1Y0A24sqLJdbVvUiEzZecco_KkrjXr9hNj_sIm4wrObGlr4MgBd_mhW0lRDBvwBKTFizqhOg__()
            break
    if items:
        parent.append(ListElement('bullet_list', items))
    return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojtU2CTonP1efvRT0U3D0L4E8tQyVcnyaVUqjd_dBklWx22oUnxvHWm2H7oC1AQawAgtG_0_w_D1HolzhKwUking__