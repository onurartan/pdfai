import re
import fitz  # PyMuPDF
from PIL import Image



def extract_text_from_pdf_page(page):
    return page.get_text()


# def extract_product_info(text):
#     lines = [line.strip() for line in text.split("\n") if line.strip()]
#     possible_names = [line for line in lines if line.isupper() or len(line) > 10]
#     price_pattern = r"\b(?:USD\s*)?\$?(\d{1,5}(?:[,\.]\d{1,2})?)\b"
#     possible_prices = re.findall(price_pattern, text)
#     possible_prices = [p.replace(",", ".") for p in possible_prices]
#     return possible_names, possible_prices


def extract_product_info(text, page):
    # Ürün isimlerini bul
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    possible_names = [line for line in lines if line.isupper() or len(line) > 10]

    # Fiyatları ve konumlarını bul
    price_pattern = r"\b(?:USD\s*)?\$?(\d{1,5}(?:[,\.]\d{1,2})?)\b"
    possible_prices_raw = re.findall(price_pattern, text)
    possible_prices = [p.replace(",", ".") for p in possible_prices_raw]

    # Fiyatların PDF içindeki konumlarını bul
    price_locations = []
    for price in possible_prices_raw:
        rects = page.search_for(price)  # PyMuPDF ile fiyatın konumunu bul
        if rects:  # Eğer fiyat sayfada bulunursa
            price_locations.append({"price": price.replace(",", "."), "rect": rects[0]})

    return possible_names, price_locations

def pdf_to_images(pdf_bytes, page_limit):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    images = []
    for page_num in range(min(page_limit, doc.page_count)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=150)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images
