"""Module to test the OCR API from Google Cloud Vision."""

import os

from typing import Optional, Any

from google.cloud import vision

from reader.text import Text, TextBox


def store_text(book: str, texts: list[Any], page: int) -> list[Text]:
    """Stores the text in a list of Text objects."""

    components = []

    for text in texts:
        vertices = text.bounding_poly.vertices
        box = TextBox(
            top_left=(vertices[0].x, vertices[0].y),
            top_right=(vertices[1].x, vertices[1].y),
            bottom_left=(vertices[2].x, vertices[2].y),
            bottom_right=(vertices[3].x, vertices[3].y),
        )

        components.append(
            Text(
                book=book,
                page=page,
                text=text.description,
                box=box,
            ),
        )

    print(f"Stored {len(components)} text components from page {page} of {book}.")
    return components


def write_text_to_file(texts: list[str], out_path: str, append: bool = False) -> None:
    """Writes the text to a file."""

    with open(out_path, "a" if append else "w", encoding="utf-8") as file:
        for text in texts:
            file.write(f'\n"{text.description}"')


def ocr_single(
    in_path: str, out_path: Optional[str] = None, append: bool = False
) -> None | list[Text]:
    """Detects text in a single image."""

    client = vision.ImageAnnotatorClient()

    with open(in_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)  # pylint: disable=no-member
    texts = response.text_annotations

    if out_path:
        write_text_to_file(texts, out_path, append)
        return None

    book = in_path.split("/")[-2]
    page = in_path.split("/")[-1].replace(".png", "")
    page_num = int(page.split("_")[-1])
    components = store_text(book, texts, page_num)
    return components


def ocr_bulk(
    in_dir: str, out_path: Optional[str] = None, limit: Optional[int] = None
) -> None:
    """Detects text in directory."""

    if out_path:
        os.makedirs(out_path, exist_ok=True)

    print(f"OCR-ing images in {in_dir}...")

    image_paths = sorted(os.listdir(in_dir))

    if limit:
        image_paths = image_paths[:limit]

    for image_path in image_paths:
        in_file = os.path.join(in_dir, image_path)
        if out_path:
            out_file = os.path.join(out_path, image_path.replace(".png", ".txt"))
            ocr_single(in_file, out_file)
        else:
            ocr_single(in_file)
