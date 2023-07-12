"""The main module."""

import os

from reader.extract_pages import convert_book_to_images
from reader.ocr import ocr_bulk
from reader.text import Text, Word


def write_text_to_file(texts: list[Text], out_path: str) -> None:
    """Writes the text to a file."""

    with open(out_path, "w", encoding="utf-8") as file:
        for word in texts:
            file.write(
                f"{word.book}\t{word.page}\t{word.box.height}\t{word.box.location}\t"
            )

            if len(word.text) > 50:
                file.write(f"{word.text[:50]}...\n")
            else:
                file.write(f"{word.text}\n")


def write_words_to_file(words: list[Word], out_path: str) -> None:
    """Writes the word to a file."""

    with open(out_path, "w", encoding="utf-8") as file:
        for word in words:
            file.write(
                f"{word.location}\t{word.size}\t{word.language}\t{word.raw}\t{word.vinyaasa if word.vinyaasa else ''}\n"
            )


def main():
    """The main function."""

    book_directory = "books_pdf"
    image_directory = "output_images"

    for book in os.listdir(book_directory):
        print(f"Processing book {book}...")

        book_path = os.path.join(book_directory, book)
        book_name = book.replace(".pdf", "")

        book_image_directory = os.path.join(image_directory, book_name)

        if os.path.exists(book_image_directory):
            print(f"Images for {book} already exist.")
        else:
            convert_book_to_images(book_path, book_image_directory)

        texts = ocr_bulk(book_image_directory, limit=6)

        texts = [text for text in texts if text.word_count == 1]

        words = [Word(text) for text in texts]

        write_words_to_file(words, f"raw_text/{book_name}.txt")


if __name__ == "__main__":
    main()
