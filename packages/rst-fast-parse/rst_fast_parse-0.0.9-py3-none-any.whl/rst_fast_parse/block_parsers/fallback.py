from __future__ import annotations
import re
from rst_fast_parse.core import gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_, gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__
from rst_fast_parse.elements import BasicElement, ElementListBase, ListElement, ListItemElement, TitleElement
from rst_fast_parse.regexes.block import gAAAAABmoAOUnkAGH_yH7dkoc8v_97xQX3glxPqFhNr9VFt6BFYr6SNP9hMkHz0swdLdm_4XBUCm5NO_nR_SRZujE3ikBiUSLoYuCd2ljF20z5rFvAdrfIw_, gAAAAABmoAOU5xOHdrDyYmDJK0ra0tYd9mNKR7zkMQC2aOKQWzW0JSUHs3YRVMJXD6LZxEBztjGg3qTNnlBXC6EBFWo52OVhP9Eu6Lq24jl8dXXbGxy_oRs_, gAAAAABmoAOUK3qoTcpCIMo11Tceoi0gJHdId6UM22NGF1_KTD7VuJwcYlTobc35Mdw4J9aXg_4b99M4AXqGpOYYyIvPyQyFwg__, gAAAAABmoAOUCX4qbDAo6ca43j8gQxClIhbGmk2TBfxXidgRyEBusUpZzIAFZtvfheHobJRNBP6_wVtC0m4qzV97aUPcJrN33Q__, gAAAAABmoAOUgvEF0GC8vjiI4NK0TipwfRhRuh4XnN3ErXHQyvb_zIJf_JF4QnCuGM0IEu1QGP_tBH53l5XxKAHepHDM5pM_oQ__, gAAAAABmoAOU3RVvo3YkzKhGKWCu8fKyuDtctqPSjiVzXO1JaMBXt0uqZpqYc1q1N6ZBumHojK1ZpxK0ChcZlgnozjyDbWAvOA__, gAAAAABmoAOUnHqpLJJqsKu6nt3jao4Sb8SXBJi2UyO8DQBREvsF8PtbY_4nAG8RugxGsr7H9iRaFQk5pbMA_UIemHaUJFOFEA__, gAAAAABmoAOUilAY8JVMHSn3PlAehbQgek6ceEpJaI65RtAIM4B9PIJltNB_cd0fZXKMgG5_fZobNpAStyW1_RbTbqSGaCCbB3fojanbDpBoIjJEYH5gt_8_, gAAAAABmoAOUciGbPWHH9cixuJIUoTSQv36k_oLO1fWRvprvdfidJmkqFfVgSzXcIB3CFvt5ZyJz8wmv1JPj0djcKmyp2ZdQHLv8QM1d9PeY9dZhVwTUzaM_, gAAAAABmoAOUO0fbYGF_1aMI31Cj1GJYoMXfpMZr0t7mHhx6PidwQjroxO_o8pIpPU3KRfdsJNrnfort_LZMNb5yFLYCgFAQds6t51IH4MBiN4LR9Ev119Q_, gAAAAABmoAOUNEZRwDi3WbtiZvOsdXXjLo1GOTAM7lk6EnQU8a1J07dFSBAGxty05qt97c5VjiucLY83azKMVO_cKNtfWxWklaN8vDTXPX2fznNswY6SGvM_, gAAAAABmoAOU_1XQzzQOe2tRhJLsdE1d00g3b2qaZ3_p_BolpWq5SaL9wQSSceZ4TUFIMtPA9SLfKWicuVuqWO4sdQpzXLghXg__, gAAAAABmoAOU11e3jgf8NDs2Qjnelo_NFgqMrakhTNV_4uMiSvum0pcQGEt_lgTtgFM_vAnUdCJ5_7WMRIHAVLbunQiBbLMk0A__
from rst_fast_parse.source import gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__, gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__
from rst_fast_parse.utils.column_widths import gAAAAABmoAOUdlj0PfNg4w4pJaxFAjHMB9z9jpZUSmkB101ROIEkW_y_TnWHUsEby6Z9CVvMVPDk8mQ1QthKul0gQBwS0iyKUQ__

def gAAAAABmoAOUWQNakEHu6VVR1xw2IM_RHB0aoNAjL6OeRo6n9hjxd_f__pS_JPD3oUtjUB_TgvoOF8TodNhD_SImYEfBCUZQow__(source: gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__, parent: ElementListBase, context: gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__, /) -> gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_:
    if not (current_line := source.current_line):
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUjd_6MxHjEtt1TugiZ6yaacbq1nREHVx2Fk2T_2621FG1CjXnhtaIU_bVoJ1U7KN1_WjYt6NyPEGMdldCcwNscQ__
    next_line = source.gAAAAABmoAOU4MROUYia9kJe75WM4gcw9LvrTZXAqyYK7_Ax0bicP68Y_yrusuxyIyyGjE_JLwwpuAjWfnUpxSISbSe_h_y4IQ__()
    if next_line is None or next_line.is_blank:
        gAAAAABmoAOU8708JmzN6MvvJeQwvs_wePjGcRE5h7BdWfHwxAOgVA8Cxn5IVKoWBWKesLfwIAmRcKqvxUqwSAAtCKN_ecrQ_dZf35iDo4Tk8JdfECNL5jo_(current_line, source, parent, context)
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__
    if next_line.content and next_line.content[0] == ' ':
        gAAAAABmoAOUhJHUJJrDCzIjZVwjszgLq_Wu_gQ_QlXtcxvc8K5PMkyueLVUZpYeq3Az5Xr_QYsHgWOOxp875QxMgS2Q96XMsIN34uL6K_Rr9J20gXewqak_(source, parent, context)
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__
    min_marker_length = 4
    if re.match(gAAAAABmoAOUNEZRwDi3WbtiZvOsdXXjLo1GOTAM7lk6EnQU8a1J07dFSBAGxty05qt97c5VjiucLY83azKMVO_cKNtfWxWklaN8vDTXPX2fznNswY6SGvM_, next_line.content):
        title = current_line.content.rstrip()
        underline = next_line.content.rstrip()
        if gAAAAABmoAOUdlj0PfNg4w4pJaxFAjHMB9z9jpZUSmkB101ROIEkW_y_TnWHUsEby6Z9CVvMVPDk8mQ1QthKul0gQBwS0iyKUQ__(title) > len(underline):
            if len(underline) < min_marker_length:
                gAAAAABmoAOUETjx5JiybFusdZW1DczptMkAWqg5Wm9dGArJfOKaW6oNnHEPuZNZMkCkDA57p2i6249yzCT6KoL1EJf_gjheJ3r_2OqEJquyUBJT_oviJYQ_(source, parent, context)
                return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__
        if not context.allow_titles:
            source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__()
            return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__
        source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__()
        parent.append(TitleElement(False, underline[0], title, (current_line.line, next_line.line)))
        return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__
    gAAAAABmoAOUETjx5JiybFusdZW1DczptMkAWqg5Wm9dGArJfOKaW6oNnHEPuZNZMkCkDA57p2i6249yzCT6KoL1EJf_gjheJ3r_2OqEJquyUBJT_oviJYQ_(source, parent, context)
    return gAAAAABmoAOUK6a31ilBYCNne1KHr5GGI0wmbn6uggbSCpy0_nPWgox1BumePmjQoKqUBfM9mvOIQoLxFO3TSYLOmEPy9lPt54L0BLR15UMgg_cTQBdBnEY_.gAAAAABmoAOUMINrwRwG9NVXYRLx79JCCoABoZ5Nv41ihAeKAbyL72Xq4d5kNltHHmo3GEY1r2UqNH8g2QbIUKgVieWlCgBhlg__

def gAAAAABmoAOU8708JmzN6MvvJeQwvs_wePjGcRE5h7BdWfHwxAOgVA8Cxn5IVKoWBWKesLfwIAmRcKqvxUqwSAAtCKN_ecrQ_dZf35iDo4Tk8JdfECNL5jo_(current_line: gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__, source: gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__, parent: ElementListBase, context: gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__, /) -> None:
    paragraph_line = current_line.rstrip()
    literal_block_next = re.search(gAAAAABmoAOUilAY8JVMHSn3PlAehbQgek6ceEpJaI65RtAIM4B9PIJltNB_cd0fZXKMgG5_fZobNpAStyW1_RbTbqSGaCCbB3fojanbDpBoIjJEYH5gt_8_, paragraph_line.content)
    parent.append(BasicElement('paragraph', (paragraph_line.line, paragraph_line.line)))
    if literal_block_next:
        gAAAAABmoAOURAmibuYTp1KMNv1vvtkOpKdKQctGlalD6B6s7Gav9XmuxBT__RmJ9ruE9xD3eskmdXl5ag2_sxZxQJRdTyujCQ__(source, parent, context)

def gAAAAABmoAOUETjx5JiybFusdZW1DczptMkAWqg5Wm9dGArJfOKaW6oNnHEPuZNZMkCkDA57p2i6249yzCT6KoL1EJf_gjheJ3r_2OqEJquyUBJT_oviJYQ_(source: gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__, parent: ElementListBase, context: gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__, /) -> None:
    if (_current_line := source.current_line) is None:
        return None
    text_slice = source.gAAAAABmoAOUCk1aQjjQn3Z4dYapsn0HEEIQzzpDFIExvv7dM8dGC_YER09iQNX9sf3o7i2vxISlwC42982fos9FLp9kXH7l_g__(stop_on_indented=True, advance=True)
    text_content = text_slice.gAAAAABmoAOUMEwj7gzeAyhCjYZfpw5MdiqELuLqXF3w0q3dNnpK0nMCrgfy8BUmcTdshRTR8h6cF0i1QTC3v4EiprvTaZgr7g__().rstrip()
    literal_block_next = re.search(gAAAAABmoAOUilAY8JVMHSn3PlAehbQgek6ceEpJaI65RtAIM4B9PIJltNB_cd0fZXKMgG5_fZobNpAStyW1_RbTbqSGaCCbB3fojanbDpBoIjJEYH5gt_8_, text_content)
    if (first := text_slice.current_line) and (last := text_slice.last_line):
        parent.append(BasicElement('paragraph', (first.line, last.line)))
    if literal_block_next:
        gAAAAABmoAOURAmibuYTp1KMNv1vvtkOpKdKQctGlalD6B6s7Gav9XmuxBT__RmJ9ruE9xD3eskmdXl5ag2_sxZxQJRdTyujCQ__(source, parent, context)
    return None

def gAAAAABmoAOURAmibuYTp1KMNv1vvtkOpKdKQctGlalD6B6s7Gav9XmuxBT__RmJ9ruE9xD3eskmdXl5ag2_sxZxQJRdTyujCQ__(source: gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__, parent: ElementListBase, context: gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__, /) -> None:
    original_index = source.current_index
    source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__()
    block_slice = source.gAAAAABmoAOUfMZzlaWk8YgQcLpS1XqWZRi0a2b1OLujUbk1MpzROhDcsEWw_xxiyXNRwvcQrHctDQjFzkGo6FxQMZvAgkDyYg__(advance=True).gAAAAABmoAOUBM_jeyehL62A4EjuS1rwlefr_E0q_magTf3zb7fJU1Yaa8OpW_KwUOHraYDzqb2WJyaP9nvv1jVGbIpMeDef6IPnPbCOHz9sfmPTUzokNx0_()
    if not block_slice.gAAAAABmoAOUR6KFT3ZpMWAeD51IwZzREeQge_XjmY_K_zJWSp4ADn2Md7XN8XCmYBBmmsiQQjdzWBx8hoIhu5ufMxt4pQQogQ__():
        source.gAAAAABmoAOUiHCs3LCinJOYERnH6vPz6qCUT6D4eKdPi_bc1mJqXbmvDmMGZ0suTJYBnkPu8eitfxw8k9edq4_ryrTa7KXfE_XlXfPc_uK_dLILFBGi0b8_(original_index)
        peek_index = 2
        while (next_line := source.gAAAAABmoAOU4MROUYia9kJe75WM4gcw9LvrTZXAqyYK7_Ax0bicP68Y_yrusuxyIyyGjE_JLwwpuAjWfnUpxSISbSe_h_y4IQ__(peek_index)) and next_line.is_blank:
            peek_index += 1
        if (next_line := source.gAAAAABmoAOU4MROUYia9kJe75WM4gcw9LvrTZXAqyYK7_Ax0bicP68Y_yrusuxyIyyGjE_JLwwpuAjWfnUpxSISbSe_h_y4IQ__(peek_index)) and re.match(gAAAAABmoAOUO0fbYGF_1aMI31Cj1GJYoMXfpMZr0t7mHhx6PidwQjroxO_o8pIpPU3KRfdsJNrnfort_LZMNb5yFLYCgFAQds6t51IH4MBiN4LR9Ev119Q_, next_line.content):
            quote_char = next_line.content[0]
            source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__(peek_index - 1)
            lines = []
            while (next_line := source.gAAAAABmoAOU4MROUYia9kJe75WM4gcw9LvrTZXAqyYK7_Ax0bicP68Y_yrusuxyIyyGjE_JLwwpuAjWfnUpxSISbSe_h_y4IQ__(1)) and next_line.content and (next_line.content[0] == quote_char):
                lines.append(next_line)
                source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__()
            block_slice = gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__(lines)
        else:
            return None
    if (first := block_slice.current_line) and (last := block_slice.last_line):
        parent.append(BasicElement('literal_block', (first.line, last.line)))

def gAAAAABmoAOUhJHUJJrDCzIjZVwjszgLq_Wu_gQ_QlXtcxvc8K5PMkyueLVUZpYeq3Az5Xr_QYsHgWOOxp875QxMgS2Q96XMsIN34uL6K_Rr9J20gXewqak_(source: gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__, parent: ElementListBase, context: gAAAAABmoAOUqM53pSy6VaERlD8sLi4BlRc1KzC_EEG53luKXTB7O8NkYrgjgDrABFt8A8EQ_YI4AqHFsoVQvgKuvKGRSj_DBQ__, /) -> None:
    items: list[ListItemElement] = []
    while (first_line := source.current_line):
        if items:
            if first_line.is_blank:
                source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__()
                continue
            if first_line.content[0] == ' ' or any((re.match(regex, first_line.content) for regex in (gAAAAABmoAOU5xOHdrDyYmDJK0ra0tYd9mNKR7zkMQC2aOKQWzW0JSUHs3YRVMJXD6LZxEBztjGg3qTNnlBXC6EBFWo52OVhP9Eu6Lq24jl8dXXbGxy_oRs_, gAAAAABmoAOUCX4qbDAo6ca43j8gQxClIhbGmk2TBfxXidgRyEBusUpZzIAFZtvfheHobJRNBP6_wVtC0m4qzV97aUPcJrN33Q__, gAAAAABmoAOU3RVvo3YkzKhGKWCu8fKyuDtctqPSjiVzXO1JaMBXt0uqZpqYc1q1N6ZBumHojK1ZpxK0ChcZlgnozjyDbWAvOA__, gAAAAABmoAOUciGbPWHH9cixuJIUoTSQv36k_oLO1fWRvprvdfidJmkqFfVgSzXcIB3CFvt5ZyJz8wmv1JPj0djcKmyp2ZdQHLv8QM1d9PeY9dZhVwTUzaM_, gAAAAABmoAOUK3qoTcpCIMo11Tceoi0gJHdId6UM22NGF1_KTD7VuJwcYlTobc35Mdw4J9aXg_4b99M4AXqGpOYYyIvPyQyFwg__, gAAAAABmoAOUnHqpLJJqsKu6nt3jao4Sb8SXBJi2UyO8DQBREvsF8PtbY_4nAG8RugxGsr7H9iRaFQk5pbMA_UIemHaUJFOFEA__, gAAAAABmoAOU_1XQzzQOe2tRhJLsdE1d00g3b2qaZ3_p_BolpWq5SaL9wQSSceZ4TUFIMtPA9SLfKWicuVuqWO4sdQpzXLghXg__, gAAAAABmoAOU11e3jgf8NDs2Qjnelo_NFgqMrakhTNV_4uMiSvum0pcQGEt_lgTtgFM_vAnUdCJ5_7WMRIHAVLbunQiBbLMk0A__, gAAAAABmoAOUgvEF0GC8vjiI4NK0TipwfRhRuh4XnN3ErXHQyvb_zIJf_JF4QnCuGM0IEu1QGP_tBH53l5XxKAHepHDM5pM_oQ__, gAAAAABmoAOUnkAGH_yH7dkoc8v_97xQX3glxPqFhNr9VFt6BFYr6SNP9hMkHz0swdLdm_4XBUCm5NO_nR_SRZujE3ikBiUSLoYuCd2ljF20z5rFvAdrfIw_, gAAAAABmoAOUNEZRwDi3WbtiZvOsdXXjLo1GOTAM7lk6EnQU8a1J07dFSBAGxty05qt97c5VjiucLY83azKMVO_cKNtfWxWklaN8vDTXPX2fznNswY6SGvM_))):
                source.gAAAAABmoAOUXBPdo9OkaxYoAc4gGo8fBfuw88NaQvW9F6dJXeOAGnTz4uetdGLdeffAFTTUljLpCo2l_WvJvzJc40wY5KLzCg__()
                break
        if (next_line := source.gAAAAABmoAOU4MROUYia9kJe75WM4gcw9LvrTZXAqyYK7_Ax0bicP68Y_yrusuxyIyyGjE_JLwwpuAjWfnUpxSISbSe_h_y4IQ__()):
            if next_line.content and next_line.content[0] == ' ':
                source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__()
            else:
                source.gAAAAABmoAOUXBPdo9OkaxYoAc4gGo8fBfuw88NaQvW9F6dJXeOAGnTz4uetdGLdeffAFTTUljLpCo2l_WvJvzJc40wY5KLzCg__()
                break
        else:
            source.gAAAAABmoAOUXBPdo9OkaxYoAc4gGo8fBfuw88NaQvW9F6dJXeOAGnTz4uetdGLdeffAFTTUljLpCo2l_WvJvzJc40wY5KLzCg__()
            break
        definition = first_line
        description = source.gAAAAABmoAOUfMZzlaWk8YgQcLpS1XqWZRi0a2b1OLujUbk1MpzROhDcsEWw_xxiyXNRwvcQrHctDQjFzkGo6FxQMZvAgkDyYg__(advance=True)
        list_item = ListItemElement((definition.line, definition.line if description.last_line is None else description.last_line.line))
        items.append(list_item)
        context.gAAAAABmoAOUjwOEnh8OvcV78z8zUYoqJJ0Y2TrThUDOYQObmZ9KKZuVx0fs2RHsOQai0Er2b51fz7_55XcSDLfrKPsEXT3Abw__(description, list_item)
        source.gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__()
    if items:
        parent.append(ListElement('definition_list', items))