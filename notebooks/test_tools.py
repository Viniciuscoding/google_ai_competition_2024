from tools import GeminiProVisionVideoInfoExtractionTool, GeminiProVideoJSONStringParserTool
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