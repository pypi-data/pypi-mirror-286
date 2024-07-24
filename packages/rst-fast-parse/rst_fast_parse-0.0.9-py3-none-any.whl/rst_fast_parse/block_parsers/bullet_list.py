from __future__ import annotations
import re
from rst_fast_parse.core import gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_, gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__
from rst_fast_parse.elements import ElementListBase, ListElement, ListItemElement
from rst_fast_parse.regexes.block import gAAAAABmoAOU5xOHdrDyYmDJK0ra0tYd9mNKR7zkMQC2aOKQWzW0JSUHs3YRVMJXD6LZxEBztjGg3qTNnlBXC6EBFWo52OVhP9Eu6Lq24jl8dXXbGxy_oRs_
from rst_fast_parse.source import gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__

def gAAAAABmoAOUbB2ETvLyPxSGayUepPIJ2Iyw96wikvNkX7K3uV9hI4LUA86whDK6xWR2rJsP2UkPcObXM1_k0nHnmQA4Gl9lFG4evEOZVDDEf3UvvQDNTWY_(source: gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__, parent: ElementListBase, context: gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__, /) -> gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_:
    if not (first_line := source.current_line):
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUjd_6MxHjEtt1TugiZ6yaacbq1nREHVx2Fk2T_2621FG1CjXnhtaIU_bVoJ1U7KN1_WjYt6NyPEGMdldCcwNscQ__
    if not (match := re.match(gAAAAABmoAOU5xOHdrDyYmDJK0ra0tYd9mNKR7zkMQC2aOKQWzW0JSUHs3YRVMJXD6LZxEBztjGg3qTNnlBXC6EBFWo52OVhP9Eu6Lq24jl8dXXbGxy_oRs_, first_line.content)):
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUproF_iscOFcDNKNx2ui84_7alGaIdXM1oeGJa_ugCTaycwn7oF_8z7vOlFa_DGDwPP5T44koPx_ElivNotdd7A__
    symbol: str = match.group(1)
    items: list[ListItemElement] = []
    while (current_line := source.current_line):
        if current_line.is_blank:
            source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__()
            continue
        if (match := re.match(gAAAAABmoAOU5xOHdrDyYmDJK0ra0tYd9mNKR7zkMQC2aOKQWzW0JSUHs3YRVMJXD6LZxEBztjGg3qTNnlBXC6EBFWo52OVhP9Eu6Lq24jl8dXXbGxy_oRs_, current_line.content)):
            next_symbol: str = match.group(1)
            if next_symbol != symbol:
                source.gAAAAABmoAOUXBPdo9OkaxYoAc4gGo8fBfuw88NaQvW9F6dJXeOAGnTz4uetdGLdeffAFTTUljLpCo2l_WvJvzJc40wY5KLzCg__()
                break
            first_indent = match.end(0)
            if len(current_line.content) > first_indent:
                content = source.gAAAAABmoAOUs2F_NH1Cb00_oxoXB1TsXtVTVkPYZAHFgA4IyJNmDri28ayNie1nOhlRWjfnUiynPZjRIPY_BJVs29L0xnbPz8e1uLfnnr_lJuL8qmYpNMM_(first_indent, always_first=True, advance=True)
            else:
                content = source.gAAAAABmoAOUrqn_gdTR2OA_oxNqRDfXHdf_AoAj9pIcLZiZCzUC1qCoNCI3jgHyx6fa_OrI5HWOaRLsSVT_EGSzmy5ld108GoCSb3jWHLN0wWbNcgb_f10_(first_indent=first_indent, advance=True)
            list_item = ListItemElement((current_line.line, current_line.line if content.last_line is None else content.last_line.line))
            items.append(list_item)
            context.gAAAAABmoAOUjwOEnh8OvcV78z8zUYoqJJ0Y2TrThUDOYQObmZ9KKZuVx0fs2RHsOQai0Er2b51fz7_55XcSDLfrKPsEXT3Abw__(content, list_item)
            source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__()
        else:
            source.gAAAAABmoAOUXBPdo9OkaxYoAc4gGo8fBfuw88NaQvW9F6dJXeOAGnTz4uetdGLdeffAFTTUljLpCo2l_WvJvzJc40wY5KLzCg__()
            break
    if items:
        parent.append(ListElement('bullet_list', items))
    return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__