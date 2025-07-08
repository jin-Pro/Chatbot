import fitz  # PyMuPDF
from PIL import Image
import pytesseract

def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = "\n".join([page.get_text() for page in doc])
    return text

def extract_images_from_pdf(file_path: str) -> list:
    doc = fitz.open(file_path)
    image_paths = []

    for page_index in range(len(doc)):
        for img_index, img in enumerate(doc.get_page_images(page_index)):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:  # not CMYK
                image_path = f"/tmp/page{page_index + 1}_img{img_index + 1}.png"
                pix.save(image_path)
                image_paths.append(image_path)
            pix = None

    return image_paths

def extract_text_from_images(image_paths: list, lang: str = "kor") -> str:
    all_text = ""
    for path in image_paths:
        img = Image.open(path)
        text = pytesseract.image_to_string(img, lang=lang)
        all_text += text + "\n"
    return all_text