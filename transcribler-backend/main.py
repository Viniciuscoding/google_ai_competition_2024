import os
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from langdetect import detect
import google.generativeai as genai
from dotenv import load_dotenv
from Gemini_Video_Summary import Gemini_Summarization
from configured_chat import ConfiguredChat
from topic_detection_function_vin import detect_topics_sentiment
from Vin_Gemini_Video_Summary import Transcription
from configs import VIN_SUMMARY_PROMPT, VIN_TOPIC, VIN_SENTIMENT_ANALYSIS

import datetime

# Load the .env file
load_dotenv('C:\\Users\\ron\\Documents\\GitHub\\google_ai_competition_2024\\backend_test\\.env')
# Accessing the environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

from IPython.display import Markdown

url = "https://www.youtube.com/watch?v=5LGEiIL1__s"

video_id = url.split("=")[1]
summarizer = Gemini_Summarization
video_id

def get_transcript(video_id):
    """
    Fetches and concatenates the transcript of a YouTube video.

    Parameters:
    video_id (str): The ID of the YouTube video.

    Returns:
    str: A string containing the concatenated transcript of the video.

    Raises:
    Exception: If there is an error in fetching the transcript.
    """
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        raise e

    transcript = " ".join([d["text"] for d in transcript_list])
    return transcript

def main():
  transcript = get_transcript(video_id)

  final_summary = summarizer.generate_response(transcript, VIN_SUMMARY_PROMPT, GEMINI_API_KEY)

  # print(final_summary)

  topics = summarizer.generate_response(transcript, VIN_TOPIC, GEMINI_API_KEY)

  # print(Markdown(topics))

  sentiment = summarizer.generate_response(transcript, VIN_SENTIMENT_ANALYSIS, GEMINI_API_KEY)
  # print(Markdown(sentiment))
  return [final_summary, topics, sentiment]

if __name__ == "__main__":
    # Code here will only run when the script is executed directly, not when imported
    main()