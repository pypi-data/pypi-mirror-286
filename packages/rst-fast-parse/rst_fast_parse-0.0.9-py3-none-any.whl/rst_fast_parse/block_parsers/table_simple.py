from __future__ import annotations
import re
from rst_fast_parse.core import gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_, gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__
from rst_fast_parse.elements import BasicElement, ElementListBase
from rst_fast_parse.regexes.block import gAAAAABmoAOU11e3jgf8NDs2Qjnelo_NFgqMrakhTNV_4uMiSvum0pcQGEt_lgTtgFM_vAnUdCJ5_7WMRIHAVLbunQiBbLMk0A__, gAAAAABmoAOUx3tEUa5u1i7YSbZuBg1UGUb8M1QevEPCFw_uMF2lxY3ZYewi2VSJWI6UvS_NIOiySsfltH5JKGjGEBDSf_J1pBn6XbDtEtY9DmL1q0MORUc_
from rst_fast_parse.source import gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__

def gAAAAABmoAOUxHZm8H8WBfrmeD6C0x_TC0hh2dSkF2c7NPV57iT2yKKWGeZQ0AeP4sXZhIwttTG1ruMQKWbKMVp95_vaO1txL9hqX34O4br4hUEZy5M6HHU_(source: gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__, parent: ElementListBase, context: gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__, /) -> gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_:
    if not (_current_line := source.current_line):
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUjd_6MxHjEtt1TugiZ6yaacbq1nREHVx2Fk2T_2621FG1CjXnhtaIU_bVoJ1U7KN1_WjYt6NyPEGMdldCcwNscQ__
    if not re.match(gAAAAABmoAOU11e3jgf8NDs2Qjnelo_NFgqMrakhTNV_4uMiSvum0pcQGEt_lgTtgFM_vAnUdCJ5_7WMRIHAVLbunQiBbLMk0A__, _current_line.content):
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUproF_iscOFcDNKNx2ui84_7alGaIdXM1oeGJa_ugCTaycwn7oF_8z7vOlFa_DGDwPP5T44koPx_ElivNotdd7A__
    if not (table_slice := gAAAAABmoAOUf_j3GzfUF1QyP_ibZy_bFOg6NOL7PVVnoI6_URlvFfSN2mCALZRKz47CMdceldX1Zj_NLcHt8X95tnafsRM4LppFxXLJfBWzja3qZzn4aL0_(source)):
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__
    if (first := table_slice.current_line) and (last := table_slice.last_line):
        parent.append(BasicElement('table_simple', (first.line, last.line)))
    return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__

def gAAAAABmoAOUf_j3GzfUF1QyP_ibZy_bFOg6NOL7PVVnoI6_URlvFfSN2mCALZRKz47CMdceldX1Zj_NLcHt8X95tnafsRM4LppFxXLJfBWzja3qZzn4aL0_(source: gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__) -> None | gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__:
    if not (first_line := source.current_line):
        return None
    toplen = len(first_line.content.strip())
    borders_found: int = 0
    peek_offset = 1
    last_border_offset: None | int = None
    while (line := source.gAAAAABmoAOU4MROUYia9kJe75WM4gcw9LvrTZXAqyYK7_Ax0bicP68Y_yrusuxyIyyGjE_JLwwpuAjWfnUpxSISbSe_h_y4IQ__(peek_offset)):
        if re.match(gAAAAABmoAOUx3tEUa5u1i7YSbZuBg1UGUb8M1QevEPCFw_uMF2lxY3ZYewi2VSJWI6UvS_NIOiySsfltH5JKGjGEBDSf_J1pBn6XbDtEtY9DmL1q0MORUc_, line.content):
            if len(line.content.strip()) != toplen:
                source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__(peek_offset)
                return None
            borders_found += 1
            last_border_offset = peek_offset
            if borders_found == 2 or not (next_line := source.gAAAAABmoAOU4MROUYia9kJe75WM4gcw9LvrTZXAqyYK7_Ax0bicP68Y_yrusuxyIyyGjE_JLwwpuAjWfnUpxSISbSe_h_y4IQ__(peek_offset + 1)) or next_line.is_blank:
                break
        peek_offset += 1
    else:
        if last_border_offset is not None:
            source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__(last_border_offset)
        else:
            source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__(peek_offset)
        return None
    table_slice = source.gAAAAABmoAOUJEv8h9H0QSbueJK37Z9fOID2IPjQk2tIOi0H_37BvDq_fVmq0QJieiTufnR9oHGDFJnZhy07M4FK_nd_VCruSA__(0, peek_offset + 1)
    source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__(peek_offset)
    return table_slice