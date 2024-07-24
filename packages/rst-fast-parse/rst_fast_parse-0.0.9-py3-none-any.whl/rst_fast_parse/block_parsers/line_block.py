import re
from rst_fast_parse.core import gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_, gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__
from rst_fast_parse.elements import ElementListBase, ListElement, ListItemElement
from rst_fast_parse.regexes.block import gAAAAABmoAOUnHqpLJJqsKu6nt3jao4Sb8SXBJi2UyO8DQBREvsF8PtbY_4nAG8RugxGsr7H9iRaFQk5pbMA_UIemHaUJFOFEA__
from rst_fast_parse.source import gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__

def gAAAAABmoAOU7FBoEtfAkDxv_AOuAF96dSZwDu2kp28qAk_0JfXa8Bjon0IvzZ4cCZhvrIFuCRw9xf2AxTV892wsrFOqg3WNG2_CNhy0vfPRr5PWvBhhUew_(source: gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__, parent: ElementListBase, _context: gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__, /) -> gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_:
    if not (_current_line := source.current_line):
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUjd_6MxHjEtt1TugiZ6yaacbq1nREHVx2Fk2T_2621FG1CjXnhtaIU_bVoJ1U7KN1_WjYt6NyPEGMdldCcwNscQ__
    if not (_ := re.match(gAAAAABmoAOUnHqpLJJqsKu6nt3jao4Sb8SXBJi2UyO8DQBREvsF8PtbY_4nAG8RugxGsr7H9iRaFQk5pbMA_UIemHaUJFOFEA__, _current_line.content)):
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUproF_iscOFcDNKNx2ui84_7alGaIdXM1oeGJa_ugCTaycwn7oF_8z7vOlFa_DGDwPP5T44koPx_ElivNotdd7A__
    items: list[ListItemElement] = []
    while (current_line := source.current_line):
        if (match := re.match(gAAAAABmoAOUnHqpLJJqsKu6nt3jao4Sb8SXBJi2UyO8DQBREvsF8PtbY_4nAG8RugxGsr7H9iRaFQk5pbMA_UIemHaUJFOFEA__, current_line.content)):
            indent_length = match.end(0)
            content = source.gAAAAABmoAOUrqn_gdTR2OA_oxNqRDfXHdf_AoAj9pIcLZiZCzUC1qCoNCI3jgHyx6fa_OrI5HWOaRLsSVT_EGSzmy5ld108GoCSb3jWHLN0wWbNcgb_f10_(first_indent=indent_length, until_blank=True, advance=True)
            list_item = ListItemElement((current_line.line, current_line.line if content.last_line is None else content.last_line.line))
            items.append(list_item)
            source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__()
        else:
            source.gAAAAABmoAOUXBPdo9OkaxYoAc4gGo8fBfuw88NaQvW9F6dJXeOAGnTz4uetdGLdeffAFTTUljLpCo2l_WvJvzJc40wY5KLzCg__()
            break
    if items:
        parent.append(ListElement('line_block', items))
    return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__