from __future__ import annotations
import re
from rst_fast_parse.core import gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_, gAAAAABmnuojyVOa__SFl52_gl5XSUoa6WT6zDtvviRWWFizGdPPVlComyZy1vRGpEh8_otsfmmSedteHWUAmThA0ExDLAlJng__
from rst_fast_parse.elements import BasicElement, ElementListBase, ListElement, ListItemElement, TitleElement
from rst_fast_parse.regexes.block import gAAAAABmnuojvmhWG0GxFRTZoCFSjm9HlguU5X6WyBPe5x0OW_DG_4Hp_lCuAl4WuH_wSm_ojaZJkcam2RLg34W_wE2cMW7utu0OKyKQP8f64WuNSEGBD2E_, gAAAAABmnuojHw_cBLhpC5HnThcFbZWML2VskxNGSeoCAVih5xyov_EHHcGI7L2ia3rUNbJ66yrYQf3Q45k_soXF57Jif8bQs_iRzabMAPSXHBDtTgabDMg_, gAAAAABmnuojDYYE1hQUod2M5mk4RU8L_PxciwG5Pusa1m9csw_xJxqlRNmbajlnSeNZG_wvjULrqDW20WzaKimiOUsbDxSCkA__, gAAAAABmnuojvIt_PpjJr24RLliunuY0LyDk1Gsm0ZgIwAQQad_jpiKnFYOcbXahn6zbWc_P1_8ZhvEGC7i8nNe2_N_YiBUDCA__, gAAAAABmnuojG1T8huthc5pOyhV_YKvYaYbr1STBeeNQTq0bAOWVhOd8qSh2Keb4bLxlomWplEfPL6njXFy4TKrRJLptTKqRuw__, gAAAAABmnuojneQp8ioMt4Crvi2R3rai5pmJHhAMYtpyCB89KPUG4KcNA8A2N5nvgkl6zY6Bdl3srM_UTRsplNXNzH5M2JgxyA__, gAAAAABmnuojHlMoOwxNiGQlqbX0aKsUdxwpy3k7vYumKkv4NQtPpbl8nlr1HCFWgbZaMKs_OqFttJG_2LoysZwCMxsECRdzSA__, gAAAAABmnuojYIN8IFfAQb0dqgf1jweZHoUo6jdtX9sGeKMCWTX_ZgcCsDS6sSJ_C6RxKE0qGlybQDBFA3Q46uaTf_69Lq_y9Ffix8VJs4nBBMM5tK9H0iM_, gAAAAABmnuojb8uamMCrsWhw6F060_kIMUf9y4FMx2gF1j9VER_EqxL9epKZJhMv5rncTRjpgZ10WtZRwKtMTVUSSZNlSS1Sk2GQYpsDM_oAkUG7HZEhYl4_, gAAAAABmnuojRu5mOfehDBiXYdWWZRHsOKAw0krzrWVBq9K3dKoYb_ahbz5L95whoZJO9oOB4ABnSusUp0p6iEarX_d_3p8ebsMtDMVHlUhPvFQb_riEKzQ_, gAAAAABmnuoj9AV02r2yqdVk5KGsMV7xRq_uRScvURRUB8n0mwg4XSnqkF6c_tVfvaAhFrU_2P4XceStufPsnd4RcqCni37VcE_oFYX0vruaa4Ct5dWQZPg_, gAAAAABmnuoj3RAf6U8gYVVrGadbuU4Qu5vKvZ6vpXfVIolIflaL9CfUE2VXokV9cmXTwbyKGxlDQmBkjYj6MkvLB_bSjXn9rQ__, gAAAAABmnuoj_IJUhn_Y6bOQ0ceB29aTG9pLtbkSimVAFSQbQpGxsbxonhVhLueUy14FVzy7w0fa0bxj98pOzV1pjJHjzRhhdg__
from rst_fast_parse.source import gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__, gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__
from rst_fast_parse.utils.column_widths import gAAAAABmnuojAyLrVjacBgZUW_gZz1RsYgh30xGIW91jRnp3SRO2_SVC1N_9h72jzM_pVHfGwvzDfNmQV_qViMB12DBOHJGCHg__

def gAAAAABmnuoj8FW_yIR36aw3_5w8roKVpC8A_3_0_jEoD4_5eML7rL_Y6wSawucvxm0ovQuJFuo4SS8XTHYxtthCUXAjhnWNOw__(source: gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__, parent: ElementListBase, context: gAAAAABmnuojyVOa__SFl52_gl5XSUoa6WT6zDtvviRWWFizGdPPVlComyZy1vRGpEh8_otsfmmSedteHWUAmThA0ExDLAlJng__, /) -> gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_:
    if not (current_line := source.current_line):
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuoj3aryYICdV_DRXww7_sB4t47whKoHzQbi63L259co7hXyWE0ipEj7HxYbUAe60Pyz7XEQS8izK2QkZQBfWccvGA__
    next_line = source.gAAAAABmnuojE1KGsr0TOFHaREF1loYgV0lWiRlfD2YdF5asAdfPtOfBkAv_9JkPtm8YOU_PzWoISZ4FTPPO1DO1m6oXqtClug__()
    if next_line is None or next_line.is_blank:
        gAAAAABmnuojCn5Se3OwqPvNDFvntonGDZjl2_j_15yFHJT1_FMRXytYrrG2mToIrM7Sjlugb71PUCiZbQDoQkAtz4rkb5JYYN0p0OCIvJJIgCV7l4M_jE4_(current_line, source, parent, context)
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojtU2CTonP1efvRT0U3D0L4E8tQyVcnyaVUqjd_dBklWx22oUnxvHWm2H7oC1AQawAgtG_0_w_D1HolzhKwUking__
    if next_line.content and next_line.content[0] == ' ':
        gAAAAABmnuoj3i4wO6S987GxgI74LZ2YkfKDcGlUjQ8AFDHdHWjTeWQqFU7S9_CpOPo49sRTVYeqP1RZngDqaqjnMrFZxRaEuJrx_2JksGvk47s142CI8NE_(source, parent, context)
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojtU2CTonP1efvRT0U3D0L4E8tQyVcnyaVUqjd_dBklWx22oUnxvHWm2H7oC1AQawAgtG_0_w_D1HolzhKwUking__
    min_marker_length = 4
    if re.match(gAAAAABmnuoj9AV02r2yqdVk5KGsMV7xRq_uRScvURRUB8n0mwg4XSnqkF6c_tVfvaAhFrU_2P4XceStufPsnd4RcqCni37VcE_oFYX0vruaa4Ct5dWQZPg_, next_line.content):
        title = current_line.content.rstrip()
        underline = next_line.content.rstrip()
        if gAAAAABmnuojAyLrVjacBgZUW_gZz1RsYgh30xGIW91jRnp3SRO2_SVC1N_9h72jzM_pVHfGwvzDfNmQV_qViMB12DBOHJGCHg__(title) > len(underline):
            if len(underline) < min_marker_length:
                gAAAAABmnuojDFBVN8qFrXtP6XNTQPWhTWbeZoTYfHmPYGW4isxhKvRfWLgaNWuyAdqE18hcmdQ6kIpdhy8touZufZ18yyoEHa77GrIu7geTtCutrfgkdjs_(source, parent, context)
                return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojtU2CTonP1efvRT0U3D0L4E8tQyVcnyaVUqjd_dBklWx22oUnxvHWm2H7oC1AQawAgtG_0_w_D1HolzhKwUking__
        if not context.allow_titles:
            source.gAAAAABmnuojVTLADCMhqSUy7AGOzFTv5zQO7PfrX9LR3rUNi_CB4ZCiOXdZh9_VenkdmSFTLhtSCRIzFtgq8r_N1_HDY6BEXQ__()
            return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojtU2CTonP1efvRT0U3D0L4E8tQyVcnyaVUqjd_dBklWx22oUnxvHWm2H7oC1AQawAgtG_0_w_D1HolzhKwUking__
        source.gAAAAABmnuojVTLADCMhqSUy7AGOzFTv5zQO7PfrX9LR3rUNi_CB4ZCiOXdZh9_VenkdmSFTLhtSCRIzFtgq8r_N1_HDY6BEXQ__()
        parent.append(TitleElement(False, underline[0], title, (current_line.line, next_line.line)))
        return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojtU2CTonP1efvRT0U3D0L4E8tQyVcnyaVUqjd_dBklWx22oUnxvHWm2H7oC1AQawAgtG_0_w_D1HolzhKwUking__
    gAAAAABmnuojDFBVN8qFrXtP6XNTQPWhTWbeZoTYfHmPYGW4isxhKvRfWLgaNWuyAdqE18hcmdQ6kIpdhy8touZufZ18yyoEHa77GrIu7geTtCutrfgkdjs_(source, parent, context)
    return gAAAAABmnuojOGBo9zpldLVHFedVghdnlO230wsxllTO9iqKR5hAMB3B_KVN_SsEa6El4dIXTSsDP6Wb3Rq9V3wFjrzs3JHZ7xSw1ALJX04Jn4EEV7AdqUs_.gAAAAABmnuojtU2CTonP1efvRT0U3D0L4E8tQyVcnyaVUqjd_dBklWx22oUnxvHWm2H7oC1AQawAgtG_0_w_D1HolzhKwUking__

def gAAAAABmnuojCn5Se3OwqPvNDFvntonGDZjl2_j_15yFHJT1_FMRXytYrrG2mToIrM7Sjlugb71PUCiZbQDoQkAtz4rkb5JYYN0p0OCIvJJIgCV7l4M_jE4_(current_line: gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__, source: gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__, parent: ElementListBase, context: gAAAAABmnuojyVOa__SFl52_gl5XSUoa6WT6zDtvviRWWFizGdPPVlComyZy1vRGpEh8_otsfmmSedteHWUAmThA0ExDLAlJng__, /) -> None:
    paragraph_line = current_line.rstrip()
    literal_block_next = re.search(gAAAAABmnuojYIN8IFfAQb0dqgf1jweZHoUo6jdtX9sGeKMCWTX_ZgcCsDS6sSJ_C6RxKE0qGlybQDBFA3Q46uaTf_69Lq_y9Ffix8VJs4nBBMM5tK9H0iM_, paragraph_line.content)
    parent.append(BasicElement('paragraph', (paragraph_line.line, paragraph_line.line)))
    if literal_block_next:
        gAAAAABmnuojGUeHZL06kVcvTErD_azzdF5cmSakHfT9XQJO7uS0TZTF4ie6nSz6UTYzNDyHNRGMDyaUcSpVbXOGMbW0aeBldQ__(source, parent, context)

def gAAAAABmnuojDFBVN8qFrXtP6XNTQPWhTWbeZoTYfHmPYGW4isxhKvRfWLgaNWuyAdqE18hcmdQ6kIpdhy8touZufZ18yyoEHa77GrIu7geTtCutrfgkdjs_(source: gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__, parent: ElementListBase, context: gAAAAABmnuojyVOa__SFl52_gl5XSUoa6WT6zDtvviRWWFizGdPPVlComyZy1vRGpEh8_otsfmmSedteHWUAmThA0ExDLAlJng__, /) -> None:
    if (_current_line := source.current_line) is None:
        return None
    text_slice = source.gAAAAABmnuojAw2_K1MUJfEWaK3kzjuTvo88vLk_f95tXe6AH6uLDTCFgmfftIO9unF1YNnq42C1ZWAcq0_mHyiVXLAKmb9YaQ__(stop_on_indented=True, advance=True)
    text_content = text_slice.gAAAAABmnuojhmM7eo4fxyy83rSx8Ln1jbrZZ1ztUEIEAL4L7EBgCqRKNqxN_2uBPuj4PMYNpK_vk25SSXW4rTn54w78ovRrOA__().rstrip()
    literal_block_next = re.search(gAAAAABmnuojYIN8IFfAQb0dqgf1jweZHoUo6jdtX9sGeKMCWTX_ZgcCsDS6sSJ_C6RxKE0qGlybQDBFA3Q46uaTf_69Lq_y9Ffix8VJs4nBBMM5tK9H0iM_, text_content)
    if (first := text_slice.current_line) and (last := text_slice.last_line):
        parent.append(BasicElement('paragraph', (first.line, last.line)))
    if literal_block_next:
        gAAAAABmnuojGUeHZL06kVcvTErD_azzdF5cmSakHfT9XQJO7uS0TZTF4ie6nSz6UTYzNDyHNRGMDyaUcSpVbXOGMbW0aeBldQ__(source, parent, context)
    return None

def gAAAAABmnuojGUeHZL06kVcvTErD_azzdF5cmSakHfT9XQJO7uS0TZTF4ie6nSz6UTYzNDyHNRGMDyaUcSpVbXOGMbW0aeBldQ__(source: gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__, parent: ElementListBase, context: gAAAAABmnuojyVOa__SFl52_gl5XSUoa6WT6zDtvviRWWFizGdPPVlComyZy1vRGpEh8_otsfmmSedteHWUAmThA0ExDLAlJng__, /) -> None:
    original_index = source.current_index
    source.gAAAAABmnuojVTLADCMhqSUy7AGOzFTv5zQO7PfrX9LR3rUNi_CB4ZCiOXdZh9_VenkdmSFTLhtSCRIzFtgq8r_N1_HDY6BEXQ__()
    block_slice = source.gAAAAABmnuojxalrA5Gj4NfX4HRsFfT1K2BubPoosVKj4pJ0KY1yjC95pHUbH4Bphc22V9TaBVmbPbILLGY78BQ3YrtLI_AEmw__(advance=True).gAAAAABmnuojY5ocgTVs8voiw0yEbvCq9zGLVthGnhdSUdtBwBBeGoySmXJCs2b__a3Op8OH61b_tI_w085CNPDwYjMcv2pEJBSabclR6lr6IIgdmgDAmlM_()
    if not block_slice.gAAAAABmnuojpX8kn1fEFYREdRlZPf_gQs7lH7E3_l6TPwPrbO5kvjlgZG8r_IBNt_9OKJ5uL7HkVMv_Hs_bQ_JJPKiWh8gmIg__():
        source.gAAAAABmnuojtOgdznCmVxf1_mH0Fww1YP6TV1NBQEr4XQdWTXlcMAqeih5Xj6EalWjCcOCHj76imM3I5b7u_3M8cteRhkpT2MOWj4Ad_3raD_VTZUnWegs_(original_index)
        peek_index = 2
        while (next_line := source.gAAAAABmnuojE1KGsr0TOFHaREF1loYgV0lWiRlfD2YdF5asAdfPtOfBkAv_9JkPtm8YOU_PzWoISZ4FTPPO1DO1m6oXqtClug__(peek_index)) and next_line.is_blank:
            peek_index += 1
        if (next_line := source.gAAAAABmnuojE1KGsr0TOFHaREF1loYgV0lWiRlfD2YdF5asAdfPtOfBkAv_9JkPtm8YOU_PzWoISZ4FTPPO1DO1m6oXqtClug__(peek_index)) and re.match(gAAAAABmnuojRu5mOfehDBiXYdWWZRHsOKAw0krzrWVBq9K3dKoYb_ahbz5L95whoZJO9oOB4ABnSusUp0p6iEarX_d_3p8ebsMtDMVHlUhPvFQb_riEKzQ_, next_line.content):
            quote_char = next_line.content[0]
            source.gAAAAABmnuojVTLADCMhqSUy7AGOzFTv5zQO7PfrX9LR3rUNi_CB4ZCiOXdZh9_VenkdmSFTLhtSCRIzFtgq8r_N1_HDY6BEXQ__(peek_index - 1)
            lines = []
            while (next_line := source.gAAAAABmnuojE1KGsr0TOFHaREF1loYgV0lWiRlfD2YdF5asAdfPtOfBkAv_9JkPtm8YOU_PzWoISZ4FTPPO1DO1m6oXqtClug__(1)) and next_line.content and (next_line.content[0] == quote_char):
                lines.append(next_line)
                source.gAAAAABmnuojVTLADCMhqSUy7AGOzFTv5zQO7PfrX9LR3rUNi_CB4ZCiOXdZh9_VenkdmSFTLhtSCRIzFtgq8r_N1_HDY6BEXQ__()
            block_slice = gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__(lines)
        else:
            return None
    if (first := block_slice.current_line) and (last := block_slice.last_line):
        parent.append(BasicElement('literal_block', (first.line, last.line)))

def gAAAAABmnuoj3i4wO6S987GxgI74LZ2YkfKDcGlUjQ8AFDHdHWjTeWQqFU7S9_CpOPo49sRTVYeqP1RZngDqaqjnMrFZxRaEuJrx_2JksGvk47s142CI8NE_(source: gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__, parent: ElementListBase, context: gAAAAABmnuojyVOa__SFl52_gl5XSUoa6WT6zDtvviRWWFizGdPPVlComyZy1vRGpEh8_otsfmmSedteHWUAmThA0ExDLAlJng__, /) -> None:
    items: list[ListItemElement] = []
    while (first_line := source.current_line):
        if items:
            if first_line.is_blank:
                source.gAAAAABmnuojVTLADCMhqSUy7AGOzFTv5zQO7PfrX9LR3rUNi_CB4ZCiOXdZh9_VenkdmSFTLhtSCRIzFtgq8r_N1_HDY6BEXQ__()
                continue
            if first_line.content[0] == ' ' or any((re.match(regex, first_line.content) for regex in (gAAAAABmnuojHw_cBLhpC5HnThcFbZWML2VskxNGSeoCAVih5xyov_EHHcGI7L2ia3rUNbJ66yrYQf3Q45k_soXF57Jif8bQs_iRzabMAPSXHBDtTgabDMg_, gAAAAABmnuojvIt_PpjJr24RLliunuY0LyDk1Gsm0ZgIwAQQad_jpiKnFYOcbXahn6zbWc_P1_8ZhvEGC7i8nNe2_N_YiBUDCA__, gAAAAABmnuojneQp8ioMt4Crvi2R3rai5pmJHhAMYtpyCB89KPUG4KcNA8A2N5nvgkl6zY6Bdl3srM_UTRsplNXNzH5M2JgxyA__, gAAAAABmnuojb8uamMCrsWhw6F060_kIMUf9y4FMx2gF1j9VER_EqxL9epKZJhMv5rncTRjpgZ10WtZRwKtMTVUSSZNlSS1Sk2GQYpsDM_oAkUG7HZEhYl4_, gAAAAABmnuojDYYE1hQUod2M5mk4RU8L_PxciwG5Pusa1m9csw_xJxqlRNmbajlnSeNZG_wvjULrqDW20WzaKimiOUsbDxSCkA__, gAAAAABmnuojHlMoOwxNiGQlqbX0aKsUdxwpy3k7vYumKkv4NQtPpbl8nlr1HCFWgbZaMKs_OqFttJG_2LoysZwCMxsECRdzSA__, gAAAAABmnuoj3RAf6U8gYVVrGadbuU4Qu5vKvZ6vpXfVIolIflaL9CfUE2VXokV9cmXTwbyKGxlDQmBkjYj6MkvLB_bSjXn9rQ__, gAAAAABmnuoj_IJUhn_Y6bOQ0ceB29aTG9pLtbkSimVAFSQbQpGxsbxonhVhLueUy14FVzy7w0fa0bxj98pOzV1pjJHjzRhhdg__, gAAAAABmnuojG1T8huthc5pOyhV_YKvYaYbr1STBeeNQTq0bAOWVhOd8qSh2Keb4bLxlomWplEfPL6njXFy4TKrRJLptTKqRuw__, gAAAAABmnuojvmhWG0GxFRTZoCFSjm9HlguU5X6WyBPe5x0OW_DG_4Hp_lCuAl4WuH_wSm_ojaZJkcam2RLg34W_wE2cMW7utu0OKyKQP8f64WuNSEGBD2E_, gAAAAABmnuoj9AV02r2yqdVk5KGsMV7xRq_uRScvURRUB8n0mwg4XSnqkF6c_tVfvaAhFrU_2P4XceStufPsnd4RcqCni37VcE_oFYX0vruaa4Ct5dWQZPg_))):
                source.gAAAAABmnuojFuII4OCpHZwcIp1Y0A24sqLJdbVvUiEzZecco_KkrjXr9hNj_sIm4wrObGlr4MgBd_mhW0lRDBvwBKTFizqhOg__()
                break
        if (next_line := source.gAAAAABmnuojE1KGsr0TOFHaREF1loYgV0lWiRlfD2YdF5asAdfPtOfBkAv_9JkPtm8YOU_PzWoISZ4FTPPO1DO1m6oXqtClug__()):
            if next_line.content and next_line.content[0] == ' ':
                source.gAAAAABmnuojVTLADCMhqSUy7AGOzFTv5zQO7PfrX9LR3rUNi_CB4ZCiOXdZh9_VenkdmSFTLhtSCRIzFtgq8r_N1_HDY6BEXQ__()
            else:
                source.gAAAAABmnuojFuII4OCpHZwcIp1Y0A24sqLJdbVvUiEzZecco_KkrjXr9hNj_sIm4wrObGlr4MgBd_mhW0lRDBvwBKTFizqhOg__()
                break
        else:
            source.gAAAAABmnuojFuII4OCpHZwcIp1Y0A24sqLJdbVvUiEzZecco_KkrjXr9hNj_sIm4wrObGlr4MgBd_mhW0lRDBvwBKTFizqhOg__()
            break
        definition = first_line
        description = source.gAAAAABmnuojxalrA5Gj4NfX4HRsFfT1K2BubPoosVKj4pJ0KY1yjC95pHUbH4Bphc22V9TaBVmbPbILLGY78BQ3YrtLI_AEmw__(advance=True)
        list_item = ListItemElement((definition.line, definition.line if description.last_line is None else description.last_line.line))
        items.append(list_item)
        source.gAAAAABmnuojVTLADCMhqSUy7AGOzFTv5zQO7PfrX9LR3rUNi_CB4ZCiOXdZh9_VenkdmSFTLhtSCRIzFtgq8r_N1_HDY6BEXQ__()
    if items:
        parent.append(ListElement('definition_list', items))