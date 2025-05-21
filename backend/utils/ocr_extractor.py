import os
import fitz  # PyMuPDF
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image
import pdfplumber

def is_pdf(filepath):
    return filepath.lower().endswith(".pdf")

def is_image(filepath):
    return filepath.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp"))

def extract_text(filepath):
    if is_pdf(filepath):
        return extract_from_pdf(filepath)
    elif is_image(filepath):
        return extract_from_image(filepath)
    else:
        raise ValueError("Unsupported file type")

def extract_from_pdf(filepath):
    text = ""
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"[pdfplumber] Failed: {e}")

    if not text.strip():
        print("No text found with pdfplumber — trying OCR with PyMuPDF")
        doc = fitz.open(filepath)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text += pytesseract.image_to_string(img)

    return text.strip()

def extract_from_image(filepath):
    try:
        img = Image.open(filepath)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        print(f"Error during OCR on image: {e}")
        return ""
