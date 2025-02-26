from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def generate_pdf(products, categories):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []
    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.fontName = "DejaVuSans"
    elements.append(Paragraph("Ürün Fiyat Raporu", title_style))

    data = [["Ürün Adı", "Kategori", "Fiyat (USD)"]]

    for p in products:
        category = categories.get(p["name"], "Belirtilmedi")
        data.append([p["name"], category, str(p["price"])])

    table = Table(
        data,
        colWidths=(2.5 * inch, 2.5 * inch, 2.5 * inch),
    )

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
            ]
        )
    )

    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer
