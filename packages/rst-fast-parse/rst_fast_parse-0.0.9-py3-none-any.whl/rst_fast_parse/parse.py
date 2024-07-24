from __future__ import annotations

import re

from rst_fast_parse.block_parsers.anonymous_target import gAAAAABmoAOUKR0M0HScNoUePVIKWWUNrP_POPvERE6Qy9GhSMeH07QgwNUnzQrZb_lJU5cI0zyebH_BJLRiHwwCYByjNpLzjC3KEhC8uxTsUKUF3LqSZF8_
from rst_fast_parse.block_parsers.blank_line import gAAAAABmoAOUuA3eBv2vGYZEJW3gUA__kHl9WdI_mduoNY_Ht2iQF9yGIMuFRFkHXd5dBFP463DRCSNgDoChCZ_0uG2b_BYVw_Pm7yf3Rn61Uit28bg58jQ_
from rst_fast_parse.block_parsers.block_quote import gAAAAABmoAOU2G7JntteCshsuyI4pWZw6iMjANa3_pzgo1J8Co7OzylVHtFXNIVgQ_csrfcK8kHC4XUhPZHVKaSvDTC7ocwSegqdSqGth87n_vogaoqFbKk_
from rst_fast_parse.block_parsers.bullet_list import gAAAAABmoAOUbB2ETvLyPxSGayUepPIJ2Iyw96wikvNkX7K3uV9hI4LUA86whDK6xWR2rJsP2UkPcObXM1_k0nHnmQA4Gl9lFG4evEOZVDDEf3UvvQDNTWY_
from rst_fast_parse.block_parsers.doctest_block import gAAAAABmoAOUZqQfhhAZAhzc4__Ty8_8jWBJrjudf6dyUZiRHOLpRncezITssQx0qwNf3HfQm8UvcEAW_Kmn9yIy3lKoptA_SVXZBo_qXmNQdQhnh0_tSts_
from rst_fast_parse.block_parsers.enumerated_list import gAAAAABmoAOUWMukC3xWibby_gWTQjsrg2NXLqBXikahSkcMtU0pJKKOwRPgbuPIdRz0W6_1AQswYpCc7yFZSoCfC251hVSr1K_9Vv9LYIVv1HbvaL2LHNE_
from rst_fast_parse.block_parsers.explicit_markups import gAAAAABmoAOU8iBQud1CGsfVwOoqEIQVvKCnP8FClKibCIr0e4CYN_sjNrX_CLTwiZzBOgIy1qhQ_7T_Fc3x5je8GQFSozFtn_uOrx5HU0DEywIGS2sW438_
from rst_fast_parse.block_parsers.fallback import gAAAAABmoAOUWQNakEHu6VVR1xw2IM_RHB0aoNAjL6OeRo6n9hjxd_f__pS_JPD3oUtjUB_TgvoOF8TodNhD_SImYEfBCUZQow__
from rst_fast_parse.block_parsers.field_list import gAAAAABmoAOUZjsSJcesqBytvjPkKU00tyN9SLYIUcDS_1xHu9RxOUNXHiT2_ZmBSShFX9ByOP_FXqlBvFWtR7wF613QWYafcr4fv6OPocV3czXP_SV7Ixg_
from rst_fast_parse.block_parsers.line_block import gAAAAABmoAOU7FBoEtfAkDxv_AOuAF96dSZwDu2kp28qAk_0JfXa8Bjon0IvzZ4cCZhvrIFuCRw9xf2AxTV892wsrFOqg3WNG2_CNhy0vfPRr5PWvBhhUew_
from rst_fast_parse.block_parsers.line_marker import gAAAAABmoAOU1OoaNIizXqjMefySkYO0CraHXhJhU6Nu9yLMPoTP6_nsYsAvnD_fvLkLjTIA6o1KBO4F7E93RuWN2KLgH2mtmdbItTMFDwJN7LWeiZ0Nyyk_
from rst_fast_parse.block_parsers.option_list import gAAAAABmoAOU_9mEt6f3Vo_agyuFsQUPBw_K0gS5XjzokJMByoEX9scjHf9pPH1CA9hi123GYdazWnfHg8am8D2__1JQKjlg_xoMZwQ793Z2MqPgj4ISZSg_
from rst_fast_parse.block_parsers.table_grid import gAAAAABmoAOUvhXviP6MwP6BRjd7oBNRsNUvTYEojfGs6J9_JZ_jEMxTqf8e30AsOjnlfjCcbSwQPFn4A1Cz0K8O3H9_WbrtaDAKRvFuqzILmmRy04Hrw_c_
from rst_fast_parse.block_parsers.table_simple import gAAAAABmoAOUxHZm8H8WBfrmeD6C0x_TC0hh2dSkF2c7NPV57iT2yKKWGeZQ0AeP4sXZhIwttTG1ruMQKWbKMVp95_vaO1txL9hqX34O4br4hUEZy5M6HHU_
from rst_fast_parse.core import gAAAAABmoAOUfiH_lyjWdxZJ5wlAftyDtjBMg7EIPu0ttw_12czCT5w4P6O_6c1oedfwJ1cVjQEdVc2t7WUqh2h25_xi_VDW0g__, gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__
from rst_fast_parse.elements import ElementListBase
from rst_fast_parse.source import gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__, gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__

_DEFAULT_BLOCK_PARSERS: tuple[gAAAAABmoAOUfiH_lyjWdxZJ5wlAftyDtjBMg7EIPu0ttw_12czCT5w4P6O_6c1oedfwJ1cVjQEdVc2t7WUqh2h25_xi_VDW0g__, ...] = (
    gAAAAABmoAOUuA3eBv2vGYZEJW3gUA__kHl9WdI_mduoNY_Ht2iQF9yGIMuFRFkHXd5dBFP463DRCSNgDoChCZ_0uG2b_BYVw_Pm7yf3Rn61Uit28bg58jQ_,
    gAAAAABmoAOU2G7JntteCshsuyI4pWZw6iMjANa3_pzgo1J8Co7OzylVHtFXNIVgQ_csrfcK8kHC4XUhPZHVKaSvDTC7ocwSegqdSqGth87n_vogaoqFbKk_,
    gAAAAABmoAOUbB2ETvLyPxSGayUepPIJ2Iyw96wikvNkX7K3uV9hI4LUA86whDK6xWR2rJsP2UkPcObXM1_k0nHnmQA4Gl9lFG4evEOZVDDEf3UvvQDNTWY_,
    gAAAAABmoAOUWMukC3xWibby_gWTQjsrg2NXLqBXikahSkcMtU0pJKKOwRPgbuPIdRz0W6_1AQswYpCc7yFZSoCfC251hVSr1K_9Vv9LYIVv1HbvaL2LHNE_,
    gAAAAABmoAOUZjsSJcesqBytvjPkKU00tyN9SLYIUcDS_1xHu9RxOUNXHiT2_ZmBSShFX9ByOP_FXqlBvFWtR7wF613QWYafcr4fv6OPocV3czXP_SV7Ixg_,
    gAAAAABmoAOU_9mEt6f3Vo_agyuFsQUPBw_K0gS5XjzokJMByoEX9scjHf9pPH1CA9hi123GYdazWnfHg8am8D2__1JQKjlg_xoMZwQ793Z2MqPgj4ISZSg_,
    gAAAAABmoAOUZqQfhhAZAhzc4__Ty8_8jWBJrjudf6dyUZiRHOLpRncezITssQx0qwNf3HfQm8UvcEAW_Kmn9yIy3lKoptA_SVXZBo_qXmNQdQhnh0_tSts_,
    gAAAAABmoAOU7FBoEtfAkDxv_AOuAF96dSZwDu2kp28qAk_0JfXa8Bjon0IvzZ4cCZhvrIFuCRw9xf2AxTV892wsrFOqg3WNG2_CNhy0vfPRr5PWvBhhUew_,
    gAAAAABmoAOUvhXviP6MwP6BRjd7oBNRsNUvTYEojfGs6J9_JZ_jEMxTqf8e30AsOjnlfjCcbSwQPFn4A1Cz0K8O3H9_WbrtaDAKRvFuqzILmmRy04Hrw_c_,
    gAAAAABmoAOUxHZm8H8WBfrmeD6C0x_TC0hh2dSkF2c7NPV57iT2yKKWGeZQ0AeP4sXZhIwttTG1ruMQKWbKMVp95_vaO1txL9hqX34O4br4hUEZy5M6HHU_,
    gAAAAABmoAOU8iBQud1CGsfVwOoqEIQVvKCnP8FClKibCIr0e4CYN_sjNrX_CLTwiZzBOgIy1qhQ_7T_Fc3x5je8GQFSozFtn_uOrx5HU0DEywIGS2sW438_,
    gAAAAABmoAOUKR0M0HScNoUePVIKWWUNrP_POPvERE6Qy9GhSMeH07QgwNUnzQrZb_lJU5cI0zyebH_BJLRiHwwCYByjNpLzjC3KEhC8uxTsUKUF3LqSZF8_,
    gAAAAABmoAOU1OoaNIizXqjMefySkYO0CraHXhJhU6Nu9yLMPoTP6_nsYsAvnD_fvLkLjTIA6o1KBO4F7E93RuWN2KLgH2mtmdbItTMFDwJN7LWeiZ0Nyyk_,
    gAAAAABmoAOUWQNakEHu6VVR1xw2IM_RHB0aoNAjL6OeRo6n9hjxd_f__pS_JPD3oUtjUB_TgvoOF8TodNhD_SImYEfBCUZQow__,
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
    context = gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__(_DEFAULT_BLOCK_PARSERS)
    lines = _sanitize_string(text, tab_width=tab_width)
    slice = gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__(
        [
            gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__(line, offset_line=i, offset_char=offset_char, source=source_key)
            for i, line in enumerate(lines)
        ]
    )
    return context.gAAAAABmoAOU8__0t7BI16YsaaDAfcl_VGzWDDVJskTG6kYt2ZE2FDW9TUgSsIlhe_f_yonSniOMZrvMxSABmNEbkfrGSuVZxg__(slice)
