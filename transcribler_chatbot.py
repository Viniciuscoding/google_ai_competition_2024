# Source: https://github.com/marshmellow77/vertex-gemini/blob/main/chatbot-gemini.py
# NOTE Streamlit must be on 1.35.0 version to work. On version 1.37.0 this error might happen RuntimeError: There is no current event loop in thread 'ScriptRunner.scriptThread'. 

import os
import time
import asyncio
# import vertexai
import streamlit as st
# from dotenv import load_dotenv
from typing import Any, List, Mapping, Optional
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from vertexai.preview.generative_models import GenerativeModel

transcript = "[Music] from illumination the creators of minions duration trailer \
Starts Now [Applause] [Music] isn't it beautiful this is awesome oh maybe we should \
go say hi hey there Jack talked to a girl a girl he wants to marry her what I say \
that you said it with your eyes [Music] they must be migrating migration what \
a stupid idea okay you're impossible because I found a safe place for us to live \
I wanted to see the world [Music] In Harm's Way for no reason except the chance \
at a Caribbean vacation I don't want to miss out on life because you're afraid \
to leave this pond let's floss hey why are we the only Birds heading this way what \
is this place I promise adventure and this is exactly what I promised can we land \
you're old enough to do it in the sky now we have a number two situation oh but \
it's gross every bird does it in the sky oh I told you\ we are not Landing there \
is no way we're Landing are you sure no one's watching when Mallard do it now or we \
leave without you okay okay we are completely lost we're trying to get to Jamaica \
and I love birds it's this way well we are not flying through this crazy death \
trap of a city just stay close to me and everything will be all right I'm okay \
yeah no I'm okay we can do this thank you maybe you don't stick too close"


# Setting page title and header
st.set_page_config(page_title="Gemini Pro Chatbot", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>Gemini Pro Chatbot</h1>", unsafe_allow_html=True)

# Load chat model
@st.cache_resource
def load_chain():
    gemini_pro_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", 
                                              temperature=0.3, 
                                              max_output_tokens=256,
                                              google_api_key="AIzaSyD2Z94fHVeEsa2wpUN0P4AIEGsm7VbX8H8"
    )
    memory = ConversationBufferMemory()
    chain = ConversationChain(llm=gemini_pro_model, memory=memory, verbose=True)

    chain.run(transcript)
    
    return chain

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

loop = get_or_create_eventloop()
asyncio.set_event_loop(loop)

chatchain = load_chain()

# Initialise session state variables

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": transcript}]
# if 'messages' not in st.session_state:
#     st.session_state['messages'] = []

st.sidebar.title("Sidebar")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# Reset conversation
if clear_button:
    st.session_state['messages'] = []

# Display previous messages
for message in st.session_state['messages']:
    role = message["role"]
    content = message["content"]
    with st.chat_message(role):
        st.markdown(content)

# Chat input
if prompt := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    response = chatchain.run(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)