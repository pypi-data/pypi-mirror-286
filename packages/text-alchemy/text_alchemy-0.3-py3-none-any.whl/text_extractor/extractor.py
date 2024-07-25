import json
from text_extractor.openai import OpenAIAPI
from text_extractor.pdf_utility import DocumentUtils, PdfUtils
from text_extractor.vision import GoogleVisionAPI

def extract_text_from_image_util(*args, **kwargs):
    file = kwargs.get("file", None)
    files = [file] if file else []
    url = kwargs.get("url")
    if files:
        converted_text = DocumentUtils.convert_file_data(files)
    elif url:
        converted_text = DocumentUtils.convert_url_to_text(url)

    prompt = kwargs.get("prompt", "")
    output_json = kwargs.get("output_json", {})
    helper_text = kwargs.get("helper_text", "")
    if output_json:
        prompt += f"\nExtract the structured data, in JSON format \n"
        prompt += json.dumps(output_json, indent=4)
    if helper_text:
        prompt += f"\n{helper_text} \n"

    openai_api_key = kwargs.get("openai_api_key")
    openai_api = OpenAIAPI(openai_key=openai_api_key)
    return openai_api.generate_extracted_info(
        prompt=prompt,
        content=converted_text,
        model_name=kwargs.get("model_name", "gpt-4o"),
    )

class Extractor:
    def __init__(self, openai_api_key, google_vision_api_key):
        self.openai_api = OpenAIAPI(openai_key=openai_api_key)
        self.google_vision_api = GoogleVisionAPI(google_vision_api_key)
        DocumentUtils(google_api_key=google_vision_api_key)
        PdfUtils(google_api_key=google_vision_api_key)

    def extract_meaningful_information_from_file(self, *args, **kwargs):
        return extract_text_from_image_util(*args, **kwargs)

    def extract_info_from_image(self, *args, **kwargs):
        return self.google_vision_api.extract_text_vision(*args, **kwargs)