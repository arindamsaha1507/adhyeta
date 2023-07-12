"""Module to store classes of text directly read from a PDF book."""

from dataclasses import dataclass


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
        return self.text.split()

    @property
    def word_count(self) -> int:
        """Number of words in the text box."""
        return len(self.words)
