"""Module to extract each page of a PDF book as a separate image."""

import os
import shutil

from pdf2image import convert_from_path


def convert_book_to_images(book_path, output_dir):
    """Convert each page of a PDF book to a separate image."""

    if not os.path.exists(book_path):
        raise FileNotFoundError(f"File {book_path} does not exist.")

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    os.makedirs(output_dir, exist_ok=True)

    print(f"Reading book from {book_path}...")

    images = convert_from_path(book_path)

    print(f"Saving pages from {book_path}...")

    str_len = len(str(len(images)))

    for i, image in enumerate(images):
        output_file = os.path.join(output_dir, f"page_{str(i+1).zfill(str_len)}.png")
        image.save(output_file, "PNG")

    print(f"Extracted {len(images)} pages to {output_dir}.")


def main():
    """The main function."""

    book_path = "book.pdf"
    output_dir = "output_images"
    convert_book_to_images(book_path, output_dir)


if __name__ == "__main__":
    main()
