#Library of Gemini Tools used by different features
#Makes use of Vertex AI, Gemini 1.5 Pro / Gemini 1.0 Pro or Gemini Pro Vision whereever feasible
"""
All tools used by LLM to process videos, extract information, used by various downstream tasks
Author: Pradeep Mohan
Date: 05/01/2024
"""
from google.cloud import aiplatform
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
from tool_schemas import (
    GeminiProVisionVideoInfoExtractionSchema, 
    GeminiProVideoJsonStringParserSchema,
    VideoTopicExtraction
)
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from time import sleep
from task_configs import (
GEMINI_1_5_VIDEO_PROMPT, 
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


#video_url = "https://www.youtube.com/watch?v=f_lRdkH_QoY"

class GeminiProVisionVideoInfoExtractionTool(BaseTool):
    name = "geminipro_vision_video_info_extractor"
    description = "useful for when you have to extract information pertaining to a given video "
    args_schema: Type[BaseModel] =  GeminiProVisionVideoInfoExtractionSchema    
    def _run(
        self, url: str, uri: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Dict:
        """Use the tool."""
        response_jsons = []
        generative_multimodal_model = GenerativeModel(model_name='gemini-1.5-pro-latest', 
                                                          generation_config=GEMINI_GENERATION_CONFIG,
                                                          safety_settings=GEMINI_SAFETY_SETTINGS)
        if url is None and uri is not None:
            #Process uri, at this point it will be a valid uri of a Google Cloud Storage bucket, 
            #caveats: this must be a small video and not longer than 10 mins in length
            #caveats not handled
            video_file = Part.from_uri(uri, mime_type="video/mp4")
            contents = [video_file, GEMINI_1_5_VIDEO_PROMPT]
            response = generative_multimodal_model.generate_content(contents)
            response_text = str(response.text)
            response_jsons = list(response_text)
            audio_urilist = None
            frame_urilist = None
        elif uri is None and url is not None:
            #Process url using Video Processor and get the default segments of the video
            video_chunker = VideoPreprocessor(output_directory="videos/")
            video_chunker.download_youtube_video(url)
            video_chunker.basic_segmentation()
            #Extract the key frames of the video
            video_chunker.extract_frames()
            #extract audio chunks
            video_chunker.extract_audio()
            #save the metadata
            video_chunker.save_metadata()            
            #Upload the Videos, the frames, the audio files and the transcripts to Cloud Storage
            cloud_storage_metadata_dict = video_chunker.upload_to_cloud_storage(bucket=DEFAULT_VIDEOS_BUCKET)
            #Get the uris of the video segments in cloud storage
            seg_urilist = cloud_storage_metadata_dict["segment_paths"]
            #Create batches of uris of video segments
            batches_urilist = chunked(seg_urilist,DEFAULT_GEMINI_BATCH_SIZE)
            #Get Video files for batches
            video_file_batches = list(map(lambda x:[Part.from_uri(uri, mime_type="video/mp4") for uri in x],batches_urilist))
            contents_batches = list(map(lambda x:[[video_file, GEMINI_1_5_VIDEO_PROMPT] for video_file in x],video_file_batches))
            #Get the response from Gemini 
            for i,contents_batch in enumerate(contents_batches):
                #sleep(DEFAULT_BATCH_PROCESSING_DELAY)
                print(f"Batch {i+1} processing")
                #flatten contents_batch into a single list
                contents = collapse(contents_batch)
                try:
                   response = generative_multimodal_model.generate_content(contents,stream=True) 
                except Exception as e:
                    print(f"Error processing batch {i+1}")
                    traceback.print_exc()                    
                response_chunk_text = [str(chunk.text) for chunk in response]
                response_jsons.extend(response_chunk_text)
                print(f"Batch {i+1} processed, sleeping for {DEFAULT_BATCH_PROCESSING_DELAY} seconds")
                time.sleep(DEFAULT_BATCH_PROCESSING_DELAY)                                
            audio_urilist = cloud_storage_metadata_dict["audio_paths"]
            frame_urilist = cloud_storage_metadata_dict["frame_paths"]
        tool_response_dict = {"jsons":response_jsons,
                              "audio_uris":audio_urilist,
                              "frame_uris":frame_urilist
                              }
        return tool_response_dict

    async def _arun(
        self, url: str, uri: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> Dict:
        """Use the tool asynchronously."""
        raise NotImplementedError("geminipro_vision_video_info_extractor does not support async")


#video_uri = "gs://youtube_videos_1/Charlie Chaplin - The Kid - Fight Scene.mp4"
class GeminiProVideoJSONStringParserTool(BaseTool):
    name = "geminipro_video_json_parser_tool"
    description = "useful for when you have to parse a list of strings each representing a JSON schema to extract relevant information about a video and output as a structured and cleaner Python dictionary schema"
    args_schema: Type[BaseModel] = GeminiProVideoJsonStringParserSchema
    
    def _run(self, jsons: List[str],run_manager: Optional[CallbackManagerForToolRun] = None) -> Dict:
        """Use the tool."""
        dict_schema = convert_to_openai_function(VideoTopicExtraction)
        text_message = {"type": "text",
                        "text": "What are the contents of the JSON ?",
                       }
        message_contents = list(map(lambda x:[text_message,{"type":"text","text":x}] ,jsons))
        message = HumanMessage(content=message_contents)
        llm = ChatVertexAI(model_name="gemini-1.0-pro-001",max_retries=0, temperature=0)
        structured_llm = llm.with_structured_output(dict_schema)
        try:
            extraction_responses = structured_llm.batch([[message]])
        except Exception as e:
            traceback.print_exc()
        #TODO: extraction_responses must be merged into a single output dictionary of responses
        merged_extraction_dict = {}
        merged_extraction_dict["description"]=""
        
        return extraction_responses
    
    def _arun(self, jsons: List[str], run_manager:Optional[AsyncCallbackManagerForToolRun] = None) -> Dict:
        """"Use the tool Asynchronously """
        raise NotImplementedError("geminipro_video_json_parser_tool does not support async")


