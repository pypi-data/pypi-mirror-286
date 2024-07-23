from __future__ import annotations
import re
from rst_fast_parse.block_parsers.fallback import gAAAAABmnuoj8FW_yIR36aw3_5w8roKVpC8A_3_0_jEoD4_5eML7rL_Y6wSawucvxm0ovQuJFuo4SS8XTHYxtthCUXAjhnWNOw__
from rst_fast_parse.core import gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_, gAAAAABmnuojyVOa__SFl52_gl5XSUoa6WT6zDtvviRWWFizGdPPVlComyZy1vRGpEh8_otsfmmSedteHWUAmThA0ExDLAlJng__
from rst_fast_parse.elements import ElementListBase, ListElement, ListItemElement
from rst_fast_parse.regexes.block import gAAAAABmnuojb8uamMCrsWhw6F060_kIMUf9y4FMx2gF1j9VER_EqxL9epKZJhMv5rncTRjpgZ10WtZRwKtMTVUSSZNlSS1Sk2GQYpsDM_oAkUG7HZEhYl4_
from rst_fast_parse.source import gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__

def gAAAAABmnuoj_evKoVHkM1ZSVJWOZ2vx0MBLmb4x0vgm1AOJzYHGXcjRYd__Rcpu9yRyqXkJ19JpTlJaVD841qdWcepK1FDKj7OLDNIZbQopHEcSkETkxeg_(source: gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__, parent: ElementListBase, context: gAAAAABmnuojyVOa__SFl52_gl5XSUoa6WT6zDtvviRWWFizGdPPVlComyZy1vRGpEh8_otsfmmSedteHWUAmThA0ExDLAlJng__, /) -> gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_:
    if not (_current_line := source.current_line):
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuoj3aryYICdV_DRXww7_sB4t47whKoHzQbi63L259co7hXyWE0ipEj7HxYbUAe60Pyz7XEQS8izK2QkZQBfWccvGA__
    if not (_ := re.match(gAAAAABmnuojb8uamMCrsWhw6F060_kIMUf9y4FMx2gF1j9VER_EqxL9epKZJhMv5rncTRjpgZ10WtZRwKtMTVUSSZNlSS1Sk2GQYpsDM_oAkUG7HZEhYl4_, _current_line.content)):
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojR_bJJWp1wWXX31xmpSl2WA0iZ_2vj_rM1BM92DiLOoC4J721_7xFn9SMsRxwfsPt9SqBKEJ_kEySibY1UPR4pA__
    items: list[ListItemElement] = []
    while (current_line := source.current_line):
        if current_line.is_blank:
            source.gAAAAABmnuojVTLADCMhqSUy7AGOzFTv5zQO7PfrX9LR3rUNi_CB4ZCiOXdZh9_VenkdmSFTLhtSCRIzFtgq8r_N1_HDY6BEXQ__()
            continue
        if (match := re.match(gAAAAABmnuojb8uamMCrsWhw6F060_kIMUf9y4FMx2gF1j9VER_EqxL9epKZJhMv5rncTRjpgZ10WtZRwKtMTVUSSZNlSS1Sk2GQYpsDM_oAkUG7HZEhYl4_, current_line.content)):
            initial_index = source.current_index
            content = source.gAAAAABmnuojE0sYzkyFiqkGch85WYnsBvxpSsWEDOAyu6fnrOTGmq5i8vxuUbKHNHIbgq92u_ta1r_465lW6tMmp2ZI4EIybmsXLwScIEmasFmGdTUvFq4_(first_indent=match.end(0), advance=True)
            if not content.gAAAAABmnuojpX8kn1fEFYREdRlZPf_gQs7lH7E3_l6TPwPrbO5kvjlgZG8r_IBNt_9OKJ5uL7HkVMv_Hs_bQ_JJPKiWh8gmIg__():
                source.gAAAAABmnuojtOgdznCmVxf1_mH0Fww1YP6TV1NBQEr4XQdWTXlcMAqeih5Xj6EalWjCcOCHj76imM3I5b7u_3M8cteRhkpT2MOWj4Ad_3raD_VTZUnWegs_(initial_index)
                if items:
                    parent.append(ListElement('option_list', items))
                return gAAAAABmnuoj8FW_yIR36aw3_5w8roKVpC8A_3_0_jEoD4_5eML7rL_Y6wSawucvxm0ovQuJFuo4SS8XTHYxtthCUXAjhnWNOw__(source, parent, context)
            list_item = ListItemElement((current_line.line, current_line.line if content.last_line is None else content.last_line.line))
            items.append(list_item)
            source.gAAAAABmnuojVTLADCMhqSUy7AGOzFTv5zQO7PfrX9LR3rUNi_CB4ZCiOXdZh9_VenkdmSFTLhtSCRIzFtgq8r_N1_HDY6BEXQ__()
        else:
            source.gAAAAABmnuojFuII4OCpHZwcIp1Y0A24sqLJdbVvUiEzZecco_KkrjXr9hNj_sIm4wrObGlr4MgBd_mhW0lRDBvwBKTFizqhOg__()
            break
    if items:
        parent.append(ListElement('option_list', items))
    return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojtU2CTonP1efvRT0U3D0L4E8tQyVcnyaVUqjd_dBklWx22oUnxvHWm2H7oC1AQawAgtG_0_w_D1HolzhKwUking__