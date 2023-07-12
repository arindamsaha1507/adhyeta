"""The main module."""

import os

from reader.extract_pages import convert_book_to_images
from reader.ocr import ocr_bulk


def main():
    """The main function."""

    book_directory = "books_pdf"
    image_directory = "output_images"
    # raw_text_directory = "raw_text"

    for book in os.listdir(book_directory):
        print(f"Processing book {book}...")

        book_path = os.path.join(book_directory, book)
        book_name = book.replace(".pdf", "")

        book_image_directory = os.path.join(image_directory, book_name)
        # book_raw_text_directory = os.path.join(raw_text_directory, book_name)

        convert_book_to_images(book_path, book_image_directory)

        # ocr_bulk(book_image_directory, book_raw_text_directory)
        ocr_bulk(book_image_directory)


if __name__ == "__main__":
    main()
