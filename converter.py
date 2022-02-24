import os.path
import cv2
import pytesseract
from os import listdir
from os.path import isfile, join

from progressbar import SingleProgressBar

IMAGE_DIR = 'images/'
TEXT_DIR = 'text/'


def convert_image_to_text(image_path: str, text_path: str) -> str:
    os.makedirs(text_path[:text_path.rindex('/')], exist_ok=True)
    with open(text_path, 'w', encoding='utf-8') as file:
        text = pytesseract.image_to_string(cv2.imread(image_path), "eng+ukr")
        file.write(text)
        return text


def get_image_text(image: str) -> str:
    """
    Returns text in image
    """
    text_path = f"{TEXT_DIR}/{image}.txt"
    if os.path.exists(text_path):
        with open(text_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        return convert_image_to_text(f"{IMAGE_DIR}/{image}.jpeg", text_path)


def convert_all_images(show_progress: bool = False) -> str:
    """
    Converts all images to text
    """
    files = [f[:f.rindex('.')] for f in listdir(IMAGE_DIR) if isfile(join(IMAGE_DIR, f))]
    return '\n'.join([get_image_text(file) for file in SingleProgressBar(files)])
