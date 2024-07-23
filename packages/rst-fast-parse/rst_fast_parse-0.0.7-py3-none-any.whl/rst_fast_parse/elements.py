from __future__ import annotations

from typing import Iterable, Iterator, Literal, Protocol, Sequence

from typing_extensions import TypeAlias

BlockTagName: TypeAlias = Literal[
    "document",
    "transition",
    "title_overline",
    "title_underline",
    "paragraph",
    "blockquote",
    "literal_block",
    "line_block",
    "doctest",
    "bullet_list",
    "enum_list",
    "definition_list",
    "field_list",
    "option_list",
    "anonymous_target",
    "link_target",
    "footnote",
    "citation",
    "substitution_def",
    "directive",
    "comment",
    "table_simple",
    "table_grid",
]


class ElementBase(Protocol):
    @property
    def tagname(self) -> BlockTagName:
        """The tag name of the element."""

    @property
    def line_range(self) -> tuple[int, int]:
        """The line range of the element in the source.
        (index-based, starting from 0)
        """

    def debug_repr(self, indent: int) -> str:
        """Return a debug representation of the element.

        This takes the form of psuedo-XML, with the tag name and line range.
        """


class ElementListBase(Protocol):
    """A list of elements in the document.

    It is assumed that the elements are in order of appearance in the source,
    and that the line ranges of the elements do not overlap.
    """

    def debug_repr(self, indent: int) -> str:
        """Return a debug representation of the list of elements."""

    def __iter__(self) -> Iterator[ElementBase]: ...

    def __getitem__(self, index: int, /) -> ElementBase: ...

    def append(self, element: ElementBase) -> None: ...

    def line_inside(self, line: int) -> Iterable[ElementBase]:
        """Return all elements that contain the given line."""


class BasicElementList(Sequence[ElementBase]):
    def __init__(self) -> None:
        self._elements: list[ElementBase] = []

    def debug_repr(self, indent: int) -> str:
        text = ""
        for element in self._elements:
            text += element.debug_repr(indent) + "\n"
        return text

    def __getitem__(self, index: int, /) -> ElementBase:  # type: ignore[override]
        return self._elements[index]

    def __len__(self) -> int:
        return len(self._elements)

    def append(self, element: ElementBase) -> None:
        self._elements.append(element)

    def line_inside(self, line: int) -> Iterable[ElementBase]:
        """Return all elements that contain the given line, in order of nesting."""
        for element in self._elements:
            if element.line_range[0] <= line <= element.line_range[1]:
                yield element
                # TODO iterate over nested items
            if element.line_range[1] > line:
                break


class BasicElement:
    """A generic element in the document tree."""

    __slots__ = ("_tagname", "_line_range")

    def __init__(self, tagname: BlockTagName, line_range: tuple[int, int]) -> None:
        """
        :param tagname: The tag name of the element.
        :param line_range: The line range of the element in the source.
            (index-based, starting from 0)
        """
        self._tagname = tagname
        self._line_range = line_range

    def __repr__(self) -> str:
        return f"Element({self._tagname!r}, {self._line_range})"

    def debug_repr(self, indent: int) -> str:
        return f"{' ' * indent}<{self._tagname}> {self._line_range[0]}-{self._line_range[1]}"

    @property
    def tagname(self) -> BlockTagName:
        return self._tagname

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range


class ListItemElement:
    """A generic element in the document tree."""

    __slots__ = ("_line_range",)

    def __init__(self, line_range: tuple[int, int]) -> None:
        """
        :param line_range: The line range of the element in the source.
            (index-based, starting from 0)
        """
        self._line_range = line_range

    def __repr__(self) -> str:
        return f"ListItemElement({self._line_range})"

    def debug_repr(self, indent: int) -> str:
        return f"{' ' * indent}<list_item> {self._line_range[0]}-{self._line_range[1]}"

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range


class ListElement:
    """A list element in the document tree."""

    __slots__ = ("_tagname", "_items")

    def __init__(self, tagname: BlockTagName, items: list[ListItemElement]) -> None:
        """
        :param tagname: The tag name of the element.
        :param line_range: The line range of the element in the source.
            (index-based, starting from 0)
        :param items: The list of items in the list.
        """
        self._tagname = tagname
        self._items = items

    def __repr__(self) -> str:
        return f"ListElement({self._tagname!r}, len={len(self.items)})"

    def debug_repr(self, indent: int) -> str:
        text = (
            f"{' ' * indent}<{self._tagname}> {self.line_range[0]}-{self.line_range[1]}"
        )
        for item in self._items:
            text += "\n" + item.debug_repr(indent + 2)
        return text

    @property
    def tagname(self) -> BlockTagName:
        return self._tagname

    @property
    def line_range(self) -> tuple[int, int]:
        return (self._items[0].line_range[0], self._items[-1].line_range[1])

    @property
    def items(self) -> list[ListItemElement]:
        return self._items


class TransitionElement:
    __slots__ = ("_style", "_line_range")

    def __init__(self, style: str, line_range: tuple[int, int]) -> None:
        self._style = style
        self._line_range = line_range

    def __repr__(self) -> str:
        return f"Element({self.tagname!r}, {self._line_range})"

    def debug_repr(self, indent: int) -> str:
        return (
            f"{' ' * indent}<{self.tagname}> {self.line_range[0]}-{self.line_range[1]}"
        )

    @property
    def tagname(self) -> BlockTagName:
        return "transition"

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    @property
    def style(self) -> str:
        return self._style


class TitleElement:
    __slots__ = ("_overline", "_style", "_title", "_line_range")

    def __init__(
        self, overline: bool, style: str, title: str, line_range: tuple[int, int]
    ) -> None:
        self._overline = overline
        self._style = style
        self._title = title
        self._line_range = line_range

    def __repr__(self) -> str:
        return f"Element({self.tagname!r}, {self._line_range})"

    def debug_repr(self, indent: int) -> str:
        return (
            f"{' ' * indent}<{self.tagname}> {self.line_range[0]}-{self.line_range[1]}"
        )

    @property
    def tagname(self) -> BlockTagName:
        return "title_overline" if self._overline else "title_underline"

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    @property
    def style(self) -> str:
        return self._style

    @property
    def overline(self) -> bool:
        return self._overline

    @property
    def title(self) -> str:
        return self._title


class DirectiveElement:
    __slots__ = ("_name", "_line_range")

    def __init__(self, name: str, line_range: tuple[int, int]) -> None:
        self._name = name
        self._line_range = line_range

    def __repr__(self) -> str:
        return f"Element({self.tagname!r}, {self._line_range})"

    def debug_repr(self, indent: int) -> str:
        return (
            f"{' ' * indent}<{self.tagname}> {self.line_range[0]}-{self.line_range[1]}"
        )

    @property
    def tagname(self) -> BlockTagName:
        return "directive"

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    @property
    def name(self) -> str:
        return self._name
