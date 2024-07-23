from __future__ import annotations
from typing import Iterable, NewType, Sequence
PositiveInt = NewType('PositiveInt', int)

class gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__:
    __slots__ = ('_content', '_source', '_offset_line', '_offset_char')

    def __init__(self, content: str, /, offset_line: int, offset_char: int, *, source: str | None=None) -> None:
        self._content = content
        self._source = source
        self._offset_line = offset_line
        self._offset_char = offset_char

    def __repr__(self) -> str:
        return f'gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__({self._content!r}, line={self._offset_line}, char={self._offset_char})'

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

    def gAAAAABmn4MYRt8yLBH4jkx6BTT_VzoUrZ_nNp9pRAL6SOkkjVw5J4CDLVrnQ8LmlSdOrYqRHSAexxkFDIPpNRB_9CuQ0W5bXw__(self) -> gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__:
        return gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__([self])

    def gAAAAABmn4MYh_UzTYFzYYEALy2nWi1wJzqyt16h7JUfqZhJytjLl8BY10TO82bMXRsZcqJKimz5L212ONIc6ERjZmf6aMW5uQ__(self, /, start: PositiveInt | None, stop: None | PositiveInt=None) -> gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__:
        if self._offset_char is None:
            new_offset = None
        else:
            new_offset = self._offset_char + (start or 0)
        return gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__(self._content[start:stop], offset_line=self._offset_line, offset_char=new_offset, source=self._source)

    def rstrip(self) -> gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__:
        return gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__(self._content.rstrip(), offset_line=self._offset_line, offset_char=self._offset_char, source=self._source)

class gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__:
    __slots__ = ('_lines', '_current')

    def __init__(self, lines: Sequence[gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__]) -> None:
        self._lines = lines
        self._current: int = 0
        'The current line index,\n\n        Note it can never be negative, but can be greater than the number of lines.\n        '

    def __repr__(self) -> str:
        return f'gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__(lines={len(self._lines)}, index={self._current})'

    def gAAAAABmn4MYX16pqDitorWR8Tz1Q6cSgqYSppnPIItwkJTZxUhhW0mHgM3ad9ZMW1_KdiUg84Tp6EMD2j25XLY_NM4VXHsYAw__(self, *, newline: str='\n') -> str:
        return newline.join((line.content for line in self._lines[self._current:]))

    @property
    def is_empty(self) -> bool:
        return not self._lines[self._current:]

    def gAAAAABmn4MYOhdG3jdRtEl14WPRZCpCcMmJQpcmnswQsDsgyhnIlaFBEVJjImyefVR2nmNCYNl9kCrvNqXt1MlEf6S9iUHGag__(self) -> int:
        return len(self._lines[self._current:])

    @property
    def current_index(self) -> int:
        return self._current

    def gAAAAABmn4MYINuiuD2MpLdUpsj0dpofZ5MDZXGL24BtQUwkF6Y3v7Qw0g_1GxmzMe83cavfzpZNHPyOnrzsaRjMJdC4OkFNp9SWHVc4zdTzlh0_gOuBg2A_(self, index: int) -> None:
        self._current = index if index >= 0 else 0

    @property
    def current_line(self) -> None | gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__:
        try:
            return self._lines[self._current]
        except IndexError:
            return None

    @property
    def last_line(self) -> None | gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__:
        try:
            self._lines[self._current]
            return self._lines[-1]
        except IndexError:
            return None

    def gAAAAABmn4MYtQdD5Kq_sQq6lten_TCnNCIEv_zgwsDrry6cnx1S3_yD_NmuuuUl5oZoiPko9j_juDAmF9b5yuY6T1zdwux2MQ__(self) -> Iterable[gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__]:
        return iter(self._lines[self._current:])

    def gAAAAABmn4MYnuVsIy8PjL4QsZm7x_jIvuCslixFijnZNMDMLmL_y8yQ5R8jf2wQkfc_Kh5rwhyugQ0mYlWMW6isWf1Z5_w5bA__(self, n: int=1) -> None | gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__:
        try:
            return self._lines[self._current + n]
        except IndexError:
            return None

    def gAAAAABmn4MY7_HztNUURZlrnxk2NhikULgBA4AybqHWU01nsxIPst3zq_4s_kyqjuNVryFTiU_txpgHnG5K6pMeucdlm_pOQg__(self, n: int=1) -> None:
        self._current += n

    def gAAAAABmn4MY5R3t_pLcLit5TwdxnPh1jL5so6P4ttHG3N4aRj_ydeo299Mths_w_X4mn1GdsLyVYMr10MZb4pcJrhnHd3TqKA__(self, n: int=1) -> None:
        self._current -= n
        if self._current < 0:
            self._current = 0

    def gAAAAABmn4MYBPO5vpw99hwEDQsrFFm0nxHCAF1XBNo4m9p69ycMltQ3kbBqJoCj7klxeeRRQu7XULiTM2cHkLzE_hqQ3qH7GA__(self, top_offset: int, bottom_offset: int | None, /, *, start_offset: PositiveInt | None=None, stop_offset: PositiveInt | None=None, strip_min_indent: bool=False) -> gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__:
        new_lines: list[gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__] = []
        for line in self._lines[self._current + top_offset:None if bottom_offset is None else self._current + bottom_offset]:
            if start_offset is None and stop_offset is None:
                new_lines.append(line)
            else:
                new_lines.append(line.gAAAAABmn4MYh_UzTYFzYYEALy2nWi1wJzqyt16h7JUfqZhJytjLl8BY10TO82bMXRsZcqJKimz5L212ONIc6ERjZmf6aMW5uQ__(start_offset, stop_offset))
        if strip_min_indent:
            indents = [len(line.content) - len(line.content.lstrip()) for line in new_lines if not line.is_blank]
            if (min_indent := PositiveInt(min(indents, default=0))):
                new_lines = [line.gAAAAABmn4MYh_UzTYFzYYEALy2nWi1wJzqyt16h7JUfqZhJytjLl8BY10TO82bMXRsZcqJKimz5L212ONIc6ERjZmf6aMW5uQ__(min_indent) for line in new_lines]
        return self.__class__(new_lines)

    def gAAAAABmn4MYjOcyJS7Ldn32tRtXR6IwmXjGm_DVJ3LT5jhCkFGwbf9xT2HhZK978cjTJze42Q6ELwdxT4_4rHcg0jyLd5Q1lIvDIIlrRy1ZNwYs8Pzk_eQ_(self, *, start: bool=True, end: bool=True) -> gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__:
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

    def gAAAAABmn4MYN5fGTBtjkUSAK88BGCHj32eexJat8C6LIe2pvXYMPXoTllZAwHYRpp4BTBfoaXMXJA2YWPp1ccyLeYleLA4AkQ__(self, *, stop_on_indented: bool=False, advance: bool=False) -> gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__:
        new_lines: list[gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__] = []
        for line in self._lines[self._current:]:
            if line.is_blank:
                break
            if stop_on_indented and line.content[0] == ' ':
                break
            new_lines.append(line)
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines)

    def gAAAAABmn4MYfJDo9J_ycMh7R8RQfdK0OUS9Ype67eE4ZrkmvMCBaWLQL1T_am_FCLMqF09tKbE2DUL9Mov4eWuRKcjrocWdCg__(self, offset: int, until_blank: bool, /) -> Iterable[tuple[gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__, int | None]]:
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

    def gAAAAABmn4MY_yfqwBsRYQF3i6B4ejtA8c7PHNAe7ywGMgPEB1VSuXCI5XaNxcmX8C908AIn05EG2lE2SBQZbHS1EvFCVvXtNQ__(self, *, until_blank: bool=False, strip_indent: bool=True, advance: bool=False) -> gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__:
        new_lines: list[gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__] = []
        indents: list[int] = []
        for line, indent in self.gAAAAABmn4MYfJDo9J_ycMh7R8RQfdK0OUS9Ype67eE4ZrkmvMCBaWLQL1T_am_FCLMqF09tKbE2DUL9Mov4eWuRKcjrocWdCg__(0, until_blank):
            if indent is not None:
                indents.append(indent)
            new_lines.append(line)
        if strip_indent and indents:
            min_indent = PositiveInt(min(indents))
            new_lines = [line.gAAAAABmn4MYh_UzTYFzYYEALy2nWi1wJzqyt16h7JUfqZhJytjLl8BY10TO82bMXRsZcqJKimz5L212ONIc6ERjZmf6aMW5uQ__(min_indent) for line in new_lines]
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines)

    def gAAAAABmn4MYTNqh79EcKgIZUtho1Kao6oAD8EVSM5KD4rLEPjlwoKwyZEchGSn_5OmW27927rJos5kMsWi7KvfcXnwI6Q1nVyhmAoFv66P6LWRRR_Khesk_(self, *, first_indent: int=0, until_blank: bool=False, strip_indent: bool=True, strip_top: bool=True, strip_bottom: bool=False, advance: bool=False) -> gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__:
        first_indent = PositiveInt(first_indent)
        new_lines: list[gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__] = []
        indents: list[int] = []
        for line, indent in self.gAAAAABmn4MYfJDo9J_ycMh7R8RQfdK0OUS9Ype67eE4ZrkmvMCBaWLQL1T_am_FCLMqF09tKbE2DUL9Mov4eWuRKcjrocWdCg__(1, until_blank):
            if indent is not None:
                indents.append(indent)
            new_lines.append(line)
        if strip_indent and indents:
            min_indent = PositiveInt(min(indents))
            new_lines = [line.gAAAAABmn4MYh_UzTYFzYYEALy2nWi1wJzqyt16h7JUfqZhJytjLl8BY10TO82bMXRsZcqJKimz5L212ONIc6ERjZmf6aMW5uQ__(min_indent) for line in new_lines]
        if self.current_line is not None:
            new_lines.insert(0, self.current_line.gAAAAABmn4MYh_UzTYFzYYEALy2nWi1wJzqyt16h7JUfqZhJytjLl8BY10TO82bMXRsZcqJKimz5L212ONIc6ERjZmf6aMW5uQ__(first_indent))
        if new_lines and advance:
            self._current += len(new_lines) - 1
        block = self.__class__(new_lines)
        if strip_top or strip_bottom:
            return block.gAAAAABmn4MYjOcyJS7Ldn32tRtXR6IwmXjGm_DVJ3LT5jhCkFGwbf9xT2HhZK978cjTJze42Q6ELwdxT4_4rHcg0jyLd5Q1lIvDIIlrRy1ZNwYs8Pzk_eQ_(start=strip_top, end=strip_bottom)
        return block

    def gAAAAABmn4MYFItSm7lWpwX1tP488ltMcGqRC94H5RK1FKb_T0CzSvzyL1SXZdRN8yB9rjxzFrgOHfaFhzc9_D5YWUIHsKTUO_hXzsYAqM2wEIvFjzzD_WY_(self, indent: int, *, always_first: bool=False, until_blank: bool=False, strip_indent: bool=True, advance: bool=False) -> gAAAAABmn4MYGGv8Lses9Tn7AEcFB9EnCRxEdf3F9sChB5KuWfuePkdB4dY2KUm_01sVLbiVJOLwCLrIuB_5lr1Ibw5TpDjwYQ__:
        indent = PositiveInt(indent)
        new_lines: list[gAAAAABmn4MYUmNZk6z6yxNVtCCbYuhNiM02dsnxLNm7OAHrUMydKKihG_0kWykDgn1DDtUfC_PIIJ_5feVtXaVaA_XunzG5_g__] = []
        line_index = self._current
        if always_first:
            if (line := self.current_line):
                new_lines.append(line.gAAAAABmn4MYh_UzTYFzYYEALy2nWi1wJzqyt16h7JUfqZhJytjLl8BY10TO82bMXRsZcqJKimz5L212ONIc6ERjZmf6aMW5uQ__(indent))
            line_index += 1
        for line in self._lines[line_index:]:
            len_total = len(line.content)
            len_indent = len_total - len(line.content.lstrip())
            if len_total != 0 and len_indent < indent:
                break
            if until_blank and len_total == len_indent:
                break
            new_lines.append(line.gAAAAABmn4MYh_UzTYFzYYEALy2nWi1wJzqyt16h7JUfqZhJytjLl8BY10TO82bMXRsZcqJKimz5L212ONIc6ERjZmf6aMW5uQ__(indent) if strip_indent else line)
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines).gAAAAABmn4MYjOcyJS7Ldn32tRtXR6IwmXjGm_DVJ3LT5jhCkFGwbf9xT2HhZK978cjTJze42Q6ELwdxT4_4rHcg0jyLd5Q1lIvDIIlrRy1ZNwYs8Pzk_eQ_(start=True, end=False)