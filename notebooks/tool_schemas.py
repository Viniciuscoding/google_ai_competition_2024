"""
All tool schemas used by LLM's Tools to process videos, extract information, used by various downstream tasks
Author: Pradeep Mohan
Date: 05/01/2024
"""
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from typing import List, Dict, Type, Optional
from vertexai.preview.generative_models import GenerativeModel, Part
from google.cloud import storage
import traceback
import requests
from task_configs import (
    GEMINI_1_5_PRO_SUPPORTED_AUDIO_MIME_TYPES,
    GEMINI_1_5_PRO_SUPPORTED_AUDIO_FORMATS
)

class GeminiProVisionVideoInfoExtractionSchema(BaseModel):
    """Inputs to the GeminiProVisionVideoInfoExtractor"""
    url: Optional[str] = Field(description="Youtube Video URL or Video ID")
    uri: Optional[str] = Field(description="Video URI inside a Google Cloud Storage Bucket")
    
    @validator("url","uri")
    @classmethod
    def valid_url_or_uri(cls,field_values):
        """Checks if the URI path to an object is a valid one"""
        def check_uri_object_exists(uri: str):
            storage_client = storage.Client()
            bucket = storage_client.bucket(uri.split('/')[2])
            objectname = None if len(uri.split('/')) < 4 else "/".join(uri.split("/")[3:])
            if objectname is None:
                raise ValueError("This appears to be a path to the parent folder of an object")
            if not bucket.blob(objectname).exists():
                raise ValueError(f"Appears that the specified object in the uri: {uri} doen't exist")
            return True
        
        if field_values["url"] is None and field_values["uri"] is None:
            raise ValueError("Both Video URL and URI cannot be empty")
        if field_values["uri"] is not None and not field_values["uri"].startswith("gs://") and field_values["url"] is None:
            raise ValueError("The Google Cloud Storage uri of the video must begin with gs://")
        else:
            try:
                check_uri_object_exists(field_values["uri"])
            except ValueError as v:
                traceback.print_exc()
                raise ValueError("uri field failed validation check, perhaps object in uri doesn't exist")
        if field_values["uri"] is not None and field_values["url"] is not None:
            raise ValueError(f"Ambiguous Specification, both, URL: {field_values["url"]} and URI: {field_values["uri"]} currently unsupported")
        if field_values["url"] is not None and field_values["uri"] is None:
            r = requests.get(field_values["url"]) 
            if "video unavailable" in r.text.lower():
                raise ValueError(f"Invalid Youtube Video URL, {field_values["url"]} specified")
            
            
class GeminiProVideoJsonStringParserSchema(BaseModel):
    """Inputs to the GeminiProVideoJSONStringParser"""
    jsons: List[str] = Field(description="A list of valid jsons as strings")
    
    @validator("json")
    @classmethod
    def valid_list_of_jsons_as_strings(cls,field_values):
        json_list = field_values["jsons"]
        valid_string = list(map(lambda x:isinstance(x,str),json_list))        
        if valid_string.count(False)>0:
            raise ValueError(f"Invalid JSON string found")
        valid_non_empty_string = list(map(lambda x:x not in [""," ","``` ```","``````"],json_list))
        if valid_non_empty_string.count(False)>0:
            raise ValueError(f"Empty JSON String Found")

                            
class YoutubeVideoTranscriberSchema(BaseModel):
    """Inputs to the YoutubeVideoTranscriber"""
    url: str = Field(
        description="Youtube Video URL or Video ID"
    )
    @validator("url")
    @classmethod
    def validate_youtube_video_url(cls,field_values):
        if field_values["url"] is not None:
            r = requests.get(field_values["url"]) 
            if "video unavailable" in r.text.lower():
                raise ValueError(f"Invalid Youtube Video URL, {field_values["url"]} specified")
        else:
            raise ValueError(f"Invalid URL string")

class GeminiAudioTranscriberSchema(BaseModel):
    """Inputs to the GeminiAudioTranscriber"""
    audio_uris: List[str] = Field( description="List of Audio URI inside a Google Cloud Storage Bucket")
    mime_types: List[str] = Field(description="Mime Type of the Audio")
    @validator("audio_uris","mime_types")
    @classmethod
    def validate_audio_uris(cls,field_values):
        """Checks if the URI path to an object is a valid one"""
        def check_audio_uri_exists(uri: str):
            storage_client = storage.Client()
            bucket = storage_client.bucket(uri.split('/')[2])
            objectname = None if len(uri.split('/')) < 4 else "/".join(uri.split("/")[3:])
            if objectname is None:
                raise ValueError("This appears to be a path to the parent folder of an object")
            if not bucket.blob(objectname).exists():
                raise ValueError(f"Appears that the specified object in the uri: {uri} doen't exist")
            return True
        if field_values["audio_uris"] is None or field_values["mime_types"] is None:
            raise ValueError("Either of Audio URI or Mime Type cannot be None")
        if len(field_values["audio_uris"])==0 or len(field_values["mime_types"])==0:
            raise ValueError("Either of Audio URI or Mime Type cannot be empty")
        if len(field_values["audio_uris"]) != len(field_values["mime_types"]):
            raise ValueError(f"Lengths of audio_uris and mime_types do not match")
        audio_uri_valid_cs_uri = list(map(lambda x:x.startswith("gs://"),field_values["audio_uris"]))
        if audio_uri_valid_cs_uri.count(False)>0:
            raise ValueError(f"Audio URIs must begin with gs://, {audio_uri_valid_cs_uri.count(False)} fail this test")
        try:
            audio_uri_check_list = list(map(lambda x:check_audio_uri_exists(x),field_values["audio_uris"]))
        except ValueError as e:
            raise ValueError(f"one of the audio uris is not a valid Google Cloud storage uri")
        if audio_uri_check_list.count(True) != len(field_values["audio_uris"]):
            raise ValueError(f"One of the audio uris is not a valid Google Cloud storage uri")
        mime_type_check_list = list(map(lambda x:True if x in GEMINI_1_5_PRO_SUPPORTED_AUDIO_MIME_TYPES else False,field_values["mime_types"]))
        if mime_type_check_list.count(False)>0:
            raise ValueError(f"Invalid Mime Type found in list of audio uris")
        audio_format_check_list = list(map(lambda x:True if x.split("/")[-1].split(".")[-1].lower() in GEMINI_1_5_PRO_SUPPORTED_AUDIO_FORMATS else False,field_values["audio_uris"]))
        if audio_format_check_list.count(False)>0:
            raise ValueError(f"Invalid Audio Format found in list of audio uris")


class GoogleCloudSpeechAudioTranscriberSchema(BaseModel):
    """Inputs to the GoogleCloudSpeechAudioTranscriber"""
    audio_uris: List[str] = Field( description="List of Audio URI inside a Google Cloud Storage Bucket")
    mime_types: List[str] = Field(description="Mime Type of the Audio")
    @validator("audio_uris","mime_types")
    @classmethod
    def validate_audio_uris(cls,field_values):
        """Checks if the URI path to an object is a valid one"""
        def check_audio_uri_exists(uri: str):
            storage_client = storage.Client()
            bucket = storage_client.bucket(uri.split('/')[2])
            objectname = None if len(uri.split('/')) < 4 else "/".join(uri.split("/")[3:])
            if objectname is None:
                raise ValueError("This appears to be a path to the parent folder of an object")
            if not bucket.blob(objectname).exists():
                raise ValueError(f"Appears that the specified object in the uri: {uri} doen't exist")
            return True
        if field_values["audio_uris"] is None or field_values["mime_types"] is None:
            raise ValueError("Either of Audio URI or Mime Type cannot be None")
        if len(field_values["audio_uris"])==0 or len(field_values["mime_types"])==0:
            raise ValueError("Either of Audio URI or Mime Type cannot be empty")
        if len(field_values["audio_uris"]) != len(field_values["mime_types"]):
            raise ValueError(f"Lengths of audio_uris and mime_types do not match")
        audio_uri_valid_cs_uri = list(map(lambda x:x.startswith("gs://"),field_values["audio_uris"]))
        if audio_uri_valid_cs_uri.count(False)>0:
            raise ValueError(f"Audio URIs must begin with gs://, {audio_uri_valid_cs_uri.count(False)} fail this test")
        try:
            audio_uri_check_list = list(map(lambda x:check_audio_uri_exists(x),field_values["audio_uris"]))
        except ValueError as e:
            raise ValueError(f"one of the audio uris is not a valid Google Cloud storage uri")
        if audio_uri_check_list.count(True) != len(field_values["audio_uris"]):
            raise ValueError(f"One of the audio uris is not a valid Google Cloud storage uri")
        mime_type_check_list = list(map(lambda x:True if x in GEMINI_1_5_PRO_SUPPORTED_AUDIO_MIME_TYPES else False,field_values["mime_types"]))
        if mime_type_check_list.count(False)>0:
            raise ValueError(f"Invalid Mime Type found in list of audio uris")
        audio_format_check_list = list(map(lambda x:True if x.split("/")[-1].split(".")[-1].lower() in GEMINI_1_5_PRO_SUPPORTED_AUDIO_FORMATS else False,field_values["audio_uris"]))
        if audio_format_check_list.count(False)>0:
            raise ValueError(f"Invalid Audio Format found in list of audio uris")


class VideoTopicExtraction(BaseModel):
    '''An Extraction of Key Features from an input video JSON'''
    description: str = Field(description="A 512 token description of the contents of the video")
    key_topics: List[str] = Field(description="A collection of key topics.")
    sentiments: List[str] = Field(description="A collection of key sentiments expressed in the video")
    emotions: List[str] = Field(description="A collection of key emotions expressed in the video")
    people: List[str] = Field(description="A list of all people mentioned or featuring in the video")
    locations: List[str] = Field(description="A list of all locations and landmarks referred or appearing  in the video")
    age_appropriateness: str = Field(description="Age groups of audience the video is appropriate for")
    movie_content_warnings: List[str] = Field(description="a collection of all content warnings applicable to the video")
    languages: List[str] = Field(description="A list of all languages spoken in the video")
    main_language: List[str] = Field(description="A the main language of the video")
                                                                   
        

            
            
    