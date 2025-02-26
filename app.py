import streamlit as st
import fitz  # PyMuPDF
import re
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from utils.generate_pdf import generate_pdf
from utils.generate_pdf_fark import generate_pdf_fark

from utils.pdf import extract_product_info, extract_text_from_pdf_page, pdf_to_images

from utils.apply_percentage import apply_percentage
from config import DEJAVUFONT_PATH

pdfmetrics.registerFont(TTFont("DejaVuSans", DEJAVUFONT_PATH))


def main():
    st.title("PDF Ürün Fiyat Analizi")

    uploaded_file = st.file_uploader("PDF dosyanızı yükleyin", type="pdf")

    if uploaded_file:
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        total_pages = doc.page_count
        st.write(f"Toplam Sayfa: {total_pages}")
        page_limit = st.slider(
            "Kaç sayfa analiz edilsin?",
            0,
            total_pages,
            min(4, total_pages) if total_pages > 1 else 1,
        )

        percentage = st.number_input(
            "Fiyata eklenecek yüzde oranı (negatif değer indirim için):",
            value=5.0,
            step=0.5,
            format="%.2f",
        )
        category_input = st.text_area(
            "Kategorileri Virgülle Ayrılmış Olarak Girin (Örn: Elektronik, Giyim, Yiyecek):"
        )

        if category_input:
            global_category_options = [
                category.strip() for category in category_input.split(",")
            ]
        else:
            global_category_options = []

        images = pdf_to_images(pdf_bytes, page_limit)
        products = []
        categories = {}

        st.divider()

        for idx, img in enumerate(images):
            page = doc.load_page(idx)
            text = extract_text_from_pdf_page(page)
            possible_names, possible_prices = extract_product_info(text)

            st.subheader(f"Sayfa {idx + 1}")
            st.image(img, caption=f"Sayfa {idx + 1}", use_container_width=True)

            num_products = st.number_input(
                f"Bu sayfadaki ürün sayısı",
                min_value=1,
                max_value=5,
                value=1,
                key=f"num_products_{idx}",
            )

            for i in range(num_products):
                selected_name = st.selectbox(
                    f"Ürün {i+1} Adı", possible_names, index=0, key=f"name_{idx}_{i}"
                )
                selected_price = st.selectbox(
                    f"Ürün {i+1} Fiyatı",
                    possible_prices,
                    index=2,
                    key=f"price_{idx}_{i}",
                )

                selected_category = st.selectbox(
                    f"Ürün {i+1} Kategorisi",
                    global_category_options,
                    key=f"category_{idx}_{i}",
                )

                add_page_products = st.radio(
                    "Rapora bu ürün eklensin mi?",
                    key=f"addPage_eklensinmi_checkbox_{idx}_{i}",
                    options=["Evet", "Hayır"],
                    index=0,
                )
                add_page_products = add_page_products == "Evet"

                if selected_price:
                    final_price = apply_percentage(selected_price, percentage)
                else:
                    final_price = "Bilinmiyor"

                if add_page_products == False:
                    continue

                categories[selected_name] = selected_category
                products.append(
                    {
                        "name": selected_name,
                        "price": final_price,
                        "orjinal_fiyat": selected_price,
                    }
                )

            st.divider()
        pdf_report = generate_pdf(products, categories)

        st.subheader("PDF Raporu Oluşturuldu")

        pdf_image = pdf_to_images(pdf_report, 2)[0]

        st.image(pdf_image, caption="Ön İzleme", use_container_width=True)

        st.download_button(
            "PDF Raporunu İndir",
            data=pdf_report,
            file_name="urun_fiyat_raporu.pdf",
            mime="application/pdf",
        )

        st.divider()

        pdf_fark_report = generate_pdf_fark(products, categories)

        st.download_button(
            "Fiyat Farkı Raporunu PDF olarak indir",
            data=pdf_fark_report,
            file_name="urun_fiyat_fark_raporu.pdf",
            mime="application/pdf",
        )


if __name__ == "__main__":
    main()
