"""
Performs a transcription of a Youtube Video
Author: Pradeep Mohan
Date: 04/15/2024
"""
from typing import List, Optional, Type

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain.tools import BaseTool, StructuredTool, tool
from youtube_transcript_api import YouTubeTranscriptApi
import vertexai
from langchain_google_vertexai import ChatVertexAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from typing import List, Dict, Optional, Type
from langchain_google_vertexai import VertexAI
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain_google_vertexai import HarmBlockThreshold, HarmCategory
from langchain_core.utils.function_calling import convert_to_openai_function
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part
from video_chunking import VideoPreprocessor
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import re
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from tool_schemas import (
    YoutubeVideoTranscriberSchema,
    GeminiAudioTranscriberSchema,
    GoogleCloudSpeechAudioTranscriberSchema
)
from task_configs import (
GEMINI_1_5_VIDEO_PROMPT, 
GEMINI_1_5_PRO_AUDIO_PROMPT,
VIDEO_PART_MAX_DURATION,
GEMINI_GENERATION_CONFIG,
GEMINI_SAFETY_SETTINGS,
DEFAULT_GEMINI_BATCH_SIZE,
DEFAULT_BATCH_PROCESSING_DELAY, 
DEFAULT_VIDEOS_BUCKET)
import json
import traceback
from more_itertools import chunked, collapse
import time
from google.cloud import speech

class YoutubeVideoTranscriberTool(BaseTool):
    """Custom Youtube Video Transcriber Tool to be callable by an Agent"""
    name = "Youtube_Video_Transcriber"
    description = "useful for when you need to transcribe a Youtube video given as a valid Youtube URL"
    args_schema: Type[BaseModel] = YoutubeVideoTranscriberSchema
    def parse_video_id(self, video_url):
        try:
            # Split the URL by "v="
            split_url = video_url.split("v=")
            # Extract the substring after "v="
            video_id = split_url[1]
            return video_id
        except IndexError:
            print("Invalid URL format")
            return None

    def get_clean_transcript(self, video_url):
        """Takes a youtube video id (in the video link, can look like: YrVVXFMgXrw). 
            Pulls transcript and returns clean   version.
        """
        # checks to see if full link then returns just id
        if "v=" in video_id:
            video_id = self.parse_video_id(video_url)
        # Pull transcript
        script = YouTubeTranscriptApi.get_transcript(video_url)
        # Combine 'text' fields into one string
        input_string = ' '.join([line['text'] for line in script])
        # remove special charaters
        pattern = re.compile(r'[^a-zA-Z0-9\s.,;:!"\'()\-—–?‘’“”\[\]]')
        transcript =  pattern.sub('', input_string)

        return transcript
    def _run(
        self, url: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the Youtube Transcriber Tool."""
        try: 
            transcript = self.get_clean_transcript(url)
        except Exception as e:
            print(f"Error getting transcript from Youtube trying Cloud Speech API")
            ##TODO: Vinny to add the cloud speech api plugin
        return transcript

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")


class GeminiProAudioTranscriberTool(BaseTool):
    """Gemini 1.5 Pro based audio Transcriber Tool to be callable by an Agent"""
    name = "gemini_pro_audio_transcriber"
    description = "useful for when you need to transcribe an audio file using Gemini 1.5 Pro given as a valid Google Cloud Storage URI"
    args_schema: Type[BaseModel] = GeminiAudioTranscriberSchema
    def _run(
        self, uris: List[str], run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the Gemini Audio Transcriber Tool."""
        generative_multimodal_model = GenerativeModel(model_name='gemini-1.5-pro-latest', 
                                                          generation_config=GEMINI_GENERATION_CONFIG,
                                                          safety_settings=GEMINI_SAFETY_SETTINGS)
        transcript = ""
        audio_files = list(map(lambda x: Part.from_uri(x, mime_type="audio/mp3"),uris))
        contents = list(map(lambda x: [x,GEMINI_1_5_PRO_AUDIO_PROMPT],audio_files))
        contents = collapse(contents)
        response = generative_multimodal_model.generate_content(contents,stream=True)
        response_chunk_text = [str(chunk.text) for chunk in response]
        transcript = '\n'.join(response_chunk_text)
        return transcript

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

class GoogleCloudSpeechAudioTranscriberTool(BaseTool):
    """Google Cloud Speech  based audio Transcriber Tool to be callable by an Agent"""
    name = "google_cloud_speech_audio_transcriber"
    description = "useful for when you need to transcribe an audio file using Gemini 1.5 Pro given as a valid Google Cloud Storage URI"
    args_schema: Type[BaseModel] = GoogleCloudSpeechAudioTranscriberSchema
    
    def speech_to_text(self, config: speech.RecognitionConfig, audio: speech.RecognitionAudio) -> speech.RecognizeResponse:
        client = speech.SpeechClient()
        # Synchronous speech recognition request
        response = client.recognize(config=config, audio=audio)

        return response
    def _run(self, uris: List[str], run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """Use the Google Cloud Speech Audio Transcriber Tool."""
        transcript = ""
        transcript_list=[]
        for uri in uris:
            config = speech.RecognitionConfig(language_code="en")
            audio = speech.RecognitionAudio(uri=uri)
            response = self.speech_to_text(config, audio)
            transcript_list.append(response.results[0].alternatives[0].transcript)
        transcript = "\n".join(transcript_list)
        return transcript

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

    