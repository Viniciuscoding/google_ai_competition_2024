from langchain_google_vertexai import ChatVertexAI
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
from langchain_core.utils.function_calling import convert_to_openai_function
from vertexai.preview.generative_models import GenerativeModel
from langchain_core.messages import HumanMessage
from task_configs import (
GEMINI_GENERATION_CONFIG,
GEMINI_1_5_VIDEO_TRANSCRIPT_PROMPT)


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

dict_schema = convert_to_openai_function(VideoTopicExtraction)

def detect_topics_sentiment(transcript_text):
    """
    Detects topics in the given text using ChatVertexAI.

    Args:
        text (str): The input text for topic detection.
    Returns:
        list: A list of detected topics.
    """

    generative_multimodal_model = GenerativeModel(model_name="gemini-1.5-pro",
                                                  generation_config=GEMINI_GENERATION_CONFIG)
    contents = [transcript_text, GEMINI_1_5_VIDEO_TRANSCRIPT_PROMPT]
    response = generative_multimodal_model.generate_content(contents)
    response_text = str(response.text)
    #print(response_text)
    text_json = {"type":"text",
                 "text":response_text,
               }
    text_message = {"type": "text",
                    "text": "What are the contents of the JSON ?",
                    }

    message_contents =  [text_message,text_json]
    message = HumanMessage(content=message_contents)
    llm = ChatVertexAI(model_name="gemini-1.0-pro-001",max_retries=0, temperature=0)
    structured_llm = llm.with_structured_output(dict_schema)
    extraction_response_dict = structured_llm.invoke([message])[0]
    print(extraction_response_dict)
    extraction_response = extraction_response_dict['args']
    return extraction_response

if __name__ == '__main__':
    transcript_text = """
        - Hello, friends.
        0:01
        I'm leaving now to go deep into the Amazon jungle
        0:03
        with my friend, the incredible Paul Rosolie,
        0:07
        deep to parts of the rainforest
        0:09
        that very few humans have ever seen.
        0:12
        I will try my best not to get eaten by anything.
        0:17
        The purpose of this trip is to celebrate nature
        0:19
        at its purest and most intense,
        0:22
        and to celebrate the work of people like Paul,
        0:24
        who have dedicated their life to protecting the jungle,
        0:27
        and the endless diversity of life that call it home.
        0:31
        If you want to support Paul in his work,
        0:33
        please donate or reach out to Jungle Keepers.
        0:36
        See the link in the description.
        0:39
        I hope to get back in one piece
        0:42
        and have some stories to tell,
        0:43
        and I will also try to record a podcast with Paul
        0:46
        when we're deep in the jungle.
        0:48
        I'll be offline until I emerge out.
        0:51
        Meanwhile, no internet, no phone,
        0:54
        no connection to the outside world,
        0:57
        just the raw, beautiful immensity of nature.
        1:02
        I am truly grateful to be alive, to have gotten the chance
        1:07
        to live on this beautiful planet of ours
        1:09
        with all of you, my fellow humans.
        1:13
        I love you all.
    """
    topics_sentiment = detect_topics_sentiment(transcript_text)
    print(topics_sentiment)