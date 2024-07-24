from __future__ import annotations
import re
from rst_fast_parse.block_parsers.fallback import gAAAAABmoAOUWQNakEHu6VVR1xw2IM_RHB0aoNAjL6OeRo6n9hjxd_f__pS_JPD3oUtjUB_TgvoOF8TodNhD_SImYEfBCUZQow__
from rst_fast_parse.core import gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_, gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__
from rst_fast_parse.elements import ElementListBase, TitleElement, TransitionElement
from rst_fast_parse.regexes.block import gAAAAABmoAOUNEZRwDi3WbtiZvOsdXXjLo1GOTAM7lk6EnQU8a1J07dFSBAGxty05qt97c5VjiucLY83azKMVO_cKNtfWxWklaN8vDTXPX2fznNswY6SGvM_
from rst_fast_parse.source import gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__, gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__
from rst_fast_parse.utils.column_widths import gAAAAABmoAOUdlj0PfNg4w4pJaxFAjHMB9z9jpZUSmkB101ROIEkW_y_TnWHUsEby6Z9CVvMVPDk8mQ1QthKul0gQBwS0iyKUQ__

def gAAAAABmoAOU1OoaNIizXqjMefySkYO0CraHXhJhU6Nu9yLMPoTP6_nsYsAvnD_fvLkLjTIA6o1KBO4F7E93RuWN2KLgH2mtmdbItTMFDwJN7LWeiZ0Nyyk_(source: gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__, parent: ElementListBase, context: gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__, /) -> gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_:
    if not (current_line := source.current_line):
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUjd_6MxHjEtt1TugiZ6yaacbq1nREHVx2Fk2T_2621FG1CjXnhtaIU_bVoJ1U7KN1_WjYt6NyPEGMdldCcwNscQ__
    if not (match := re.match(gAAAAABmoAOUNEZRwDi3WbtiZvOsdXXjLo1GOTAM7lk6EnQU8a1J07dFSBAGxty05qt97c5VjiucLY83azKMVO_cKNtfWxWklaN8vDTXPX2fznNswY6SGvM_, current_line.content)):
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUproF_iscOFcDNKNx2ui84_7alGaIdXM1oeGJa_ugCTaycwn7oF_8z7vOlFa_DGDwPP5T44koPx_ElivNotdd7A__
    marker = match.string.strip()
    marker_char = marker[0]
    marker_length = len(marker)
    min_marker_length = 4
    if not context.allow_titles:
        if marker == '::':
            return gAAAAABmoAOUWQNakEHu6VVR1xw2IM_RHB0aoNAjL6OeRo6n9hjxd_f__pS_JPD3oUtjUB_TgvoOF8TodNhD_SImYEfBCUZQow__(source, parent, context)
        if marker_length < min_marker_length:
            return gAAAAABmoAOUWQNakEHu6VVR1xw2IM_RHB0aoNAjL6OeRo6n9hjxd_f__pS_JPD3oUtjUB_TgvoOF8TodNhD_SImYEfBCUZQow__(source, parent, context)
        parent.append(gAAAAABmoAOUn68m6f3sRzRQP4nouxubieadxaH8gCrjBJsafZ9jokHAa0sbJb9BwDpcxKaFgrpXVjGkR1rlBmO8c30swdUkzA__(marker_char, current_line))
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__
    next_line = source.gAAAAABmoAOU4MROUYia9kJe75WM4gcw9LvrTZXAqyYK7_Ax0bicP68Y_yrusuxyIyyGjE_JLwwpuAjWfnUpxSISbSe_h_y4IQ__()
    if next_line is None or next_line.is_blank:
        if marker_length < min_marker_length:
            return gAAAAABmoAOUWQNakEHu6VVR1xw2IM_RHB0aoNAjL6OeRo6n9hjxd_f__pS_JPD3oUtjUB_TgvoOF8TodNhD_SImYEfBCUZQow__(source, parent, context)
        parent.append(gAAAAABmoAOUn68m6f3sRzRQP4nouxubieadxaH8gCrjBJsafZ9jokHAa0sbJb9BwDpcxKaFgrpXVjGkR1rlBmO8c30swdUkzA__(marker_char, current_line))
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__
    if re.match(gAAAAABmoAOUNEZRwDi3WbtiZvOsdXXjLo1GOTAM7lk6EnQU8a1J07dFSBAGxty05qt97c5VjiucLY83azKMVO_cKNtfWxWklaN8vDTXPX2fznNswY6SGvM_, next_line.content):
        if marker_length < min_marker_length:
            return gAAAAABmoAOUWQNakEHu6VVR1xw2IM_RHB0aoNAjL6OeRo6n9hjxd_f__pS_JPD3oUtjUB_TgvoOF8TodNhD_SImYEfBCUZQow__(source, parent, context)
        parent.append(gAAAAABmoAOUn68m6f3sRzRQP4nouxubieadxaH8gCrjBJsafZ9jokHAa0sbJb9BwDpcxKaFgrpXVjGkR1rlBmO8c30swdUkzA__(marker_char, current_line))
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__
    next_next_line = source.gAAAAABmoAOU4MROUYia9kJe75WM4gcw9LvrTZXAqyYK7_Ax0bicP68Y_yrusuxyIyyGjE_JLwwpuAjWfnUpxSISbSe_h_y4IQ__(2)
    if next_next_line is None:
        if marker_length < min_marker_length:
            return gAAAAABmoAOUWQNakEHu6VVR1xw2IM_RHB0aoNAjL6OeRo6n9hjxd_f__pS_JPD3oUtjUB_TgvoOF8TodNhD_SImYEfBCUZQow__(source, parent, context)
        parent.append(gAAAAABmoAOUn68m6f3sRzRQP4nouxubieadxaH8gCrjBJsafZ9jokHAa0sbJb9BwDpcxKaFgrpXVjGkR1rlBmO8c30swdUkzA__(marker_char, current_line))
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__
    if (underline_match := re.match(gAAAAABmoAOUNEZRwDi3WbtiZvOsdXXjLo1GOTAM7lk6EnQU8a1J07dFSBAGxty05qt97c5VjiucLY83azKMVO_cKNtfWxWklaN8vDTXPX2fznNswY6SGvM_, next_next_line.content)) is None:
        if marker_length < min_marker_length:
            return gAAAAABmoAOUWQNakEHu6VVR1xw2IM_RHB0aoNAjL6OeRo6n9hjxd_f__pS_JPD3oUtjUB_TgvoOF8TodNhD_SImYEfBCUZQow__(source, parent, context)
        parent.append(gAAAAABmoAOUn68m6f3sRzRQP4nouxubieadxaH8gCrjBJsafZ9jokHAa0sbJb9BwDpcxKaFgrpXVjGkR1rlBmO8c30swdUkzA__(marker_char, current_line))
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__
    underline = underline_match.string.rstrip()
    if marker != underline:
        if marker_length < min_marker_length:
            return gAAAAABmoAOUWQNakEHu6VVR1xw2IM_RHB0aoNAjL6OeRo6n9hjxd_f__pS_JPD3oUtjUB_TgvoOF8TodNhD_SImYEfBCUZQow__(source, parent, context)
        parent.append(gAAAAABmoAOUn68m6f3sRzRQP4nouxubieadxaH8gCrjBJsafZ9jokHAa0sbJb9BwDpcxKaFgrpXVjGkR1rlBmO8c30swdUkzA__(marker_char, current_line))
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__
    title = next_line.content.rstrip()
    if gAAAAABmoAOUdlj0PfNg4w4pJaxFAjHMB9z9jpZUSmkB101ROIEkW_y_TnWHUsEby6Z9CVvMVPDk8mQ1QthKul0gQBwS0iyKUQ__(title) > marker_length:
        if marker_length < min_marker_length:
            return gAAAAABmoAOUWQNakEHu6VVR1xw2IM_RHB0aoNAjL6OeRo6n9hjxd_f__pS_JPD3oUtjUB_TgvoOF8TodNhD_SImYEfBCUZQow__(source, parent, context)
    source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__(2)
    parent.append(TitleElement(True, marker[0], title, (current_line.line, next_next_line.line)))
    return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__

def gAAAAABmoAOUn68m6f3sRzRQP4nouxubieadxaH8gCrjBJsafZ9jokHAa0sbJb9BwDpcxKaFgrpXVjGkR1rlBmO8c30swdUkzA__(style: str, line: gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__) -> TransitionElement:
    return TransitionElement(style, (line.line, line.line))