import os
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def get_dejavu_font_path():
    project_root = os.path.dirname(os.path.abspath(__file__))
    dejavu_font_path = os.path.join(project_root, 'fonts', 'DejaVuSans.ttf')
    
    if os.path.exists(dejavu_font_path):
        return dejavu_font_path
    else:
        raise FileNotFoundError(f"Font dosyası bulunamadı: {dejavu_font_path}")



def register_font():
    try:
        dejavu_font_path = get_dejavu_font_path() 
        pdfmetrics.registerFont(TTFont("DejaVuSans", dejavu_font_path))
        print(f"Font başarıyla kaydedildi: {dejavu_font_path}")
    except FileNotFoundError as e:
        print(e)

DEJAVUFONT_PATH = get_dejavu_font_path()