from __future__ import annotations

import re

from rst_fast_parse.block_parsers.anonymous_target import gAAAAABmn4MYfFNGB4msHesk0V5FXYapItp6qqNj7tsxGE_TcGixAo6pr4OrkH8MdfRufDoGgApWmWcW5rBqQxxkR2Sko5PzVSwYZ_PQJofLtzbXUTWb0uQ_
from rst_fast_parse.block_parsers.blank_line import gAAAAABmn4MYvo_KwPYXMg90YZyN4baFZ0Vbt_12RgEbOH6sYGZgb95BkLLYRZ0GxDY6JFk_4D8bGbOfLLA_ty__GevSUTu_irtllRVErVfYyPrrC70Hf1Y_
from rst_fast_parse.block_parsers.block_quote import gAAAAABmn4MYO6Pz9lqIHBdRezCUjE9x3TwDB0S_1FIK7nlKC0HfK_A0hB3w1hXc_E7vQe1GoaWaQAYyjCS3qVzWxo8bdD3ho1RTOLTE07z_KYUEPszXYmg_
from rst_fast_parse.block_parsers.bullet_list import gAAAAABmn4MY2DpOw5CVRtjXO5zyaBixYoehEwyruB0DaFDdDAZzdoNQz7RVWB5sRCeM7J51tCa_N0CU3nPBddz9uHzJkzjzG08x9G_CPjDfqxDVdGMcjhM_
from rst_fast_parse.block_parsers.doctest_block import gAAAAABmn4MY_MxdFrVomaONhvrXUY9m8Wu6e6hvZnk4nggdeCMPDguVMi0l9Y0uUmG37j7TZnyWpVUHwfHEk_kPsdOZAu5rJ_kbJ3SRUSP9t_W5_Gq7upw_
from rst_fast_parse.block_parsers.enumerated_list import gAAAAABmn4MYJ_LbQpWuZ9wSVyYVtjmOY2BjcyaNMYHLmq3ulYN0tZrersBJYvbrh9j5wC9ZF5N7atM7jfrn0d4YDRWvSaZ__jfCLnJyH4GOrXfhWhTtkfM_
from rst_fast_parse.block_parsers.explicit_markups import gAAAAABmn4MYGTbQJXby_cFntbJEBcvGkYOPU542DNwL0IIQvUJNiTuAIa1XvWQn2dxnDzKNlc8bvd1hEOG_I3nWNz_VT0_whUCEfmZ9W_lSSNOR4IF9LG0_
from rst_fast_parse.block_parsers.fallback import gAAAAABmn4MYf0njqRPTsYiBbt6fiBQSV0TYAaDixMXvMgEhoZ8l5kmC3WL8uNy7GW8mhoSaqftINj2RmQwUyjd0bVjDUVgJXA__
from rst_fast_parse.block_parsers.field_list import gAAAAABmn4MYjiI2PvhWBsaQCX7EurGDbkU1bvYJlwp6Fye_BS7WMq_eT_6m7e1q7ars2ozFpS8G40KSsZxHhpkyTYHUDp8Vm4hgn0tJlB2Bnhn_4SoQOyw_
from rst_fast_parse.block_parsers.line_block import gAAAAABmn4MYdbya_P_Fnx4jHD09dyCS4iDEilPOYwOgkmIyOnJ7z9IwVslaUaEylh1iNxJaJ3EtnGHKnSqWb_YDM7__XKxZ5EYVl8K8JGQDhOwvMF4Gdqw_
from rst_fast_parse.block_parsers.line_marker import gAAAAABmn4MYDpZTxiaE7CGI5VSv_zmHjfm_pbMEAAVICSEMMZdJ0Br40iF8yTm3osG4ZqM7GgSYBEVqFWtCu7_RUS3TXk69__zGCqE16ML0YvR_Jjik4rY_
from rst_fast_parse.block_parsers.option_list import gAAAAABmn4MYiSx47RSfMznSKy0434f9o7VWKctiu8TLjQNu8wYO3Xv5lctNeYmJJN6WNgR_RR6VdPDrl69_9Y9redwVVVDWjyN_6Aer6_fURiBzB3e4c0I_
from rst_fast_parse.block_parsers.table_grid import gAAAAABmn4MYIsoclEK1tw6vXCcDurr4GCWFCs2kLsCk3zJCps_WnJIL1sffD_gtQlpLhz9HAZwNetrlKht8JSmiOEaVVKD9XafGYOVkq1H8ZsfQp5Jvc_s_
from rst_fast_parse.block_parsers.table_simple import gAAAAABmn4MYDm4BxCIDWeMRPQaYzJJWpTkJu_JRL5jGS3hC1goT0Vm5NLzm7TCHLVrLpC8QXs0WQCc4Gb0jxtBKE2n_9M0_kbAb_b99yECr0DgacWDl2ps_
from rst_fast_parse.core import gAAAAABmn4MY4r_tMHxH3zR3QnP_I6Udcic33ItT9kZ2N2eb_AK9mPPqdniTI0ZUreJ4p9_xE3jGMnPLrV9R_7eoh0Oow2_m5Q__, gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__
from rst_fast_parse.elements import ElementListBase
from rst_fast_parse.source import gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__, gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__

_DEFAULT_BLOCK_PARSERS: tuple[gAAAAABmn4MY4r_tMHxH3zR3QnP_I6Udcic33ItT9kZ2N2eb_AK9mPPqdniTI0ZUreJ4p9_xE3jGMnPLrV9R_7eoh0Oow2_m5Q__, ...] = (
    gAAAAABmn4MYvo_KwPYXMg90YZyN4baFZ0Vbt_12RgEbOH6sYGZgb95BkLLYRZ0GxDY6JFk_4D8bGbOfLLA_ty__GevSUTu_irtllRVErVfYyPrrC70Hf1Y_,
    gAAAAABmn4MYO6Pz9lqIHBdRezCUjE9x3TwDB0S_1FIK7nlKC0HfK_A0hB3w1hXc_E7vQe1GoaWaQAYyjCS3qVzWxo8bdD3ho1RTOLTE07z_KYUEPszXYmg_,
    gAAAAABmn4MY2DpOw5CVRtjXO5zyaBixYoehEwyruB0DaFDdDAZzdoNQz7RVWB5sRCeM7J51tCa_N0CU3nPBddz9uHzJkzjzG08x9G_CPjDfqxDVdGMcjhM_,
    gAAAAABmn4MYJ_LbQpWuZ9wSVyYVtjmOY2BjcyaNMYHLmq3ulYN0tZrersBJYvbrh9j5wC9ZF5N7atM7jfrn0d4YDRWvSaZ__jfCLnJyH4GOrXfhWhTtkfM_,
    gAAAAABmn4MYjiI2PvhWBsaQCX7EurGDbkU1bvYJlwp6Fye_BS7WMq_eT_6m7e1q7ars2ozFpS8G40KSsZxHhpkyTYHUDp8Vm4hgn0tJlB2Bnhn_4SoQOyw_,
    gAAAAABmn4MYiSx47RSfMznSKy0434f9o7VWKctiu8TLjQNu8wYO3Xv5lctNeYmJJN6WNgR_RR6VdPDrl69_9Y9redwVVVDWjyN_6Aer6_fURiBzB3e4c0I_,
    gAAAAABmn4MY_MxdFrVomaONhvrXUY9m8Wu6e6hvZnk4nggdeCMPDguVMi0l9Y0uUmG37j7TZnyWpVUHwfHEk_kPsdOZAu5rJ_kbJ3SRUSP9t_W5_Gq7upw_,
    gAAAAABmn4MYdbya_P_Fnx4jHD09dyCS4iDEilPOYwOgkmIyOnJ7z9IwVslaUaEylh1iNxJaJ3EtnGHKnSqWb_YDM7__XKxZ5EYVl8K8JGQDhOwvMF4Gdqw_,
    gAAAAABmn4MYIsoclEK1tw6vXCcDurr4GCWFCs2kLsCk3zJCps_WnJIL1sffD_gtQlpLhz9HAZwNetrlKht8JSmiOEaVVKD9XafGYOVkq1H8ZsfQp5Jvc_s_,
    gAAAAABmn4MYDm4BxCIDWeMRPQaYzJJWpTkJu_JRL5jGS3hC1goT0Vm5NLzm7TCHLVrLpC8QXs0WQCc4Gb0jxtBKE2n_9M0_kbAb_b99yECr0DgacWDl2ps_,
    gAAAAABmn4MYGTbQJXby_cFntbJEBcvGkYOPU542DNwL0IIQvUJNiTuAIa1XvWQn2dxnDzKNlc8bvd1hEOG_I3nWNz_VT0_whUCEfmZ9W_lSSNOR4IF9LG0_,
    gAAAAABmn4MYfFNGB4msHesk0V5FXYapItp6qqNj7tsxGE_TcGixAo6pr4OrkH8MdfRufDoGgApWmWcW5rBqQxxkR2Sko5PzVSwYZ_PQJofLtzbXUTWb0uQ_,
    gAAAAABmn4MYDpZTxiaE7CGI5VSv_zmHjfm_pbMEAAVICSEMMZdJ0Br40iF8yTm3osG4ZqM7GgSYBEVqFWtCu7_RUS3TXk69__zGCqE16ML0YvR_Jjik4rY_,
    gAAAAABmn4MYf0njqRPTsYiBbt6fiBQSV0TYAaDixMXvMgEhoZ8l5kmC3WL8uNy7GW8mhoSaqftINj2RmQwUyjd0bVjDUVgJXA__,
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
    context = gAAAAABmn4MYYGkkVklfAHap9sw1EIHXDNIKshm53CevB7hl8iJPCNPA58He66EPf_OLHEMqLGJTRILjwUrI39BxJAH1t_S_0g__(_DEFAULT_BLOCK_PARSERS)
    lines = _sanitize_string(text, tab_width=tab_width)
    slice = gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__(
        [
            gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__(line, offset_line=i, offset_char=offset_char, source=source_key)
            for i, line in enumerate(lines)
        ]
    )
    return context.gAAAAABmn4MYxo3_uMLISv2ozZeabQf_AVbssvdZ__FilsAixa2NxfwjhzSLJXhpPFmbJ7ea6ZD_vFMnNkYHXrs1DgEs89YIYg__(slice)
