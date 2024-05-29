import vertexai
from vertexai.generative_models import GenerativeModel
import vertexai.preview.generative_models as generative_models

class ConfiguredChat:
    def __init__(self, project_id, model_name):
        vertexai.init(project="vertexai-gemini-hackathon-2024", location="us-central1")
        self.project_id = project_id
        self.model_name = model_name
        self.safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}
        self.model_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}
        self.model = GenerativeModel(model_name, safety_settings=self.safety_settings, generation_config=self.model_config)
        # self.chat = self.model.start_chat()
# Example usage
# if __name__ == "__main__":
#     project_id = "vertexai-gemini-hackathon-2024"
#     model_name = "gemini-1.5-pro-preview-0409"

#     # Create an instance of ConfiguredChat
#     chat = ConfiguredChat(project_id, model_name)

#     # Start a chat
#     chat_instance = chat.model.start_chat()

#     # Send a message and get the response
#     response = chat_instance.send_message("Hello! How are you?")
#     print("Assistant:", response.text)

#     # Send another message and get the response
#     response = chat_instance.send_message("Can you tell me a joke?")
#     print("Assistant:", response.text)