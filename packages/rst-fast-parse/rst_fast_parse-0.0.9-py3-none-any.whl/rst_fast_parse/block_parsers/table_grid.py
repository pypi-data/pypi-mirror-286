from __future__ import annotations
import re
from rst_fast_parse.core import gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_, gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__
from rst_fast_parse.elements import BasicElement, ElementListBase
from rst_fast_parse.regexes.block import gAAAAABmoAOU_1XQzzQOe2tRhJLsdE1d00g3b2qaZ3_p_BolpWq5SaL9wQSSceZ4TUFIMtPA9SLfKWicuVuqWO4sdQpzXLghXg__
from rst_fast_parse.source import gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__, gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__

def gAAAAABmoAOUvhXviP6MwP6BRjd7oBNRsNUvTYEojfGs6J9_JZ_jEMxTqf8e30AsOjnlfjCcbSwQPFn4A1Cz0K8O3H9_WbrtaDAKRvFuqzILmmRy04Hrw_c_(source: gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__, parent: ElementListBase, context: gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__, /) -> gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_:
    if not (_current_line := source.current_line):
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUjd_6MxHjEtt1TugiZ6yaacbq1nREHVx2Fk2T_2621FG1CjXnhtaIU_bVoJ1U7KN1_WjYt6NyPEGMdldCcwNscQ__
    if not re.match(gAAAAABmoAOU_1XQzzQOe2tRhJLsdE1d00g3b2qaZ3_p_BolpWq5SaL9wQSSceZ4TUFIMtPA9SLfKWicuVuqWO4sdQpzXLghXg__, _current_line.content):
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUproF_iscOFcDNKNx2ui84_7alGaIdXM1oeGJa_ugCTaycwn7oF_8z7vOlFa_DGDwPP5T44koPx_ElivNotdd7A__
    if not (table_slice := gAAAAABmoAOU8fZu_13wNV5hZHlCicppjuUoVtqMQ27wCccTb6c_EqSeBpmHeg88x_AOn5NeeZ09DxO0TRXrFTjDON9k1ATciVCMzaDmTMpLKTxd7jyC990_(source)):
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__
    if (first := table_slice.current_line) and (last := table_slice.last_line):
        parent.append(BasicElement('table_grid', (first.line, last.line)))
    return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__

def gAAAAABmoAOU8fZu_13wNV5hZHlCicppjuUoVtqMQ27wCccTb6c_EqSeBpmHeg88x_AOn5NeeZ09DxO0TRXrFTjDON9k1ATciVCMzaDmTMpLKTxd7jyC990_(source: gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__) -> None | gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__:
    original_source_index = source.current_index
    block = source.gAAAAABmoAOUCk1aQjjQn3Z4dYapsn0HEEIQzzpDFIExvv7dM8dGC_YER09iQNX9sf3o7i2vxISlwC42982fos9FLp9kXH7l_g__(stop_on_indented=True, advance=True)
    if not (first_line := block.current_line):
        return None
    lines: list[gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__] = []
    for line in block.gAAAAABmoAOUzG1EvfQyN5BmSdkjUtgO9Qiz4G3soPbw063G_By2oLrYiaGZXCXPJ9TJ27fbJVmN8fNEHILDFeNYKwjikdN5jA__():
        if not (line.content.startswith('+') or line.content.startswith('|')):
            source.gAAAAABmoAOUiHCs3LCinJOYERnH6vPz6qCUT6D4eKdPi_bc1mJqXbmvDmMGZ0suTJYBnkPu8eitfxw8k9edq4_ryrTa7KXfE_XlXfPc_uK_dLILFBGi0b8_(original_source_index + len(lines) - 1)
            break
        lines.append(line.rstrip())
    if not re.match(gAAAAABmoAOU_1XQzzQOe2tRhJLsdE1d00g3b2qaZ3_p_BolpWq5SaL9wQSSceZ4TUFIMtPA9SLfKWicuVuqWO4sdQpzXLghXg__, lines[-1].content):
        for i in range(len(lines) - 2, 1, -1):
            if re.match(gAAAAABmoAOU_1XQzzQOe2tRhJLsdE1d00g3b2qaZ3_p_BolpWq5SaL9wQSSceZ4TUFIMtPA9SLfKWicuVuqWO4sdQpzXLghXg__, lines[i].content):
                del lines[i + 1:]
                source.gAAAAABmoAOUiHCs3LCinJOYERnH6vPz6qCUT6D4eKdPi_bc1mJqXbmvDmMGZ0suTJYBnkPu8eitfxw8k9edq4_ryrTa7KXfE_XlXfPc_uK_dLILFBGi0b8_(original_source_index + len(lines) - 2)
                break
        else:
            return None
    width = len(first_line.content.rstrip())
    for line in lines:
        if len(line.content) != width:
            return None
        if not (line.content.endswith('+') or line.content.endswith('|')):
            return None
    return gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__(lines)