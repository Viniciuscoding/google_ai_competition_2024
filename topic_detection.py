import os
import json
from typing import List
from google.cloud import aiplatform
# from langchain_core.pydantic_v1 import BaseModel, Field
# from langchain_core.utils.function_calling import convert_to_openai_function
import google.generativeai as genai
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from dotenv import load_dotenv

load_dotenv('./google_ai_competition_2024/.env')
# Accessing the environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


""" from task_configs import (
    GEMINI_1_5_VIDEO_TRANSCRIPT_PROMPT,
    GEMINI_GENAI_OBJECT,
    GEMINI_GENERATION_CONFIG,
    GEMINI_SAFETY_SETTINGS
)
from benchmark_examples import (
    GEMINI_1_5_PRO_BENCHMARK_EXTRACTION_LEX_TUCKER_TRANSCRIPT
) """
VIDEO_PART_MAX_DURATION=120 #Part duration in seconds

GEMINI_1_5_VIDEO_TRANSCRIPT_PROMPT=""" You are provided with a transcript of video. Your task is to analyze the video's transcript
 and extract the following information from the transcript:
1. description: <a proper summary of the video in 1000 tokens>
2. key_topics: <a collection of 10 key topics as a valid python list>
3. sentiments: <a collection of 10 key sentiments as a valid python list>
4. emotions: <a collection of 10 key emotions as a valid python list>
5. people: <a list of all people mentioned in the video as a valid python list>
6. locations: <a list of all locations mentioned in the video as a valid python list>
7. age_appropriateness: <What age is the video appropriate for?>
8. movie_content_warnings: <a collection of all content warnings applicable to the video?>
9. languages: <a collection of key languages spoken in the video>
10. main_language: <the main or dominant language spoken in the video>
The information must be extracted only from the video and you must not refer to outside sources.
Make sure you generate the final output in a valid JSON format enclosed within opening and closing curly braces. Do not add the word JSON to the beginning of your response.
"""
#Generation Config
GEMINI_GENERATION_CONFIG = {
  "temperature": 0
}
# Safety config
GEMINI_SAFETY_SETTINGS = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]
#aiplatform.init(project="helpful-compass-425319-r7")
# vertexai.init(project="helpful-compass-425319-r7")
# vertexai.preview.init()
# class VideoTopicExtraction(BaseModel):
#     '''An Extraction of Key Features from an input video JSON'''
#     description: str = Field(description="A 1000 token description of the contents of the video")
#     key_topics: List[str] = Field(description="A collection of key topics.")
#     sentiments: List[str] = Field(description="A collection of key sentiments expressed in the video")
#     emotions: List[str] = Field(description="A collection of key emotions expressed in the video")
#     people: List[str] = Field(description="A list of all people mentioned or featuring in the video")
#     locations: List[str] = Field(description="A list of all locations and landmarks referred or appearing  in the video")
#     age_appropriateness: str = Field(description="Age groups of audience the video is appropriate for")
#     movie_content_warnings: List[str] = Field(description="a collection of all content warnings applicable to the video")
#     languages: List[str] = Field(description="A list of all languages spoken in the video")
#     main_language: List[str] = Field(description="A the main language of the video")

# dict_schema = convert_to_openai_function(VideoTopicExtraction)
def detect_topics_sentiment(transcript_text):
    """
    Detects topics in the given text using ChatVertexAI.

    Args:
        text (str): The input text for topic detection.
    Returns:
        list: A list of detected topics.
    """

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    GEMINI_GENAI_OBJECT = genai

    generative_multimodal_model = GenerativeModel(model_name="gemini-1.0-pro-vision",
                                                         generation_config=GEMINI_GENERATION_CONFIG)
    # generative_multimodal_model = GEMINI_GENAI_OBJECT.GenerativeModel(model_name="gemini-1.5-pro-latest", generation_config=GEMINI_GENERATION_CONFIG,safety_settings=GEMINI_SAFETY_SETTINGS)
    contents = [transcript_text, GEMINI_1_5_VIDEO_TRANSCRIPT_PROMPT]
    response = generative_multimodal_model.generate_content(contents)
    response_text = str(response.text)

    # print(response_text)# Remove the Markdown code block formatting
    json_string = response_text.replace('```json', '').replace('```', '').strip()

    return json.loads(json_string)


if __name__ == '__main__':
    transcript_text = ""
    topics_sentiment = detect_topics_sentiment(transcript_text)
    