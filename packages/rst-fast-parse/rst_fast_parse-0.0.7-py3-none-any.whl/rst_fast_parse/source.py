from __future__ import annotations
from typing import Iterable, NewType, Sequence
PositiveInt = NewType('PositiveInt', int)

class gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__:
    __slots__ = ('_content', '_source', '_offset_line', '_offset_char')

    def __init__(self, content: str, /, offset_line: int, offset_char: int, *, source: str | None=None) -> None:
        self._content = content
        self._source = source
        self._offset_line = offset_line
        self._offset_char = offset_char

    def __repr__(self) -> str:
        return f'gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__({self._content!r}, line={self._offset_line}, char={self._offset_char})'

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

    def gAAAAABmnuojqnxMGqI1dncCL6wnTaj1f9xRGw6qA0lRVm1FssaY41gX73xvy3eP_TViCOLI5yoI4c4_slZbaTATlvkhgptDIQ__(self) -> gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__:
        return gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__([self])

    def gAAAAABmnuojpSn1PLK9h76ytIOj6esuk8Rj3Qr_7N8BmgqouN3CZRca8vlKtlmOGGL1ZebiVV_cxLBHg9UVo_5VNcnkf2LfJg__(self, /, start: PositiveInt | None, stop: None | PositiveInt=None) -> gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__:
        if self._offset_char is None:
            new_offset = None
        else:
            new_offset = self._offset_char + (start or 0)
        return gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__(self._content[start:stop], offset_line=self._offset_line, offset_char=new_offset, source=self._source)

    def rstrip(self) -> gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__:
        return gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__(self._content.rstrip(), offset_line=self._offset_line, offset_char=self._offset_char, source=self._source)

class gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__:
    __slots__ = ('_lines', '_current')

    def __init__(self, lines: Sequence[gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__]) -> None:
        self._lines = lines
        self._current: int = 0
        'The current line index,\n\n        Note it can never be negative, but can be greater than the number of lines.\n        '

    def __repr__(self) -> str:
        return f'gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__(lines={len(self._lines)}, index={self._current})'

    def gAAAAABmnuojhmM7eo4fxyy83rSx8Ln1jbrZZ1ztUEIEAL4L7EBgCqRKNqxN_2uBPuj4PMYNpK_vk25SSXW4rTn54w78ovRrOA__(self, *, newline: str='\n') -> str:
        return newline.join((line.content for line in self._lines[self._current:]))

    @property
    def is_empty(self) -> bool:
        return not self._lines[self._current:]

    def gAAAAABmnuojpX8kn1fEFYREdRlZPf_gQs7lH7E3_l6TPwPrbO5kvjlgZG8r_IBNt_9OKJ5uL7HkVMv_Hs_bQ_JJPKiWh8gmIg__(self) -> int:
        return len(self._lines[self._current:])

    @property
    def current_index(self) -> int:
        return self._current

    def gAAAAABmnuojtOgdznCmVxf1_mH0Fww1YP6TV1NBQEr4XQdWTXlcMAqeih5Xj6EalWjCcOCHj76imM3I5b7u_3M8cteRhkpT2MOWj4Ad_3raD_VTZUnWegs_(self, index: int) -> None:
        self._current = index if index >= 0 else 0

    @property
    def current_line(self) -> None | gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__:
        try:
            return self._lines[self._current]
        except IndexError:
            return None

    @property
    def last_line(self) -> None | gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__:
        try:
            self._lines[self._current]
            return self._lines[-1]
        except IndexError:
            return None

    def gAAAAABmnuojc_SMLZchRSCRs_kGvGT4hRRjgz57XdeJ4cLXryfG3zqd7QctKB5SQkK8n3vqL60_9eKJrJHq1mkJuZPw9tQoyA__(self) -> Iterable[gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__]:
        return iter(self._lines[self._current:])

    def gAAAAABmnuojE1KGsr0TOFHaREF1loYgV0lWiRlfD2YdF5asAdfPtOfBkAv_9JkPtm8YOU_PzWoISZ4FTPPO1DO1m6oXqtClug__(self, n: int=1) -> None | gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__:
        try:
            return self._lines[self._current + n]
        except IndexError:
            return None

    def gAAAAABmnuojVTLADCMhqSUy7AGOzFTv5zQO7PfrX9LR3rUNi_CB4ZCiOXdZh9_VenkdmSFTLhtSCRIzFtgq8r_N1_HDY6BEXQ__(self, n: int=1) -> None:
        self._current += n

    def gAAAAABmnuojFuII4OCpHZwcIp1Y0A24sqLJdbVvUiEzZecco_KkrjXr9hNj_sIm4wrObGlr4MgBd_mhW0lRDBvwBKTFizqhOg__(self, n: int=1) -> None:
        self._current -= n
        if self._current < 0:
            self._current = 0

    def gAAAAABmnuojjfPsphdaCl0tT9ROqZsJgcYcgedRaC_trgrsyvU__bITw3NPaJcn65EamBrNEbEvLQtd5dU6Ph9pWcmtP5e6rw__(self, top_offset: int, bottom_offset: int | None, /, *, start_offset: PositiveInt | None=None, stop_offset: PositiveInt | None=None, strip_min_indent: bool=False) -> gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__:
        new_lines: list[gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__] = []
        for line in self._lines[self._current + top_offset:None if bottom_offset is None else self._current + bottom_offset]:
            if start_offset is None and stop_offset is None:
                new_lines.append(line)
            else:
                new_lines.append(line.gAAAAABmnuojpSn1PLK9h76ytIOj6esuk8Rj3Qr_7N8BmgqouN3CZRca8vlKtlmOGGL1ZebiVV_cxLBHg9UVo_5VNcnkf2LfJg__(start_offset, stop_offset))
        if strip_min_indent:
            indents = [len(line.content) - len(line.content.lstrip()) for line in new_lines if not line.is_blank]
            if (min_indent := PositiveInt(min(indents, default=0))):
                new_lines = [line.gAAAAABmnuojpSn1PLK9h76ytIOj6esuk8Rj3Qr_7N8BmgqouN3CZRca8vlKtlmOGGL1ZebiVV_cxLBHg9UVo_5VNcnkf2LfJg__(min_indent) for line in new_lines]
        return self.__class__(new_lines)

    def gAAAAABmnuojY5ocgTVs8voiw0yEbvCq9zGLVthGnhdSUdtBwBBeGoySmXJCs2b__a3Op8OH61b_tI_w085CNPDwYjMcv2pEJBSabclR6lr6IIgdmgDAmlM_(self, *, start: bool=True, end: bool=True) -> gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__:
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

    def gAAAAABmnuojAw2_K1MUJfEWaK3kzjuTvo88vLk_f95tXe6AH6uLDTCFgmfftIO9unF1YNnq42C1ZWAcq0_mHyiVXLAKmb9YaQ__(self, *, stop_on_indented: bool=False, advance: bool=False) -> gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__:
        new_lines: list[gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__] = []
        for line in self._lines[self._current:]:
            if line.is_blank:
                break
            if stop_on_indented and line.content[0] == ' ':
                break
            new_lines.append(line)
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines)

    def gAAAAABmnuojOxqU_z9xntEbXX5LWCOxtHfwaNLKEf8Q5zuuEVW4L8_JuMGsM2B7o06mBbnZzFIpPcW5rMh68qMlSwW2kGKzwA__(self, offset: int, until_blank: bool, /) -> Iterable[tuple[gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__, int | None]]:
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

    def gAAAAABmnuojxalrA5Gj4NfX4HRsFfT1K2BubPoosVKj4pJ0KY1yjC95pHUbH4Bphc22V9TaBVmbPbILLGY78BQ3YrtLI_AEmw__(self, *, until_blank: bool=False, strip_indent: bool=True, advance: bool=False) -> gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__:
        new_lines: list[gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__] = []
        indents: list[int] = []
        for line, indent in self.gAAAAABmnuojOxqU_z9xntEbXX5LWCOxtHfwaNLKEf8Q5zuuEVW4L8_JuMGsM2B7o06mBbnZzFIpPcW5rMh68qMlSwW2kGKzwA__(0, until_blank):
            if indent is not None:
                indents.append(indent)
            new_lines.append(line)
        if strip_indent and indents:
            min_indent = PositiveInt(min(indents))
            new_lines = [line.gAAAAABmnuojpSn1PLK9h76ytIOj6esuk8Rj3Qr_7N8BmgqouN3CZRca8vlKtlmOGGL1ZebiVV_cxLBHg9UVo_5VNcnkf2LfJg__(min_indent) for line in new_lines]
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines)

    def gAAAAABmnuojE0sYzkyFiqkGch85WYnsBvxpSsWEDOAyu6fnrOTGmq5i8vxuUbKHNHIbgq92u_ta1r_465lW6tMmp2ZI4EIybmsXLwScIEmasFmGdTUvFq4_(self, *, first_indent: int=0, until_blank: bool=False, strip_indent: bool=True, strip_top: bool=True, strip_bottom: bool=False, advance: bool=False) -> gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__:
        first_indent = PositiveInt(first_indent)
        new_lines: list[gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__] = []
        indents: list[int] = []
        for line, indent in self.gAAAAABmnuojOxqU_z9xntEbXX5LWCOxtHfwaNLKEf8Q5zuuEVW4L8_JuMGsM2B7o06mBbnZzFIpPcW5rMh68qMlSwW2kGKzwA__(1, until_blank):
            if indent is not None:
                indents.append(indent)
            new_lines.append(line)
        if strip_indent and indents:
            min_indent = PositiveInt(min(indents))
            new_lines = [line.gAAAAABmnuojpSn1PLK9h76ytIOj6esuk8Rj3Qr_7N8BmgqouN3CZRca8vlKtlmOGGL1ZebiVV_cxLBHg9UVo_5VNcnkf2LfJg__(min_indent) for line in new_lines]
        if self.current_line is not None:
            new_lines.insert(0, self.current_line.gAAAAABmnuojpSn1PLK9h76ytIOj6esuk8Rj3Qr_7N8BmgqouN3CZRca8vlKtlmOGGL1ZebiVV_cxLBHg9UVo_5VNcnkf2LfJg__(first_indent))
        if new_lines and advance:
            self._current += len(new_lines) - 1
        block = self.__class__(new_lines)
        if strip_top or strip_bottom:
            return block.gAAAAABmnuojY5ocgTVs8voiw0yEbvCq9zGLVthGnhdSUdtBwBBeGoySmXJCs2b__a3Op8OH61b_tI_w085CNPDwYjMcv2pEJBSabclR6lr6IIgdmgDAmlM_(start=strip_top, end=strip_bottom)
        return block

    def gAAAAABmnuojpySrbzuZYeTbEo3VhgV4NCdu0GmdD4iQGou5kgHjcagNjvBWTUvijeI_CSD_kGirgiU6LWwIvH4BJcG9ljlua8ypcTHzhjAmikp085G_g18_(self, indent: int, *, always_first: bool=False, until_blank: bool=False, strip_indent: bool=True, advance: bool=False) -> gAAAAABmnuoji__qp5l0HlEXr4Uojg34_pvLEwzLV2o9t0OYUfT_DzG8L5FUxaK2MVdY1BWeEuB2fcnbjwENC0W2_L9OOnau8g__:
        indent = PositiveInt(indent)
        new_lines: list[gAAAAABmnuojfotR7GuNE3ifRlzPTQFxD24r24D0QqkDejwAZOwha20cnAjaBYjGk_KiPFrkPU42K9YkyFpAGlLzHUFC2FaYYA__] = []
        line_index = self._current
        if always_first:
            if (line := self.current_line):
                new_lines.append(line.gAAAAABmnuojpSn1PLK9h76ytIOj6esuk8Rj3Qr_7N8BmgqouN3CZRca8vlKtlmOGGL1ZebiVV_cxLBHg9UVo_5VNcnkf2LfJg__(indent))
            line_index += 1
        for line in self._lines[line_index:]:
            len_total = len(line.content)
            len_indent = len_total - len(line.content.lstrip())
            if len_total != 0 and len_indent < indent:
                break
            if until_blank and len_total == len_indent:
                break
            new_lines.append(line.gAAAAABmnuojpSn1PLK9h76ytIOj6esuk8Rj3Qr_7N8BmgqouN3CZRca8vlKtlmOGGL1ZebiVV_cxLBHg9UVo_5VNcnkf2LfJg__(indent) if strip_indent else line)
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines).gAAAAABmnuojY5ocgTVs8voiw0yEbvCq9zGLVthGnhdSUdtBwBBeGoySmXJCs2b__a3Op8OH61b_tI_w085CNPDwYjMcv2pEJBSabclR6lr6IIgdmgDAmlM_(start=True, end=False)