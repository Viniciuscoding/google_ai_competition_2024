import os
import json
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from langdetect import detect
import google.generativeai as genai
from dotenv import load_dotenv
from Gemini_Video_Summary import Gemini_Summarization
from topic_detection_function_vin import detect_topics_sentiment
from Vin_Gemini_Video_Summary import Transcription
from configs import VIN_SUMMARY_PROMPT, VIN_TOPIC, VIN_SENTIMENT_ANALYSIS

# Load the .env file
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, ".env")
load_dotenv(env_path)
# Accessing the environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

from IPython.display import Markdown

# url = "https://www.youtube.com/watch?v=6COmYeLsz4c"

import requests
from bs4 import BeautifulSoup

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

def parse_sentiment(sentiment):
    data = {}
    lines = sentiment.strip().split("\n")

    for line in lines:
        if "**" in line:
            key = line.split("**")[1].strip(":") 
            value = line.split(":**")[1].strip() 
            data[key] = value
    return data

def main(url):
    print(url)
    # Extracting HTML Code of the Video Page:
    response = requests.get(url)
    html_content = response.text

    # Processing the HTML Code with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extracting <title> tag's content
    title_tag = soup.find('meta', property='og:title')
    video_title = title_tag['content'] if title_tag else 'Title not found'

    video_id = url.split("=")[1]
    summarizer = Gemini_Summarization
    video_id

    transcript = get_transcript(video_id)

    final_summary = summarizer.generate_response(transcript, VIN_SUMMARY_PROMPT, GEMINI_API_KEY)

    # print(final_summary)

    topics = summarizer.generate_response(transcript, VIN_TOPIC, GEMINI_API_KEY)

    # print(Markdown(topics))

    sentiment = summarizer.generate_response(transcript, VIN_SENTIMENT_ANALYSIS, GEMINI_API_KEY)
    
    data = parse_sentiment(sentiment)
    data["final summary"] = final_summary
    data["topics"] = topics
    data["title"] = video_title
    json_data = json.dumps(data, indent=4)
    print(sentiment)
    print(data)
    print(json_data)
    return json_data

if __name__ == "__main__":
    # Code here will only run when the script is executed directly, not when imported
    main()