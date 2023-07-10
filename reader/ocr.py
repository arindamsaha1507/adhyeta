"""Module to test the OCR API from Google Cloud Vision."""

import os

from typing import Optional

from google.cloud import vision


def write_text_to_file(texts: list[str], out_path: str, append: bool = False):
    """Writes the text to a file."""

    with open(out_path, "a" if append else "w", encoding="utf-8") as file:
        for text in texts:
            file.write(f'\n"{text.description}"')


def ocr_single(in_path: str, out_path: Optional[str] = None, append: bool = False):
    """Detects text in a single image."""

    client = vision.ImageAnnotatorClient()

    with open(in_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)  # pylint: disable=no-member
    texts = response.text_annotations

    if out_path:
        write_text_to_file(texts, out_path, append)

    if response.error.message:
        raise RuntimeError(
            f"{response.error.message}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors"
        )


def ocr_bulk(in_dir: str, out_path: str):
    """Detects text in directory."""

    os.makedirs(out_path, exist_ok=True)

    for i, image_path in enumerate(sorted(os.listdir(in_dir))):
        print(f"Processing image {i+1}...")
        in_file = os.path.join(in_dir, image_path)
        out_file = os.path.join(out_path, image_path.replace(".png", ".txt"))
        ocr_single(in_file, out_file)
