from io import BytesIO
import fitz
from config import DEJAVUFONT_PATH
from utils.convert import usd_to_try

def update_pdf_with_prices(pdf_bytes, products, price_locations, page_limit):

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    font_name = "DejaVuSans"

    new_doc = fitz.open()

    for idx in range(page_limit):
        if idx >= len(doc):
            break

        page = doc[idx]
        new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
        new_page.show_pdf_page(page.rect, doc, idx)

        new_page.insert_font(fontname=font_name, fontfile=DEJAVUFONT_PATH)
        font = fitz.Font(fontname=font_name, fontfile=DEJAVUFONT_PATH)

        # Fiyat güncellemelerini yap
        if idx < len(price_locations) and price_locations[idx]:
            for product in products:
                old_price = product["orjinal_fiyat"]
                new_price = product["price"]
                for loc in price_locations[idx]:
                    if loc["price"] == old_price:
                        rect = loc["rect"]

                        new_page.draw_rect(
                            rect, color=(0.76, 0.15, 0.18), fill=(0.76, 0.15, 0.18)
                        )

                        # Yeni fiyatı yaz
                        price_text = f"{usd_to_try(new_price)}"
                        tw = font.text_length(price_text, fontsize=13)
                        ascent = font.ascender
                        descent = font.descender
                        font_scale = 15 / 1000
                        th = (ascent - descent) * font_scale

                        x_center = rect.x0 + (rect.width - tw) / 2
                        y_center = rect.y0 + (rect.height - th) / 2

                        new_page.insert_text(
                            (x_center, y_center),
                            price_text,
                            fontname=font_name,
                            fontsize=13,
                            color=(1, 1, 1),
                        )

                        tl_rect = fitz.Rect(rect.x0, rect.y1, rect.x1 + 10, rect.y1 + 20)
                        new_page.draw_rect(tl_rect, color=(1, 1, 1), fill=(0.76, 0.15, 0.18))
                        tl_text = "TL"
                        tl_tw = font.text_length(tl_text, fontsize=10)
                        tl_th = (font.ascender - font.descender) * (10 / 1000)
                        tl_x_center = tl_rect.x0 + (tl_rect.width - tl_tw) / 2
                        tl_y_center = tl_rect.y0 + (tl_rect.height - tl_th) / 2
                        new_page.insert_text(
                            (tl_x_center, tl_y_center +3),
                            tl_text,
                            fontname=font_name,
                            fontsize=10,
                            color=(1, 1, 1),
                        )

    buffer = BytesIO()
    new_doc.save(buffer)
    new_doc.close()
    buffer.seek(0)
    return buffer
