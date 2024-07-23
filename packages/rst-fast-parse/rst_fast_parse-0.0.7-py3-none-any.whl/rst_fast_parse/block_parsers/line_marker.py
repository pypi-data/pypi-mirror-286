from __future__ import annotations
import re
from rst_fast_parse.block_parsers.fallback import gAAAAABmnuoj8FW_yIR36aw3_5w8roKVpC8A_3_0_jEoD4_5eML7rL_Y6wSawucvxm0ovQuJFuo4SS8XTHYxtthCUXAjhnWNOw__
from rst_fast_parse.core import gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_, gAAAAABmnuojyVOa__SFl52_gl5XSUoa6WT6zDtvviRWWFizGdPPVlComyZy1vRGpEh8_otsfmmSedteHWUAmThA0ExDLAlJng__
from rst_fast_parse.elements import ElementListBase, TitleElement, TransitionElement
from rst_fast_parse.regexes.block import gAAAAABmnuoj9AV02r2yqdVk5KGsMV7xRq_uRScvURRUB8n0mwg4XSnqkF6c_tVfvaAhFrU_2P4XceStufPsnd4RcqCni37VcE_oFYX0vruaa4Ct5dWQZPg_
from rst_fast_parse.source import gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__, gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__
from rst_fast_parse.utils.column_widths import gAAAAABmnuojAyLrVjacBgZUW_gZz1RsYgh30xGIW91jRnp3SRO2_SVC1N_9h72jzM_pVHfGwvzDfNmQV_qViMB12DBOHJGCHg__

def gAAAAABmnuoj_oSZkA3cO1TX0DGayzAuP_Ld_xKDnezIbkiML8FZqNMigN_QWT5N8Jbjqip4b6SEKcmu2u0GDvpkyasaAyIgRKSVBx4_crd2aB3z3a3VyQo_(source: gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__, parent: ElementListBase, context: gAAAAABmnuojyVOa__SFl52_gl5XSUoa6WT6zDtvviRWWFizGdPPVlComyZy1vRGpEh8_otsfmmSedteHWUAmThA0ExDLAlJng__, /) -> gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_:
    if not (current_line := source.current_line):
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuoj3aryYICdV_DRXww7_sB4t47whKoHzQbi63L259co7hXyWE0ipEj7HxYbUAe60Pyz7XEQS8izK2QkZQBfWccvGA__
    if not (match := re.match(gAAAAABmnuoj9AV02r2yqdVk5KGsMV7xRq_uRScvURRUB8n0mwg4XSnqkF6c_tVfvaAhFrU_2P4XceStufPsnd4RcqCni37VcE_oFYX0vruaa4Ct5dWQZPg_, current_line.content)):
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojR_bJJWp1wWXX31xmpSl2WA0iZ_2vj_rM1BM92DiLOoC4J721_7xFn9SMsRxwfsPt9SqBKEJ_kEySibY1UPR4pA__
    marker = match.string.strip()
    marker_char = marker[0]
    marker_length = len(marker)
    min_marker_length = 4
    if not context.allow_titles:
        if marker == '::':
            return gAAAAABmnuoj8FW_yIR36aw3_5w8roKVpC8A_3_0_jEoD4_5eML7rL_Y6wSawucvxm0ovQuJFuo4SS8XTHYxtthCUXAjhnWNOw__(source, parent, context)
        if marker_length < min_marker_length:
            return gAAAAABmnuoj8FW_yIR36aw3_5w8roKVpC8A_3_0_jEoD4_5eML7rL_Y6wSawucvxm0ovQuJFuo4SS8XTHYxtthCUXAjhnWNOw__(source, parent, context)
        parent.append(gAAAAABmnuojxKNsI8cZXCKcZYISgq5_iQ9LQ_xlIH1_YCEynx5vPgXkNbJM_9jDHiM8j6dfhdDrP_HjafYxQabgeB3bf4cQvw__(marker_char, current_line))
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojtU2CTonP1efvRT0U3D0L4E8tQyVcnyaVUqjd_dBklWx22oUnxvHWm2H7oC1AQawAgtG_0_w_D1HolzhKwUking__
    next_line = source.gAAAAABmnuojE1KGsr0TOFHaREF1loYgV0lWiRlfD2YdF5asAdfPtOfBkAv_9JkPtm8YOU_PzWoISZ4FTPPO1DO1m6oXqtClug__()
    if next_line is None or next_line.is_blank:
        if marker_length < min_marker_length:
            return gAAAAABmnuoj8FW_yIR36aw3_5w8roKVpC8A_3_0_jEoD4_5eML7rL_Y6wSawucvxm0ovQuJFuo4SS8XTHYxtthCUXAjhnWNOw__(source, parent, context)
        parent.append(gAAAAABmnuojxKNsI8cZXCKcZYISgq5_iQ9LQ_xlIH1_YCEynx5vPgXkNbJM_9jDHiM8j6dfhdDrP_HjafYxQabgeB3bf4cQvw__(marker_char, current_line))
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojtU2CTonP1efvRT0U3D0L4E8tQyVcnyaVUqjd_dBklWx22oUnxvHWm2H7oC1AQawAgtG_0_w_D1HolzhKwUking__
    if re.match(gAAAAABmnuoj9AV02r2yqdVk5KGsMV7xRq_uRScvURRUB8n0mwg4XSnqkF6c_tVfvaAhFrU_2P4XceStufPsnd4RcqCni37VcE_oFYX0vruaa4Ct5dWQZPg_, next_line.content):
        if marker_length < min_marker_length:
            return gAAAAABmnuoj8FW_yIR36aw3_5w8roKVpC8A_3_0_jEoD4_5eML7rL_Y6wSawucvxm0ovQuJFuo4SS8XTHYxtthCUXAjhnWNOw__(source, parent, context)
        parent.append(gAAAAABmnuojxKNsI8cZXCKcZYISgq5_iQ9LQ_xlIH1_YCEynx5vPgXkNbJM_9jDHiM8j6dfhdDrP_HjafYxQabgeB3bf4cQvw__(marker_char, current_line))
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojtU2CTonP1efvRT0U3D0L4E8tQyVcnyaVUqjd_dBklWx22oUnxvHWm2H7oC1AQawAgtG_0_w_D1HolzhKwUking__
    next_next_line = source.gAAAAABmnuojE1KGsr0TOFHaREF1loYgV0lWiRlfD2YdF5asAdfPtOfBkAv_9JkPtm8YOU_PzWoISZ4FTPPO1DO1m6oXqtClug__(2)
    if next_next_line is None:
        if marker_length < min_marker_length:
            return gAAAAABmnuoj8FW_yIR36aw3_5w8roKVpC8A_3_0_jEoD4_5eML7rL_Y6wSawucvxm0ovQuJFuo4SS8XTHYxtthCUXAjhnWNOw__(source, parent, context)
        parent.append(gAAAAABmnuojxKNsI8cZXCKcZYISgq5_iQ9LQ_xlIH1_YCEynx5vPgXkNbJM_9jDHiM8j6dfhdDrP_HjafYxQabgeB3bf4cQvw__(marker_char, current_line))
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojtU2CTonP1efvRT0U3D0L4E8tQyVcnyaVUqjd_dBklWx22oUnxvHWm2H7oC1AQawAgtG_0_w_D1HolzhKwUking__
    if (underline_match := re.match(gAAAAABmnuoj9AV02r2yqdVk5KGsMV7xRq_uRScvURRUB8n0mwg4XSnqkF6c_tVfvaAhFrU_2P4XceStufPsnd4RcqCni37VcE_oFYX0vruaa4Ct5dWQZPg_, next_next_line.content)) is None:
        if marker_length < min_marker_length:
            return gAAAAABmnuoj8FW_yIR36aw3_5w8roKVpC8A_3_0_jEoD4_5eML7rL_Y6wSawucvxm0ovQuJFuo4SS8XTHYxtthCUXAjhnWNOw__(source, parent, context)
        parent.append(gAAAAABmnuojxKNsI8cZXCKcZYISgq5_iQ9LQ_xlIH1_YCEynx5vPgXkNbJM_9jDHiM8j6dfhdDrP_HjafYxQabgeB3bf4cQvw__(marker_char, current_line))
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojtU2CTonP1efvRT0U3D0L4E8tQyVcnyaVUqjd_dBklWx22oUnxvHWm2H7oC1AQawAgtG_0_w_D1HolzhKwUking__
    underline = underline_match.string.rstrip()
    if marker != underline:
        if marker_length < min_marker_length:
            return gAAAAABmnuoj8FW_yIR36aw3_5w8roKVpC8A_3_0_jEoD4_5eML7rL_Y6wSawucvxm0ovQuJFuo4SS8XTHYxtthCUXAjhnWNOw__(source, parent, context)
        parent.append(gAAAAABmnuojxKNsI8cZXCKcZYISgq5_iQ9LQ_xlIH1_YCEynx5vPgXkNbJM_9jDHiM8j6dfhdDrP_HjafYxQabgeB3bf4cQvw__(marker_char, current_line))
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojtU2CTonP1efvRT0U3D0L4E8tQyVcnyaVUqjd_dBklWx22oUnxvHWm2H7oC1AQawAgtG_0_w_D1HolzhKwUking__
    title = next_line.content.rstrip()
    if gAAAAABmnuojAyLrVjacBgZUW_gZz1RsYgh30xGIW91jRnp3SRO2_SVC1N_9h72jzM_pVHfGwvzDfNmQV_qViMB12DBOHJGCHg__(title) > marker_length:
        if marker_length < min_marker_length:
            return gAAAAABmnuoj8FW_yIR36aw3_5w8roKVpC8A_3_0_jEoD4_5eML7rL_Y6wSawucvxm0ovQuJFuo4SS8XTHYxtthCUXAjhnWNOw__(source, parent, context)
    source.gAAAAABmnuojVTLADCMhqSUy7AGOzFTv5zQO7PfrX9LR3rUNi_CB4ZCiOXdZh9_VenkdmSFTLhtSCRIzFtgq8r_N1_HDY6BEXQ__(2)
    parent.append(TitleElement(True, marker[0], title, (current_line.line, next_next_line.line)))
    return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojtU2CTonP1efvRT0U3D0L4E8tQyVcnyaVUqjd_dBklWx22oUnxvHWm2H7oC1AQawAgtG_0_w_D1HolzhKwUking__

def gAAAAABmnuojxKNsI8cZXCKcZYISgq5_iQ9LQ_xlIH1_YCEynx5vPgXkNbJM_9jDHiM8j6dfhdDrP_HjafYxQabgeB3bf4cQvw__(style: str, line: gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__) -> TransitionElement:
    return TransitionElement(style, (line.line, line.line))