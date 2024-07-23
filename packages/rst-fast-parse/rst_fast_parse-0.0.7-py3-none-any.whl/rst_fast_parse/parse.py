from __future__ import annotations

import re

from rst_fast_parse.block_parsers.anonymous_target import gAAAAABmnuojwfRPGVb4JXObBDVJaC_E3PTdJ8YZEXoaCbJqCoGJ6lYyegaOmEnZG9FeTyNGSSHWAC8PzYzBJM570Y7i5h4DYefwCLQCyc3zyAa44WZyI04_
from rst_fast_parse.block_parsers.blank_line import gAAAAABmnuojNyvg_M7yP1j5JJNW8_1HfkNwawes9RHswGEgMLJV1T4DcnefxiEmeDr3rqwNlAqNzDg99ZdE1pmGtzDmMp5tXBuuOjh_vWzyoua8BBZ413U_
from rst_fast_parse.block_parsers.block_quote import gAAAAABmnuojSZ_fraRyAzbgQJHtHanYT1MiqpRbu_yzojZYvb4igTZ0bJwPGzcvBNI_2cIIdIjnnGf_3C0isLIO48iqvwOeyScg9K2npJ_k9bMyPFj_SNU_
from rst_fast_parse.block_parsers.bullet_list import gAAAAABmnuojOCzhm3bvQlUeNv1XkKLVDcibvllTFBKrTlAwsucCM4LnE4_jeGod2x2Tyf4x_h1Ce9fMMopT_4tFfKemIjkpfhzijcSDWdr5YtXGByeAHjg_
from rst_fast_parse.block_parsers.doctest_block import gAAAAABmnuojanQkYTSgv_hqF35X7f_Wbsz_PiHG_ffisQGTb_dt_Yz_fNEv0UWLsD_49DLjS4CfOR7GDx3fvKL_h9V8GZ7itAr2KiMoS7tvqagV_sOu7MA_
from rst_fast_parse.block_parsers.enumerated_list import gAAAAABmnuojaLTymOKdK7gZCIcztKfsJZm8VQ7wxPqA__CNC2EaAu4hYohdhOMu_KSCJnJSHFBCrgIylPOM0L_vi88YKtuHN_zMddHQuZOMy0sneaZQ8_M_
from rst_fast_parse.block_parsers.explicit_markups import gAAAAABmnuoj5vtZ4_yz3AnafQbqou3bqoEVXCiR8JSeOM7mAAegh_OneWDHN5PlfwnldM2l_hQgeFQW5GlEo3IdDrj0puC2Gkohw2AkFmZbWxPxhAQhdxQ_
from rst_fast_parse.block_parsers.fallback import gAAAAABmnuoj8FW_yIR36aw3_5w8roKVpC8A_3_0_jEoD4_5eML7rL_Y6wSawucvxm0ovQuJFuo4SS8XTHYxtthCUXAjhnWNOw__
from rst_fast_parse.block_parsers.field_list import gAAAAABmnuojzQozNQXGnjhsSixWPIRlwBCg6OTCx6UECXIug85i9vXxN33tZq9Eds_tzzZtKW4OQ6FxMVJ_7DZbhG_QBTZ7tg5GtpkdH7g5gKd9TNiopIs_
from rst_fast_parse.block_parsers.line_block import gAAAAABmnuojYwp0ypBGPmbKTJ6QHiYX2SYprheAsH5nuDtma7s17VmDcQLJoUKgUFm42MQtu1wzVgDzZF8CRVlhiQUDdRRJUtN8JokGDf_CsU9eNlqgJyo_
from rst_fast_parse.block_parsers.line_marker import gAAAAABmnuoj_oSZkA3cO1TX0DGayzAuP_Ld_xKDnezIbkiML8FZqNMigN_QWT5N8Jbjqip4b6SEKcmu2u0GDvpkyasaAyIgRKSVBx4_crd2aB3z3a3VyQo_
from rst_fast_parse.block_parsers.option_list import gAAAAABmnuoj_evKoVHkM1ZSVJWOZ2vx0MBLmb4x0vgm1AOJzYHGXcjRYd__Rcpu9yRyqXkJ19JpTlJaVD841qdWcepK1FDKj7OLDNIZbQopHEcSkETkxeg_
from rst_fast_parse.block_parsers.table_grid import gAAAAABmnuoj6V9XIAWW4BQReklY3CxDutE6Bob9LY3aew9R3z9dbbDGEYboVCTTO22VRKBH0lhKS3AgvKbUIEtx3btGhnWUDte5ktKYfudCq298qegIo7Q_
from rst_fast_parse.block_parsers.table_simple import gAAAAABmnuojmwIh93hJ_68cTLLOve5ouueuRYwJU2MhqhTtINRLF7ALZz7HTHmQR_zHs4xF57ijdy3rkw_w0y5Xq3XzGwYYZjLtqHuNVg8yiJOLRM4nkbE_
from rst_fast_parse.core import gAAAAABmnuojQyqeDaQy__YnlWrGwcnNDnxX3WFc5sEYCq3YNFNSjWOb8708Q0QAEfAGoVBcddyFfkxZXO22_vMDLeo3VErrAQ__, gAAAAABmnuojyVOa__SFl52_gl5XSUoa6WT6zDtvviRWWFizGdPPVlComyZy1vRGpEh8_otsfmmSedteHWUAmThA0ExDLAlJng__
from rst_fast_parse.elements import ElementListBase
from rst_fast_parse.source import gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__, gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__

_DEFAULT_BLOCK_PARSERS: tuple[gAAAAABmnuojQyqeDaQy__YnlWrGwcnNDnxX3WFc5sEYCq3YNFNSjWOb8708Q0QAEfAGoVBcddyFfkxZXO22_vMDLeo3VErrAQ__, ...] = (
    gAAAAABmnuojNyvg_M7yP1j5JJNW8_1HfkNwawes9RHswGEgMLJV1T4DcnefxiEmeDr3rqwNlAqNzDg99ZdE1pmGtzDmMp5tXBuuOjh_vWzyoua8BBZ413U_,
    gAAAAABmnuojSZ_fraRyAzbgQJHtHanYT1MiqpRbu_yzojZYvb4igTZ0bJwPGzcvBNI_2cIIdIjnnGf_3C0isLIO48iqvwOeyScg9K2npJ_k9bMyPFj_SNU_,
    gAAAAABmnuojOCzhm3bvQlUeNv1XkKLVDcibvllTFBKrTlAwsucCM4LnE4_jeGod2x2Tyf4x_h1Ce9fMMopT_4tFfKemIjkpfhzijcSDWdr5YtXGByeAHjg_,
    gAAAAABmnuojaLTymOKdK7gZCIcztKfsJZm8VQ7wxPqA__CNC2EaAu4hYohdhOMu_KSCJnJSHFBCrgIylPOM0L_vi88YKtuHN_zMddHQuZOMy0sneaZQ8_M_,
    gAAAAABmnuojzQozNQXGnjhsSixWPIRlwBCg6OTCx6UECXIug85i9vXxN33tZq9Eds_tzzZtKW4OQ6FxMVJ_7DZbhG_QBTZ7tg5GtpkdH7g5gKd9TNiopIs_,
    gAAAAABmnuoj_evKoVHkM1ZSVJWOZ2vx0MBLmb4x0vgm1AOJzYHGXcjRYd__Rcpu9yRyqXkJ19JpTlJaVD841qdWcepK1FDKj7OLDNIZbQopHEcSkETkxeg_,
    gAAAAABmnuojanQkYTSgv_hqF35X7f_Wbsz_PiHG_ffisQGTb_dt_Yz_fNEv0UWLsD_49DLjS4CfOR7GDx3fvKL_h9V8GZ7itAr2KiMoS7tvqagV_sOu7MA_,
    gAAAAABmnuojYwp0ypBGPmbKTJ6QHiYX2SYprheAsH5nuDtma7s17VmDcQLJoUKgUFm42MQtu1wzVgDzZF8CRVlhiQUDdRRJUtN8JokGDf_CsU9eNlqgJyo_,
    gAAAAABmnuoj6V9XIAWW4BQReklY3CxDutE6Bob9LY3aew9R3z9dbbDGEYboVCTTO22VRKBH0lhKS3AgvKbUIEtx3btGhnWUDte5ktKYfudCq298qegIo7Q_,
    gAAAAABmnuojmwIh93hJ_68cTLLOve5ouueuRYwJU2MhqhTtINRLF7ALZz7HTHmQR_zHs4xF57ijdy3rkw_w0y5Xq3XzGwYYZjLtqHuNVg8yiJOLRM4nkbE_,
    gAAAAABmnuoj5vtZ4_yz3AnafQbqou3bqoEVXCiR8JSeOM7mAAegh_OneWDHN5PlfwnldM2l_hQgeFQW5GlEo3IdDrj0puC2Gkohw2AkFmZbWxPxhAQhdxQ_,
    gAAAAABmnuojwfRPGVb4JXObBDVJaC_E3PTdJ8YZEXoaCbJqCoGJ6lYyegaOmEnZG9FeTyNGSSHWAC8PzYzBJM570Y7i5h4DYefwCLQCyc3zyAa44WZyI04_,
    gAAAAABmnuoj_oSZkA3cO1TX0DGayzAuP_Ld_xKDnezIbkiML8FZqNMigN_QWT5N8Jbjqip4b6SEKcmu2u0GDvpkyasaAyIgRKSVBx4_crd2aB3z3a3VyQo_,
    gAAAAABmnuoj8FW_yIR36aw3_5w8roKVpC8A_3_0_jEoD4_5eML7rL_Y6wSawucvxm0ovQuJFuo4SS8XTHYxtthCUXAjhnWNOw__,
)


def _sanitize_string(
    text: str, *, tab_width: int = 8, convert_whitespace: bool = True
) -> list[str]:
    """Return a list of one-line strings with tabs expanded, no newlines, and
    trailing whitespace stripped.

    Each tab is expanded with between 1 and `tab_width` spaces, so that the
    next character's index becomes a multiple of `tab_width` (8 by default).

    :param text: a multi-line string.
    :param tab_width: the number of spaces to replace tabs with.
    :param convert_whitespace: convert form feeds and vertical tabs to spaces?
    """
    if convert_whitespace:
        text = re.sub("[\v\f]", " ", text)
    return [s.expandtabs(tab_width).rstrip() for s in text.splitlines()]


def parse_string(
    text: str,
    *,
    source_key: str | None = None,
    tab_width: int = 8,
    offset_char: int = 0,
) -> ElementListBase:
    """Parse a multi-line string and return a list of elements.

    :param text: a multi-line string.
    :param tab_width: the number of spaces to replace tabs with.
    """
    context = gAAAAABmnuojyVOa__SFl52_gl5XSUoa6WT6zDtvviRWWFizGdPPVlComyZy1vRGpEh8_otsfmmSedteHWUAmThA0ExDLAlJng__(_DEFAULT_BLOCK_PARSERS)
    lines = _sanitize_string(text, tab_width=tab_width)
    slice = gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__(
        [
            gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__(line, offset_line=i, offset_char=offset_char, source=source_key)
            for i, line in enumerate(lines)
        ]
    )
    return context.gAAAAABmnuojYfYikgFo6Xpz3o5GeAuyIG5Bm4jQ_phZM7QycxRg1nU_VOerZBtHPWnuPvpkVCeF744MIjsw1gNze_GW_gXZXQ__(slice)
