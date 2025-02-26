from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def generate_pdf_fark(products, categories):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []
    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.fontName = "DejaVuSans"
    elements.append(Paragraph("Ürün Fiyat Farkı Raporu", title_style))

    data = [["Ürün Adı", "Kategori", "Fiyat (USD)", "Orjinal Fiyat (USD)", "Fark"]]

    for p in products:
        category = categories.get(p["name"], "Belirtilmedi")
        orjinal_fiyat = p.get("orjinal_fiyat", 0)

        # Fiyatların geçerli olup olmadığını kontrol et
        price = p["price"] if p["price"] is not None else "Bilinmiyor"
        orjinal_fiyat = orjinal_fiyat if orjinal_fiyat is not None else "Bilinmiyor"

        if price != "Bilinmiyor" and orjinal_fiyat != "Bilinmiyor":
            try:
                price_float = float(price)
                orjinal_fiyat_float = float(orjinal_fiyat)
                fark = price_float - orjinal_fiyat_float  # Fiyat farkı hesapla
                fark_str = f"{fark:.2f}"
            except ValueError:
                fark_str = "Bilinmiyor"
        else:
            fark_str = "Bilinmiyor"

        data.append([p["name"], category, str(price), str(orjinal_fiyat), fark_str])

    # Tabloyu oluştur
    table = Table(
        data, colWidths=(1.5 * inch, 1.5 * inch, 1.5 * inch, 1.5 * inch, 1.5 * inch)
    )

    # Tabloya stil ekle
    table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.20, colors.dimgrey),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    "DejaVuSans",
                ),
                ("INNERGRID", (0, 0), (-1, -1), 0.1, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4B8BBE")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ],
        ),
    )

    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer
