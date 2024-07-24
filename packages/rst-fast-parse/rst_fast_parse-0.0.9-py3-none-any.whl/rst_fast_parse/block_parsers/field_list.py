from __future__ import annotations
import re
from typing import Generator
from rst_fast_parse.core import gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_, gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__
from rst_fast_parse.elements import ElementListBase, ListElement, ListItemElement
from rst_fast_parse.regexes.block import gAAAAABmoAOU3RVvo3YkzKhGKWCu8fKyuDtctqPSjiVzXO1JaMBXt0uqZpqYc1q1N6ZBumHojK1ZpxK0ChcZlgnozjyDbWAvOA__
from rst_fast_parse.source import PositiveInt, gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__

def gAAAAABmoAOUZjsSJcesqBytvjPkKU00tyN9SLYIUcDS_1xHu9RxOUNXHiT2_ZmBSShFX9ByOP_FXqlBvFWtR7wF613QWYafcr4fv6OPocV3czXP_SV7Ixg_(source: gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__, parent: ElementListBase, context: gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__, /) -> gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_:
    if not (_current_line := source.current_line):
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUjd_6MxHjEtt1TugiZ6yaacbq1nREHVx2Fk2T_2621FG1CjXnhtaIU_bVoJ1U7KN1_WjYt6NyPEGMdldCcwNscQ__
    if not (_ := re.match(gAAAAABmoAOU3RVvo3YkzKhGKWCu8fKyuDtctqPSjiVzXO1JaMBXt0uqZpqYc1q1N6ZBumHojK1ZpxK0ChcZlgnozjyDbWAvOA__, _current_line.content)):
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUproF_iscOFcDNKNx2ui84_7alGaIdXM1oeGJa_ugCTaycwn7oF_8z7vOlFa_DGDwPP5T44koPx_ElivNotdd7A__
    items: list[ListItemElement] = []
    for name, content in gAAAAABmoAOUnLLIjOD5rCqS6ejdfj_1BEeAK7CNsUVE34AXlDe2a9poZoWZmfk6_TpSlTeoqHy7HIPwx_tt3F9_EPcSOfjFa4N7aeAXxc152FCHnX_6VOQ_(source):
        if name.current_line:
            list_item = ListItemElement((name.current_line.line, name.current_line.line if content.last_line is None else content.last_line.line))
            items.append(list_item)
            context.gAAAAABmoAOUjwOEnh8OvcV78z8zUYoqJJ0Y2TrThUDOYQObmZ9KKZuVx0fs2RHsOQai0Er2b51fz7_55XcSDLfrKPsEXT3Abw__(content, list_item)
    if items:
        parent.append(ListElement('field_list', items))
    return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__

def gAAAAABmoAOUnLLIjOD5rCqS6ejdfj_1BEeAK7CNsUVE34AXlDe2a9poZoWZmfk6_TpSlTeoqHy7HIPwx_tt3F9_EPcSOfjFa4N7aeAXxc152FCHnX_6VOQ_(source: gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__, /) -> Generator[tuple[gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__, gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__], None, None]:
    while (current_line := source.current_line):
        if current_line.is_blank:
            source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__()
            continue
        if (match := re.match(gAAAAABmoAOU3RVvo3YkzKhGKWCu8fKyuDtctqPSjiVzXO1JaMBXt0uqZpqYc1q1N6ZBumHojK1ZpxK0ChcZlgnozjyDbWAvOA__, current_line.content)):
            name_slice = current_line.gAAAAABmoAOUVJk0OIgrX4tQstRTR65UTKPvmwUSZ2Uor8BBWPSatShHksNnwnCg_VKVzOAQcp8QPG796Bw7EPgnzy0_USnYFw__(PositiveInt(match.start(1)), PositiveInt(match.end(1))).gAAAAABmoAOU_Dgn29ePOZICyelpAflzeMzC3issyPc5lnfrhTyTNMUXRLRT0utnzBk0Ek8TDmL22bUcweJUf_XSY0WwZ0eMDw__()
            body_slice = source.gAAAAABmoAOUrqn_gdTR2OA_oxNqRDfXHdf_AoAj9pIcLZiZCzUC1qCoNCI3jgHyx6fa_OrI5HWOaRLsSVT_EGSzmy5ld108GoCSb3jWHLN0wWbNcgb_f10_(first_indent=match.end(0), advance=True)
            yield (name_slice, body_slice)
            source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__()
        else:
            source.gAAAAABmoAOUXBPdo9OkaxYoAc4gGo8fBfuw88NaQvW9F6dJXeOAGnTz4uetdGLdeffAFTTUljLpCo2l_WvJvzJc40wY5KLzCg__()
            break