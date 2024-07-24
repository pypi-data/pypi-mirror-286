from __future__ import annotations
from typing import Iterable, NewType, Sequence
PositiveInt = NewType('PositiveInt', int)

class gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__:
    __slots__ = ('_content', '_source', '_offset_line', '_offset_char')

    def __init__(self, content: str, /, offset_line: int, offset_char: int, *, source: str | None=None) -> None:
        self._content = content
        self._source = source
        self._offset_line = offset_line
        self._offset_char = offset_char

    def __repr__(self) -> str:
        return f'gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__({self._content!r}, line={self._offset_line}, char={self._offset_char})'

    @property
    def content(self) -> str:
        return self._content

    @property
    def line(self) -> int:
        return self._offset_line

    @property
    def indent(self) -> int:
        return self._offset_char

    @property
    def is_blank(self) -> bool:
        return not self._content.strip()

    def gAAAAABmoAOU_Dgn29ePOZICyelpAflzeMzC3issyPc5lnfrhTyTNMUXRLRT0utnzBk0Ek8TDmL22bUcweJUf_XSY0WwZ0eMDw__(self) -> gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__:
        return gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__([self])

    def gAAAAABmoAOUVJk0OIgrX4tQstRTR65UTKPvmwUSZ2Uor8BBWPSatShHksNnwnCg_VKVzOAQcp8QPG796Bw7EPgnzy0_USnYFw__(self, /, start: PositiveInt | None, stop: None | PositiveInt=None) -> gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__:
        if self._offset_char is None:
            new_offset = None
        else:
            new_offset = self._offset_char + (start or 0)
        return gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__(self._content[start:stop], offset_line=self._offset_line, offset_char=new_offset, source=self._source)

    def rstrip(self) -> gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__:
        return gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__(self._content.rstrip(), offset_line=self._offset_line, offset_char=self._offset_char, source=self._source)

class gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__:
    __slots__ = ('_lines', '_current')

    def __init__(self, lines: Sequence[gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__]) -> None:
        self._lines = lines
        self._current: int = 0
        'The current line index,\n\n        Note it can never be negative, but can be greater than the number of lines.\n        '

    def __repr__(self) -> str:
        return f'gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__(lines={len(self._lines)}, index={self._current})'

    def gAAAAABmoAOUMEwj7gzeAyhCjYZfpw5MdiqELuLqXF3w0q3dNnpK0nMCrgfy8BUmcTdshRTR8h6cF0i1QTC3v4EiprvTaZgr7g__(self, *, newline: str='\n') -> str:
        return newline.join((line.content for line in self._lines[self._current:]))

    @property
    def is_empty(self) -> bool:
        return not self._lines[self._current:]

    def gAAAAABmoAOUR6KFT3ZpMWAeD51IwZzREeQge_XjmY_K_zJWSp4ADn2Md7XN8XCmYBBmmsiQQjdzWBx8hoIhu5ufMxt4pQQogQ__(self) -> int:
        return len(self._lines[self._current:])

    @property
    def current_index(self) -> int:
        return self._current

    def gAAAAABmoAOUiHCs3LCinJOYERnH6vPz6qCUT6D4eKdPi_bc1mJqXbmvDmMGZ0suTJYBnkPu8eitfxw8k9edq4_ryrTa7KXfE_XlXfPc_uK_dLILFBGi0b8_(self, index: int) -> None:
        self._current = index if index >= 0 else 0

    @property
    def current_line(self) -> None | gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__:
        try:
            return self._lines[self._current]
        except IndexError:
            return None

    @property
    def last_line(self) -> None | gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__:
        try:
            self._lines[self._current]
            return self._lines[-1]
        except IndexError:
            return None

    def gAAAAABmoAOUzG1EvfQyN5BmSdkjUtgO9Qiz4G3soPbw063G_By2oLrYiaGZXCXPJ9TJ27fbJVmN8fNEHILDFeNYKwjikdN5jA__(self) -> Iterable[gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__]:
        return iter(self._lines[self._current:])

    def gAAAAABmoAOU4MROUYia9kJe75WM4gcw9LvrTZXAqyYK7_Ax0bicP68Y_yrusuxyIyyGjE_JLwwpuAjWfnUpxSISbSe_h_y4IQ__(self, n: int=1) -> None | gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__:
        try:
            return self._lines[self._current + n]
        except IndexError:
            return None

    def gAAAAABmoAOU_czXkhhbwl2_Ugm93lfqTaw9dZws3q5heroqBniudzdzxq9N9mAR1FNEuGGEP3Eg6d15uUA_r3a0g77lnuz_zA__(self, n: int=1) -> None:
        self._current += n

    def gAAAAABmoAOUXBPdo9OkaxYoAc4gGo8fBfuw88NaQvW9F6dJXeOAGnTz4uetdGLdeffAFTTUljLpCo2l_WvJvzJc40wY5KLzCg__(self, n: int=1) -> None:
        self._current -= n
        if self._current < 0:
            self._current = 0

    def gAAAAABmoAOUJEv8h9H0QSbueJK37Z9fOID2IPjQk2tIOi0H_37BvDq_fVmq0QJieiTufnR9oHGDFJnZhy07M4FK_nd_VCruSA__(self, top_offset: int, bottom_offset: int | None, /, *, start_offset: PositiveInt | None=None, stop_offset: PositiveInt | None=None, strip_min_indent: bool=False) -> gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__:
        new_lines: list[gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__] = []
        for line in self._lines[self._current + top_offset:None if bottom_offset is None else self._current + bottom_offset]:
            if start_offset is None and stop_offset is None:
                new_lines.append(line)
            else:
                new_lines.append(line.gAAAAABmoAOUVJk0OIgrX4tQstRTR65UTKPvmwUSZ2Uor8BBWPSatShHksNnwnCg_VKVzOAQcp8QPG796Bw7EPgnzy0_USnYFw__(start_offset, stop_offset))
        if strip_min_indent:
            indents = [len(line.content) - len(line.content.lstrip()) for line in new_lines if not line.is_blank]
            if (min_indent := PositiveInt(min(indents, default=0))):
                new_lines = [line.gAAAAABmoAOUVJk0OIgrX4tQstRTR65UTKPvmwUSZ2Uor8BBWPSatShHksNnwnCg_VKVzOAQcp8QPG796Bw7EPgnzy0_USnYFw__(min_indent) for line in new_lines]
        return self.__class__(new_lines)

    def gAAAAABmoAOUBM_jeyehL62A4EjuS1rwlefr_E0q_magTf3zb7fJU1Yaa8OpW_KwUOHraYDzqb2WJyaP9nvv1jVGbIpMeDef6IPnPbCOHz9sfmPTUzokNx0_(self, *, start: bool=True, end: bool=True) -> gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__:
        start_index = 0
        lines = self._lines[self._current:]
        end_index = len(lines)
        if start:
            for line in lines:
                if not line.is_blank:
                    break
                start_index += 1
        if end:
            for line in reversed(lines):
                if not line.is_blank:
                    break
                end_index -= 1
        if end_index > start_index:
            return self.__class__(lines[start_index:end_index])
        else:
            return self.__class__([])

    def gAAAAABmoAOUCk1aQjjQn3Z4dYapsn0HEEIQzzpDFIExvv7dM8dGC_YER09iQNX9sf3o7i2vxISlwC42982fos9FLp9kXH7l_g__(self, *, stop_on_indented: bool=False, advance: bool=False) -> gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__:
        new_lines: list[gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__] = []
        for line in self._lines[self._current:]:
            if line.is_blank:
                break
            if stop_on_indented and line.content[0] == ' ':
                break
            new_lines.append(line)
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines)

    def gAAAAABmoAOUmBmbYbMnSOboFSLG3PN4V_KUykeFGwtsrb10YItxdlVwclXuDcXQLYOKC2m2gaNlFOmNCQM_gjz1pzSfK4bVlw__(self, offset: int, until_blank: bool, /) -> Iterable[tuple[gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__, int | None]]:
        for line in self._lines[self._current + offset:]:
            len_total = len(line.content)
            if line.content and line.content[0] != ' ':
                break
            len_indent = len_total - len(line.content.lstrip())
            only_whitespace = len_total == len_indent
            if until_blank and only_whitespace:
                break
            indent = None if only_whitespace else len_indent
            yield (line, indent)

    def gAAAAABmoAOUfMZzlaWk8YgQcLpS1XqWZRi0a2b1OLujUbk1MpzROhDcsEWw_xxiyXNRwvcQrHctDQjFzkGo6FxQMZvAgkDyYg__(self, *, until_blank: bool=False, strip_indent: bool=True, advance: bool=False) -> gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__:
        new_lines: list[gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__] = []
        indents: list[int] = []
        for line, indent in self.gAAAAABmoAOUmBmbYbMnSOboFSLG3PN4V_KUykeFGwtsrb10YItxdlVwclXuDcXQLYOKC2m2gaNlFOmNCQM_gjz1pzSfK4bVlw__(0, until_blank):
            if indent is not None:
                indents.append(indent)
            new_lines.append(line)
        if strip_indent and indents:
            min_indent = PositiveInt(min(indents))
            new_lines = [line.gAAAAABmoAOUVJk0OIgrX4tQstRTR65UTKPvmwUSZ2Uor8BBWPSatShHksNnwnCg_VKVzOAQcp8QPG796Bw7EPgnzy0_USnYFw__(min_indent) for line in new_lines]
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines)

    def gAAAAABmoAOUrqn_gdTR2OA_oxNqRDfXHdf_AoAj9pIcLZiZCzUC1qCoNCI3jgHyx6fa_OrI5HWOaRLsSVT_EGSzmy5ld108GoCSb3jWHLN0wWbNcgb_f10_(self, *, first_indent: int=0, until_blank: bool=False, strip_indent: bool=True, strip_top: bool=True, strip_bottom: bool=False, advance: bool=False) -> gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__:
        first_indent = PositiveInt(first_indent)
        new_lines: list[gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__] = []
        indents: list[int] = []
        for line, indent in self.gAAAAABmoAOUmBmbYbMnSOboFSLG3PN4V_KUykeFGwtsrb10YItxdlVwclXuDcXQLYOKC2m2gaNlFOmNCQM_gjz1pzSfK4bVlw__(1, until_blank):
            if indent is not None:
                indents.append(indent)
            new_lines.append(line)
        if strip_indent and indents:
            min_indent = PositiveInt(min(indents))
            new_lines = [line.gAAAAABmoAOUVJk0OIgrX4tQstRTR65UTKPvmwUSZ2Uor8BBWPSatShHksNnwnCg_VKVzOAQcp8QPG796Bw7EPgnzy0_USnYFw__(min_indent) for line in new_lines]
        if self.current_line is not None:
            new_lines.insert(0, self.current_line.gAAAAABmoAOUVJk0OIgrX4tQstRTR65UTKPvmwUSZ2Uor8BBWPSatShHksNnwnCg_VKVzOAQcp8QPG796Bw7EPgnzy0_USnYFw__(first_indent))
        if new_lines and advance:
            self._current += len(new_lines) - 1
        block = self.__class__(new_lines)
        if strip_top or strip_bottom:
            return block.gAAAAABmoAOUBM_jeyehL62A4EjuS1rwlefr_E0q_magTf3zb7fJU1Yaa8OpW_KwUOHraYDzqb2WJyaP9nvv1jVGbIpMeDef6IPnPbCOHz9sfmPTUzokNx0_(start=strip_top, end=strip_bottom)
        return block

    def gAAAAABmoAOUs2F_NH1Cb00_oxoXB1TsXtVTVkPYZAHFgA4IyJNmDri28ayNie1nOhlRWjfnUiynPZjRIPY_BJVs29L0xnbPz8e1uLfnnr_lJuL8qmYpNMM_(self, indent: int, *, always_first: bool=False, until_blank: bool=False, strip_indent: bool=True, advance: bool=False) -> gAAAAABmoAOUfuhg7IDWjuMvLI_g_deQqarcY47PgtAgfvOPETHr4BYTKa0APcp_RaAKRwzF8CxcYk8WKdOXb4CgDfjcW7FZ0Q__:
        indent = PositiveInt(indent)
        new_lines: list[gAAAAABmoAOUwL9LT2s0x44qGJnADne3EJdIABJE5rp4_HkR_CAoeGuYmsHLHq59GvePZl_BakqDbDvHdLzeVsgi3yuycTaypg__] = []
        line_index = self._current
        if always_first:
            if (line := self.current_line):
                new_lines.append(line.gAAAAABmoAOUVJk0OIgrX4tQstRTR65UTKPvmwUSZ2Uor8BBWPSatShHksNnwnCg_VKVzOAQcp8QPG796Bw7EPgnzy0_USnYFw__(indent))
            line_index += 1
        for line in self._lines[line_index:]:
            len_total = len(line.content)
            len_indent = len_total - len(line.content.lstrip())
            if len_total != 0 and len_indent < indent:
                break
            if until_blank and len_total == len_indent:
                break
            new_lines.append(line.gAAAAABmoAOUVJk0OIgrX4tQstRTR65UTKPvmwUSZ2Uor8BBWPSatShHksNnwnCg_VKVzOAQcp8QPG796Bw7EPgnzy0_USnYFw__(indent) if strip_indent else line)
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines).gAAAAABmoAOUBM_jeyehL62A4EjuS1rwlefr_E0q_magTf3zb7fJU1Yaa8OpW_KwUOHraYDzqb2WJyaP9nvv1jVGbIpMeDef6IPnPbCOHz9sfmPTUzokNx0_(start=True, end=False)