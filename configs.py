from google.cloud import aiplatform
import google.generativeai as genai
import vertexai
from dotenv import load_dotenv
load_dotenv('./google_ai_competition_2024/.env')
# genai.configure(api_key=GOOGLE_API_KEY)
GEMINI_GENAI_OBJECT = genai
VIDEO_PART_MAX_DURATION=120 #Part duration in seconds
GEMINI_1_5_VIDEO_PROMPT=""" You are provided with a video. Your task is to analyze the video and extract the following information from the video:
1. description: <a proper description of the video in 512 tokens>
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
GEMINI_1_5_PRO_AUDIO_PROMPT=""" You are provided with an audio file. Your task is to analyze the audio and extract the following information from the audio:
in the format of timecode, speaker, caption. Use speaker A, speaker B, etc. to identify the speakers. If you cannot attribute to any speakers,
then simply return the transcription of the entire audio. If you can, identify relevant topics associated with the audio such as people,
places, sentiments, emotions, locations, languages, and the main language. Identify them and included that as a part of your transcript towards the end of the transcript.
You must not refer to outside sources and work only with the audio file provided to you. If you need to refer to outside sources to
provide additional context after transcription and extraction, you can use Google Search and gather that additional context as follows towards the end of the transcript:
Additional Context:
Additional Context Source:
"""
GEMINI_1_5_VIDEO_TRANSCRIPT_PROMPT=""" You are provided with a transcript of video. Your task is to analyze the video's transcript
 and extract the following information from the transcript:
1. description: <a proper description of the video in 512 tokens>
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

VIN_SUMMARY_PROMPT = """Provide me with a summarization of the video transcription.
Your response should be structured in a markdown format where the overall topic is at the top followed by each supporting topic.
The overall topic should be bolded, and sub-topics formatted as a dash list where the sub-topic is bolded and italized, while, the description is non-bolded. The sub-topics should be in chronological order.
Do not repeat profane, toxic, or improper words found in the transcription within your answer. Video transcription: {transcription}
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
aiplatform.init(project="helpful-compass-425319-r7")
vertexai.init(project="helpful-compass-425319-r7")
vertexai.preview.init()
DEFAULT_VIDEOS_BUCKET="youtube_videos_1"
DEFAULT_GEMINI_BATCH_SIZE=10
#increases 2x after each rate limit error encountered during inference calls
DEFAULT_BATCH_PROCESSING_DELAY=30#seconds
GEMINI_1_5_PRO_SUPPORTED_AUDIO_MIME_TYPES=["audio/wav", "audio/mp3", "audio/aiff", "audio/aac", "audio/ogg", "audio/flac"]
GEMINI_1_5_PRO_SUPPORTED_AUDIO_FORMATS = ["wav", "mp3", "aiff", "aac", "ogg", "flac"]