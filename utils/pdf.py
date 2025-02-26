import re
import fitz  # PyMuPDF
from PIL import Image

def extract_text_from_pdf_page(page):
    return page.get_text()


def extract_product_info(text):
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    possible_names = [line for line in lines if line.isupper() or len(line) > 10]
    price_pattern = r"\b(?:USD\s*)?\$?(\d{1,5}(?:[,\.]\d{1,2})?)\b"
    possible_prices = re.findall(price_pattern, text)
    possible_prices = [p.replace(",", ".") for p in possible_prices]
    return possible_names, possible_prices


def pdf_to_images(pdf_bytes, page_limit):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    images = []
    for page_num in range(min(page_limit, doc.page_count)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=150)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images
