from __future__ import annotations
import re
from rst_fast_parse.block_parsers.fallback import gAAAAABmoAOUWQNakEHu6VVR1xw2IM_RHB0aoNAjL6OeRo6n9hjxd_f__pS_JPD3oUtjUB_TgvoOF8TodNhD_SImYEfBCUZQow__
from rst_fast_parse.core import gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_, gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__
from rst_fast_parse.elements import ElementListBase, ListElement, ListItemElement
from rst_fast_parse.regexes.block import gAAAAABmoAOUciGbPWHH9cixuJIUoTSQv36k_oLO1fWRvprvdfidJmkqFfVgSzXcIB3CFvt5ZyJz8wmv1JPj0djcKmyp2ZdQHLv8QM1d9PeY9dZhVwTUzaM_
from rst_fast_parse.source import gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__

def gAAAAABmoAOU_9mEt6f3Vo_agyuFsQUPBw_K0gS5XjzokJMByoEX9scjHf9pPH1CA9hi123GYdazWnfHg8am8D2__1JQKjlg_xoMZwQ793Z2MqPgj4ISZSg_(source: gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__, parent: ElementListBase, context: gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__, /) -> gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_:
    if not (_current_line := source.current_line):
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUjd_6MxHjEtt1TugiZ6yaacbq1nREHVx2Fk2T_2621FG1CjXnhtaIU_bVoJ1U7KN1_WjYt6NyPEGMdldCcwNscQ__
    if not (_ := re.match(gAAAAABmoAOUciGbPWHH9cixuJIUoTSQv36k_oLO1fWRvprvdfidJmkqFfVgSzXcIB3CFvt5ZyJz8wmv1JPj0djcKmyp2ZdQHLv8QM1d9PeY9dZhVwTUzaM_, _current_line.content)):
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUproF_iscOFcDNKNx2ui84_7alGaIdXM1oeGJa_ugCTaycwn7oF_8z7vOlFa_DGDwPP5T44koPx_ElivNotdd7A__
    items: list[ListItemElement] = []
    while (current_line := source.current_line):
        if current_line.is_blank:
            source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__()
            continue
        if (match := re.match(gAAAAABmoAOUciGbPWHH9cixuJIUoTSQv36k_oLO1fWRvprvdfidJmkqFfVgSzXcIB3CFvt5ZyJz8wmv1JPj0djcKmyp2ZdQHLv8QM1d9PeY9dZhVwTUzaM_, current_line.content)):
            initial_index = source.current_index
            content = source.gAAAAABmoAOUrqn_gdTR2OA_oxNqRDfXHdf_AoAj9pIcLZiZCzUC1qCoNCI3jgHyx6fa_OrI5HWOaRLsSVT_EGSzmy5ld108GoCSb3jWHLN0wWbNcgb_f10_(first_indent=match.end(0), advance=True)
            if not content.gAAAAABmoAOUR6KFT3ZpMWAeD51IwZzREeQge_XjmY_K_zJWSp4ADn2Md7XN8XCmYBBmmsiQQjdzWBx8hoIhu5ufMxt4pQQogQ__():
                source.gAAAAABmoAOUiHCs3LCinJOYERnH6vPz6qCUT6D4eKdPi_bc1mJqXbmvDmMGZ0suTJYBnkPu8eitfxw8k9edq4_ryrTa7KXfE_XlXfPc_uK_dLILFBGi0b8_(initial_index)
                if items:
                    parent.append(ListElement('option_list', items))
                return gAAAAABmoAOUWQNakEHu6VVR1xw2IM_RHB0aoNAjL6OeRo6n9hjxd_f__pS_JPD3oUtjUB_TgvoOF8TodNhD_SImYEfBCUZQow__(source, parent, context)
            list_item = ListItemElement((current_line.line, current_line.line if content.last_line is None else content.last_line.line))
            items.append(list_item)
            context.gAAAAABmoAOUjwOEnh8OvcV78z8zUYoqJJ0Y2TrThUDOYQObmZ9KKZuVx0fs2RHsOQai0Er2b51fz7_55XcSDLfrKPsEXT3Abw__(content, list_item)
            source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__()
        else:
            source.gAAAAABmoAOUXBPdo9OkaxYoAc4gGo8fBfuw88NaQvW9F6dJXeOAGnTz4uetdGLdeffAFTTUljLpCo2l_WvJvzJc40wY5KLzCg__()
            break
    if items:
        parent.append(ListElement('option_list', items))
    return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__