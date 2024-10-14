import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_google_genai import ChatGoogleGenerativeAI
from notebooks.transcribe_translate import TranscribeTranslate
import Youtube_transcript

# NOTE: The os.environ["GOOGLE_API_KEY"] will need to be populated for the following code to run
# Load the .env file
load_dotenv('C:\\Users\\vinid\\google_competition\\geminihackathon24\\.env')
# Accessing the environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

class Gemini_Summarization:
    def __init__(self, chunk_size=5000):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro")
        self.chunk_size = chunk_size

        self.template_split = """
Here's how you will summarize the transcript provide at the end:
1. Transcript Refinement:
    Error Elimination: Spelling, grammar, and punctuation errors will be meticulously corrected.
    Structural Enhancement: Sentence structure will be improved, awkward phrasing smoothed out, and the overall flow of the text enhanced.
    Clarity and Coherence: The text will be made clear, concise, and logical, ensuring the original meaning is preserved.
2. Concise Summary:
    Key Point Identification: The main points and crucial insights from the refined transcript will be identified and highlighted.
    Essence Extraction: The core message and essential information will be captured, providing a snapshot of the video's content.
    Informative and Coherent: Expect a clear, concise, and informative summary that accurately reflects the video's key points.

The final text should not reference the prompt and only contains the Concise Summary results. Do not add a header or use *.

Transcript {context}
"""
        self.template_final = """
Here's the instructions for summarizing the context provide at the end that will be used:
1. Split Refinement:
    Gather the context that are splits summarized from a video transcript. Understand its structiure and meaning before continuing.
2. Concise Summary:
    Key Point Identification: The main points and crucial insights from the combined transcript summaries will be identified and highlighted.
    Essence Extraction: The core message and essential information will be captured, providing a snapshot of the video's content.
    Informative and Coherent: Expect a clear, concise, and informative summary that accurately reflects the video's key points.
    Fluid Language: Attempt to have the summary in paragraph format and use of bullet points where needed.

The final text should not reference the prompt and only contains the Concise Summary results. Do not add a header or use *.

Transcript {context}
"""

    # Handles full summarization of the video transcript
    def complete_summarization(self, text, is_YU_url=True):
        # if is_YU_url:
        #     transcript = Youtube_transcript.get_clean_transcript(text)
        # else:
        #     transcript = text


        transcript = text
        results = self.summarize_splits(transcript)
        summaries = [summary['text'] for summary in results if summary]

        combined_summaries = ' \n\n'.join(summaries)
        final_summary = self.summarize_final(combined_summaries)

        return final_summary, combined_summaries

    # Summarizes each split and returns result.
    def summarize_splits(self, text):
        prompt_split = PromptTemplate(
            input_variables=["context"],
            template=self.template_split,
        )

        # Create an LLMChain for final summarization
        chain_split = LLMChain(llm=self.llm, prompt=prompt_split)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=150)
        all_splits = text_splitter.split_text(text)

        # TODO: Change to have it async or batch
        results = []

        for split in all_splits:
            result = chain_split.invoke(split)
            results.append(result)

        return results

    # Summarizes all splits and returns final result.
    def summarize_final(self, context):
        prompt_final = PromptTemplate(
            input_variables=["context"],
            template=self.template_final,
        )

        # Create an LLMChain for final summarization
        chain_final = LLMChain(llm=self.llm, prompt=prompt_final)

        return chain_final.invoke(context)['text']


    # VINNY SUMMARY CODE
    def generate_response(transcription, prompt, api = GEMINI_API_KEY, model = 'gemini-1.5-pro-latest'):
    # Return a gemini response
        genai.configure(api_key=api)
        model = genai.GenerativeModel(model)
        theprompt = prompt + transcription
        response = model.generate_content(theprompt)
        result = ''.join([p.text for p in response.candidates[0].content.parts])
        return result
