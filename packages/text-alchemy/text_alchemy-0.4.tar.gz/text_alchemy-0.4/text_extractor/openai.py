import base64
import io
import json
import re

import openai

def get_structure_openai_response(ai_response):
    if "``json" in ai_response:
        try:
            ai_response = ai_response.replace("False", "false").replace("True", "true")
            ai_response = re.search(r"```json\n([\s\S]+)\n```", ai_response)
            ai_response = ai_response.group(1)
            ai_response_json = json.loads(ai_response)
        except Exception as e:
            ai_response_json = json.loads(ai_response)
    else:
        try:
            ai_response_json = json.loads(ai_response)
        except Exception as e:
            ai_response_json = ai_response
    return ai_response_json


def file_storage_to_base64(file_storage):

    file_storage.seek(0)  # Ensure the file pointer is at the beginning
    image_buffer = io.BytesIO(file_storage.read())
    file_storage.seek(0)  # Reset the file pointer to the beginning again if needed

    image_buffer.seek(0)  # Ensure the buffer pointer is at the beginning
    image_bytes = image_buffer.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    return image_base64


class CompletionClient:
    def __init__(self, openai_key=None):
        self.openai_key = openai_key
        self.client = self._initialize_client()

    @classmethod
    def get_instance(cls, openai_key=None):
        return CompletionClient(openai_key)

    def _initialize_client(self):
        return openai.OpenAI(api_key=self.openai_key)

    def extract_ai_response(self, response):

        ai_response_dict = response.choices[0].message
        ai_response = (
            ai_response_dict["content"]
            if isinstance(ai_response_dict, dict)
            else ai_response_dict.content
        )

        return get_structure_openai_response(ai_response)

    def generate_extracted_info(self, messages, model_name="gpt-4o"):
        try:
            gpt_data = {
                "model": model_name,
                "messages": messages,
                "response_format": {"type": "json_object"},
            }

            response = self.client.chat.completions.create(**gpt_data)
            ai_response_json = self.extract_ai_response(response)

            return {"status": "SUCCESS", "response": ai_response_json}
        except Exception as e:
            print(e)
            return {
                "status": "FAILED",
                "response": {},
                "error_description": str(e),
            }

    def generate_info(
        self,
        prompt,
        content,
        model_name="gpt-4o",
        return_prompt=False,
    ):
        content = content.replace("  ", " ").replace("NaN", " ").replace("NaT", " ")
        while "  " in content:
            content = content.replace("  ", " ")

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": content},
        ]

        result = self.generate_extracted_info(messages, model_name)
        if return_prompt:
            result["prompt"] = prompt
        return result

    def generate_info_from_image(
        self,
        prompt,
        url=None,
        files=None,
        return_prompt=False,
    ):
        content = []
        if files:
            for file in files:
                image_base64 = file_storage_to_base64(file)
                if image_base64:
                    url = f"data:image/jpeg;base64,{image_base64}"
                    content.append({"type": "image_url", "image_url": {"url": url}})
        elif url:
            content.append({"type": "image_url", "image_url": {"url": url}})

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": content},
        ]

        result = self.generate_extracted_info(messages, "gpt-4o")
        if return_prompt:
            result["prompt"] = prompt
        return result


class AssistantClient:
    __instance = None

    def __init__(self, client):
        if AssistantClient.__instance is not None:
            raise Exception("CompletionClient instance already exists")
        self.client = client
        AssistantClient.__instance = self

    @classmethod
    def get_instance(cls, client):
        if AssistantClient.__instance is None:
            AssistantClient(client)
        return cls.__instance

    def list_assistants(self):
        return self.client.beta.assistants.list(order="desc", limit="20")

    def create_assistant(self, name, instruction, model="gpt-4o"):
        return self.client.beta.assistants.create(
            name=name,
            instructions=instruction,
            model=model,
        )

    def modify_assistant(self, assistant_id, name, instruction, model="gpt-4o"):
        return self.client.beta.assistants.update(
            assistant_id,
            name=name,
            instructions=instruction,
            model=model,
        )

    def add_file_to_assistant(self, assistant_id, file_path):
        file = self.client.files.create(file=open(file_path, "rb"), purpose="assistants")
        return self.client.beta.assistants.files.create(assistant_id=assistant_id, file_id=file.id)


class ThreadClient:
    __instance = None

    def __init__(self, client):
        if ThreadClient.__instance is not None:
            raise Exception("ThreadClient instance already exists")

        self.client = client
        ThreadClient.__instance = self

    @classmethod
    def get_instance(cls, client):
        if ThreadClient.__instance is None:
            ThreadClient(client)
        return cls.__instance

    def create_thread(self, metadata={}):
        return self.client.beta.threads.create(metadata=metadata)

    def retrieve_thread(self, thread_id):
        return self.client.beta.threads.retrieve(thread_id)

    def add_message_to_thread(self, thread_id, content, metadata={}):
        return self.client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=str(content), metadata=metadata
        )

    def list_messages(self, thread_id, limit=100):
        return self.client.beta.threads.messages.list(thread_id, limit=limit)

    def run_assistant_on_thread(self, thread_id, assistant_id):
        return self.client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)

    def get_run_status(self, thread_id, run_id):
        return self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)


class OpenAIAPI:
    openai_key = None

    def __init__(self, openai_key=None):
        if openai_key:
            OpenAIAPI.openai_key = openai_key
        self.completion_client = CompletionClient.get_instance(OpenAIAPI.openai_key)
        self.assistant_client = AssistantClient.get_instance(self.completion_client.client)
        self.thread_client = ThreadClient.get_instance(self.completion_client.client)

    def generate_extracted_info(self, *args, **kwargs):
        return self.completion_client.generate_info(*args, **kwargs)

    def generate_extracted_info_from_image(self, *args, **kwargs):
        return self.completion_client.generate_info_from_image(*args, **kwargs)

    def list_assistants(self, *args, **kwargs):
        return self.assistant_client.list_assistants(*args, **kwargs)

    def create_assistant(self, *args, **kwargs):
        return self.assistant_client.create_assistant(*args, **kwargs)

    def modify_assistant(self, *args, **kwargs):
        return self.assistant_client.modify_assistant(*args, **kwargs)

    def add_file_to_assistant(self, *args, **kwargs):
        return self.assistant_client.add_file_to_assistant(*args, **kwargs)

    def create_thread(self, *args, **kwargs):
        return self.thread_client.create_thread(*args, **kwargs)

    def retrieve_thread(self, *args, **kwargs):
        return self.thread_client.retrieve_thread(*args, **kwargs)

    def add_message_to_thread(self, *args, **kwargs):
        return self.thread_client.add_message_to_thread(*args, **kwargs)

    def list_messages(self, *args, **kwargs):
        return self.thread_client.list_messages(*args, **kwargs)

    def run_assistant_on_thread(self, *args, **kwargs):
        return self.thread_client.run_assistant_on_thread(*args, **kwargs)

    def get_run_status(self, *args, **kwargs):
        return self.thread_client.get_run_status(*args, **kwargs)
