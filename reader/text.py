"""Module to store classes of text directly read from a PDF book."""

from enum import Enum
from dataclasses import dataclass, field
import re
from typing import Optional

import akshara.varnakaarya as vk


class Languages(Enum):
    """Languages supported by Google Cloud Vision."""

    ENGLISH = "en"
    SANSKRIT = "sa"
    OTHER = "und"


@dataclass
class TextBox:
    """Class to store a text box identified by ocr."""

    top_left: tuple
    top_right: tuple
    bottom_left: tuple
    bottom_right: tuple

    @property
    def width(self) -> int:
        """Width of the text box."""
        return abs(self.top_right[0] - self.top_left[0])

    @property
    def height(self) -> int:
        """Height of the text box."""
        return abs(self.bottom_left[1] - self.top_left[1])

    @property
    def area(self) -> int:
        """Area of the text box."""
        return self.width * self.height

    @property
    def location(self) -> tuple:
        """Location of the text box."""
        return (self.top_left[0], self.top_left[1])


@dataclass
class Text:
    """Class to store text directly read from a PDF book."""

    book: str
    page: int
    text: str
    box: TextBox

    @property
    def words(self) -> list[str]:
        """Words in the text box."""
        return self.text.split(" ")

    @property
    def word_count(self) -> int:
        """Number of words in the text box."""
        return len(self.words)

    def __repr__(self) -> str:
        string = f"Book: {self.book}; Page: {self.page}; Word Count: "
        string += f"{self.word_count}; Box Height: {self.box.height}; "
        string += f"Box Location: {self.box.location}"
        return string


@dataclass
class Word:
    """Class to store a word identified by ocr."""

    text: Text
    raw: str = field(init=False)
    language: Languages = field(init=False)
    vinyaasa: Optional[list[str]] = field(init=False)
    moola: bool = field(init=False)
    line: int = field(init=False)

    def __post_init__(self) -> None:
        if self.text.word_count > 1:
            raise ValueError("Word should have only one word.")

        self.raw = self.text.text

        if re.search("[a-zA-Z]", self.raw) or re.search("[0-9]", self.raw):
            self.language = Languages.ENGLISH
            self.vinyaasa = None
            return

        self.language = Languages.SANSKRIT
        try:
            self.vinyaasa = vk.get_vinyaasa(self.raw)
        except AssertionError:
            self.vinyaasa = self.raw
        self.moola = False

    @property
    def size(self) -> int:
        """Size of the text box."""
        return self.text.box.height

    @property
    def location(self) -> tuple:
        """Location of the text box."""
        return self.text.box.location


def get_lines(words: list[Word]) -> None:
    """Identifies the number of words in each line."""

    current_line = 1
    current_location = words[0].location[1]
    for word in words:
        if abs(word.location[1] - current_location) > word.size:
            current_line += 1
            current_location = word.location[1]
        word.line = current_line
