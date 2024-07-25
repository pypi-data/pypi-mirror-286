import base64

import requests
from googleapiclient.discovery import build

class GoogleVisionAPI:
    def __init__(self, google_api_key=None):
        self.client = build("vision", "v1", developerKey=google_api_key)

    def extract_text_from_url(self, url):
        try:
            r = requests.get(url)
            content = base64.b64encode(r.content).decode("utf-8")
            return self.process_image(content)
        except Exception as e:
            return {
                "status": "FAILED",
                "error_description": e.args[0],
            }

    def extract_text_vision(self, image_buffer):
        try:
            image_buffer.seek(0)  # Ensure the buffer pointer is at the beginning
            image_bytes = image_buffer.read()
            content = base64.b64encode(image_bytes).decode("utf-8")
            return self.process_image(content)
        except Exception as e:
            return {
                "status": "FAILED",
                "error_description": e.args[0],
            }

    def process_image(self, content):
        image = {"content": content}
        request = {
            "image": image,
            "features": [{"type": "DOCUMENT_TEXT_DETECTION"}, {"type": "OBJECT_LOCALIZATION"}],
            "imageContext": {"languageHints": ["th", "en"]},
        }
        response = self.client.images().annotate(body={"requests": [request]}).execute()

        responses = (
            response["responses"][0]
            if "responses" in response and len(response["responses"]) > 0
            else {}
        )

        texts = responses["textAnnotations"] if "textAnnotations" in responses else []
        objects = (
            responses["localizedObjectAnnotations"]
            if "localizedObjectAnnotations" in responses
            else []
        )

        # Extract names for objects
        object_names = [obj["name"] for obj in objects]

        description = (
            f"The image contains the following text: '{texts[0]['description']}'."
            if texts
            else "The image does not contain any recognizable text."
        )
        if object_names:
            description += f" The image includes objects such as: {', '.join(object_names)}."
        else:
            description += " The image does not contain any recognizable objects."
        return description, object_names
