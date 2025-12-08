import fitz  # PyMuPDF

def pdf_to_images(pdf_bytes: bytes, max_pages: int = 5) -> list[bytes]:
    """
    Convert the first `max_pages` of a PDF into JPEG image bytes.

    Returns:
        A list of raw JPEG bytes.
    """
    images = []
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    for i in range(min(len(doc), max_pages)):
        page = doc.load_page(i)
        pix = page.get_pixmap(dpi=200)  # good balance for OCR
        img_bytes = pix.tobytes("jpeg")
        images.append(img_bytes)

    return images
