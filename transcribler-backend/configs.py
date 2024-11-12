import os
from dotenv import load_dotenv
from google.cloud import aiplatform
import google.generativeai as genai
import vertexai

# Load the .env file
load_dotenv('C:\\Users\\vinid\\google_competition\\geminihackathon24\\.env')
# Accessing the environment variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# genai.configure(api_key=GOOGLE_API_KEY)
# GEMINI_GENAI_OBJECT = genai
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
Do not repeat profane, toxic, or improper words found in the transcription within your answer.
Video transcription: {transcription}
"""
VIN_TOPIC = """Provide me with all the topics in the video transcription.
Your response should be structured in a markdown format where the overall topic is at the top followed by each supporting topic.
The overall topic should be bolded, and sub-topics formatted as a dash list where the sub-topic is bolded and italized, while, the description is non-bolded. The sub-topics should be in chronological order. 
Do not repeat profane, toxic, or improper words found in the transcription."""

VIN_SENTIMENT_ANALYSIS = """You are a sentiment anylisis expert of video transcriptions? Your job is to figure out the sentiment for the following information:
1. Sentiment Analysis: Rank the video transction between three types of sentitments: negative, neutral, and positive.
2. Age Rating: provide the usa video age ratings: G, PR, PG-13, R, NC-17, X-XXX 
3. Toxicity: Display some toxicity examples if any. 
4. Fake news: Show if there is some sort of fake news in the video when it is not a fiction video.
If information is not found in each information, add Not Found as a response.
Video transcription: {transcription}
"""

# Source: https://www.filmratings.com/downloads/rating_rules.pdf
age_rating = """You are a video editor expert of video transcriptions. Your job is to provide the United States video age ratings G, PR, PG-13, R, and NC-17 to any video even though it is not a film. The respective description of each video age rating is bellow. Use them as guideline to your answer.
G - General Audiences. All Ages Admitted.
A G-rated motion picture contains nothing in theme, language, nudity,
sex, violence or other matters that, in the view of the Rating Board, would
offend parents whose younger children view the motion picture. The G
rating is not a "certificate of approval," nor does it signify a "children's"
motion picture. Some snippets of language may go beyond polite
conversation but they are common everyday expressions. No stronger
words are present in G-rated motion pictures. Depictions of violence are
minimal. No nudity, sex scenes or drug use are present in the motion
picture.

PG - Parental Guidance Suggested. Some Material May Not Be
Suitable For Children.
A PG-rated motion picture should be investigated by parents before they
let their younger children attend. The PG rating indicates, in the view of
the Rating Board, that parents may consider some material unsuitable for
their children, and parents should make that decision.
The more mature themes in some PG-rated motion pictures may call for
parental guidance. There may be some profanity and some depictions of
violence or brief nudity. But these elements are not deemed so intense
as to require that parents be strongly cautioned beyond the suggestion of
parental guidance. There is no drug use content in a PG-rated motion
picture.

PG-13 - Parents Strongly Cautioned. Some Material May Be
Inappropriate For Children Under 13.
A PG-13 rating is a sterner warning by the Rating Board to parents to
determine whether their children under age 13 should view the motion
picture, as some material might not be suited for them. A PG-13 motion
picture may go beyond the PG rating in theme, violence, nudity,
sensuality, language, adult activities or other elements, but does not
reach the restricted R category. The theme of the motion picture by itself
will not result in a rating greater than PG-13, although depictions of
activities related to a mature theme may result in a restricted rating for the
motion picture. Any drug use will initially require at least a PG-13 rating.
More than brief nudity will require at least a PG-13 rating, but such nudity in a PG-13 rated motion picture generally will not be sexually oriented.
There may be depictions of violence in a PG-13 movie, but generally not
both realistic and extreme or persistent violence. A motion picture's
single use of one of the harsher sexually-derived words, though only as
an expletive, initially requires at least a PG-13 rating. More than one
such expletive requires an R rating, as must even one of those words
used in a sexual context. The Rating Board nevertheless may rate such
a motion picture PG-13 if, based on a special vote by a two-thirds
majority, the Raters feel that most American parents would believe that a
PG-13 rating is appropriate because of the context or manner in which
the words are used or because the use of those words in the motion
picture is inconspicuous.

R - Restricted. Children Under 17 Require Accompanying Parent
or Adult Guardian.
An R-rated motion picture, in the view of the Rating Board, contains some
adult material. An R-rated motion picture may include adult themes, adult
activity, hard language, intense or persistent violence, sexually-oriented
nudity, drug abuse or other elements, so that parents are counseled to
take this rating very seriously. Children under 17 are not allowed to
attend R-rated motion pictures unaccompanied by a parent or adult
guardian. Parents are strongly urged to find out more about R-rated
motion pictures in determining their suitability for their children.
Generally, it is not appropriate for parents to bring their young children
with them to R-rated motion pictures.

NC-17 - No One 17 and Under Admitted.
An NC-17 rated motion picture is one that, in the view of the Rating
Board, most parents would consider patently too adult for their children 17
and under. No children will be admitted. NC-17 does not mean
"obscene" or "pornographic" in the common or legal meaning of those
words, and should not be construed as a negative judgment in any sense.
The rating simply signals that the content is appropriate only for an adult
audience. An NC-17 rating can be based on violence, sex, aberrational
behavior, drug abuse or any other element that most parents would
consider too strong and therefore off-limits for viewing by their children.

If you are not sure of the age appropriatness, please return "No enough certainty to the age appropriateness of this video" as the response. The transcript to be rated is presented bellow: {transcription}


# Source: https://smith.langchain.com/hub/mcdiddy/transcript2summary
transcript2summary = """# EXECUTIVE SUMMARY FROM TRANSCRIPT


## Instructions
'''
Review each chunk of the transcript from {location} chunk by chunk following the {chunkingSuggestion},
summarizing each chunk. Then summarize each summary into a long-form, stylized executive summary titled
as "Transcript Executive Summary about" + [Inferred Subject] with the following output:
'''
## Location
'''
{transcript}
'''
'''

Chunking Suggestion
json
{
 "chunkSize": {
 "unit": "words",
 "value": 500
 },
 "overlapSize": {
 "unit": "words",
 "value": 50
 },
 "rationale": {
 "chunkSize": "A chunk size of 500 words is chosen to balance detail retention and computational efficiency
 while ensuring the content is manageable for the model without exceeding token limits.",
 "overlapSize": "An overlap of 50 words helps maintain context continuity between chunks, ensuring smoother and more coherent summaries."
 }
}

## Output
[long-form, stylized executive summary]
'''


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
# aiplatform.init(project="google-ai-competition")
# vertexai.init(project="google-ai-competition")
# vertexai.preview.init()
# DEFAULT_VIDEOS_BUCKET="youtube_videos_1"
# DEFAULT_GEMINI_BATCH_SIZE=10
# #increases 2x after each rate limit error encountered during inference calls
# DEFAULT_BATCH_PROCESSING_DELAY=30#seconds
# GEMINI_1_5_PRO_SUPPORTED_AUDIO_MIME_TYPES=["audio/wav", "audio/mp3", "audio/aiff", "audio/aac", "audio/ogg", "audio/flac"]
# GEMINI_1_5_PRO_SUPPORTED_AUDIO_FORMATS = ["wav", "mp3", "aiff", "aac", "ogg", "flac"]


