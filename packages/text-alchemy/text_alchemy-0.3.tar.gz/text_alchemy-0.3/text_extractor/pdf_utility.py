import csv
import hashlib
import io

import fitz
import magic
import pandas as pd
import requests
from pdf2image import convert_from_bytes
from PIL import Image

from text_extractor.vision import GoogleVisionAPI


def is_short_message(message):
    return len(message) < 200


class PdfUtils:
    google_api_key = None

    def __init__(self, google_api_key=None) -> None:
        if google_api_key:
            PdfUtils.google_api_key = google_api_key

    @classmethod
    def get_png_from_pdf(cls, pdf):
        images = convert_from_bytes(pdf)

        if len(images) == 1:
            image = images[0]
        else:
            widths, heights = zip(*(i.size for i in images))

            max_width = max(widths)
            total_height = sum(heights)
            image = Image.new("RGB", (max_width, total_height))

            y_offset = 0
            change_in_height = 0
            for index, im in enumerate(images):
                pixels = im.load()
                if index == len(images) - 1:
                    # Last image, crop extra whitespace. Start from bottom and stop at first non-white pixel
                    y = im.height - 1
                    while y > 0:
                        if any(pixels[x, y] != (255, 255, 255) for x in range(im.width - 1)):
                            break
                        y -= 1

                    change_in_height = im.height - y - 25  # Keeping 25 pixel padding

                image.paste(im, (0, y_offset))
                y_offset += im.size[1]
            if change_in_height:
                image = image.crop((0, 0, image.width, image.height - change_in_height - 5))

        return image

    @classmethod
    def extract_text_from_pdf(cls, file_content, direct_convert=False):
        if direct_convert:
            pdf_text = ""
            pdf_document = fitz.open(stream=file_content, filetype="pdf")
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                pdf_text += page.get_text("text") + "\n"
        else:
            image = cls.get_png_from_pdf(file_content)
            image_file = io.BytesIO()
            image.save(image_file, format="PNG")
            vision = GoogleVisionAPI(google_api_key=cls.google_api_key)
            pdf_text, _ = vision.extract_text_vision(image_file)

        return pdf_text


class DocumentUtils:
    google_api_key = None

    def __init__(self, google_api_key=None) -> None:
        if google_api_key:
            DocumentUtils.google_api_key = google_api_key

    @classmethod
    def generate_image_hash_from_url(cls, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_bytes = response.content
            hasher = hashlib.md5()
            hasher.update(image_bytes)
            return hasher.hexdigest()
        except requests.RequestException as e:
            return None

    @classmethod
    def generate_hash_from_text(cls, text):
        try:
            hasher = hashlib.sha256()
            hasher.update(text.encode("utf-8"))
            return hasher.hexdigest()
        except Exception as e:
            return None

    @classmethod
    def generate_image_hash_from_file(cls, file_obj):
        try:
            file_obj.seek(0)
            file_bytes = file_obj.read()
            hasher = hashlib.md5()
            hasher.update(file_bytes)
            return hasher.hexdigest()
        except Exception as e:
            return None

    @classmethod
    def extract_text_from_xlsx(cls, file_content):
        xlsx_text = ""
        xls = pd.read_excel(io.BytesIO(file_content), sheet_name=None)
        for sheet_name, df in xls.items():
            xlsx_text += f"Sheet: {sheet_name}\n"
            xlsx_text += df.to_string(index=False) + "\n"
        return xlsx_text

    @classmethod
    def extract_text_from_csv(cls, file_content):
        csv_text = ""
        file_content = io.StringIO(file_content.decode("utf-8"))
        reader = csv.reader(file_content)
        for row in reader:
            csv_text += ",".join(row) + "\n"
        return csv_text

    @classmethod
    def convert_url_to_text(cls, url):
        response = requests.get(url)
        mime = magic.Magic(mime=True)
        file_content = response.content
        mime_type = mime.from_buffer(file_content)

        if mime_type == "application/pdf":
            message = f"Text from PDF: {PdfUtils.extract_text_from_pdf(file_content)}\n"
        elif mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            message = f"Text from XLSX: {cls.extract_text_from_xlsx(file_content)}\n"
        elif mime_type == "text/csv":
            message = f"Text from CSV: {cls.extract_text_from_csv(file_content)}\n"
        else:
            message, _ = cls.extract_text_from_image_url(url)

        return message

    @classmethod
    def convert_file_data(cls, files):
        all_text = ""
        mime = magic.Magic(mime=True)

        for file in files:
            file.seek(0)
            file_content = file.read()
            mime_type = mime.from_buffer(file_content)

            if mime_type.startswith("image/"):
                extracted_text, _ = cls.extract_text_from_image(file)
                if not is_short_message(extracted_text):
                    all_text += f"Text from Image: {extracted_text} \n"
                else:
                    all_text += extracted_text
            elif mime_type == "application/pdf":
                pdf_text = PdfUtils.extract_text_from_pdf(file_content)
                all_text += "Text from PDF: " + pdf_text + "\n"
            elif mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                xlsx_text = cls.extract_text_from_xlsx(file_content)
                all_text += "Text from XLSX: " + xlsx_text + "\n"
            elif mime_type == "text/csv":
                csv_text = cls.extract_text_from_csv(file_content)
                all_text += "Text from CSV: " + csv_text + "\n"

        return all_text

    @classmethod
    def extract_text_from_image(cls, file):
        vision = GoogleVisionAPI(google_api_key=cls.google_api_key)
        file.seek(0)
        buffer = io.BytesIO(file.read())
        file.seek(0)
        return vision.extract_text_vision(buffer)

    @classmethod
    def extract_text_from_image_url(cls, url):
        vision = GoogleVisionAPI(google_api_key=cls.google_api_key)
        return vision.extract_text_from_url(url)
