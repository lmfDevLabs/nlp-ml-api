import io
import requests
import pdfplumber

# other utils
from app.utilities.text_processing_utils import split_text_into_paragraphs
from app.utilities.text_processing_utils import chunk_paragraphs

# Función para extraer texto de un PDF usando pdfplumber
def extract_text_from_pdf(pdf_bytes):
    print("extract_text_from_pdf")
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error al procesar el PDF: {e}")
    return text

# Verificar si la URL es válida
def is_valid_url(url):
    print("is_valid_url")
    return url and url.lower() != "nan"

# Función para procesar el PDF desde la URL
def process_pdf_url(pdf_url):
    print("process_pdf_url")
    if not is_valid_url(pdf_url):
        return None, "URL no válida"

    try:
        response = requests.get(pdf_url)
        if response.status_code == 200:
            pdf_text = extract_text_from_pdf(response.content)
            return pdf_text, "Procesado con éxito"
        else:
            return None, f"Error al descargar el PDF: {response.status_code}"
    except Exception as e:
        return None, f"Error al descargar el PDF: {e}"

# Función para procesar el texto del PDF
def process_pdf_text(pdf_text):
    print("process_pdf_text")
    paragraphs = split_text_into_paragraphs(pdf_text)
    chunks = chunk_paragraphs(paragraphs)
    return chunks
