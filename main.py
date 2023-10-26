import streamlit as st
from llama_index import ServiceContext, Document, GPTVectorStoreIndex
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader
import os
from PIL import Image


openai.api_key = st.secrets.openai_key
os.environ["OPENAI_API_KEY"] = openai.api_key
st.set_page_config(page_title="Chat with t∞ether ai 3", page_icon="icon.svg",
                   layout="centered", initial_sidebar_state="auto", menu_items=None)

st.title("Chat with t∞ether ai")


# def goto_sme_cv():
#    exec(open('sme_cv.py').read())


# st.button("SME: Add CV", on_click="")  # goto_sme_cv()

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me to help open a Job or find you SMEs match?"}
    ]


@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="t∞ether, Loading and indexing.. Hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data/CV", recursive=True)
        docs = reader.load_data()

        llm = OpenAI(model="gpt-3.5-turbo",
                     temperature=0.5, system_prompt="You are an HR expert and your job is to help the manager writing a open job position. If you missing any of these details; Job title, responsibilities, required skills, qualifications, payment, then ask them for that information. If they will ask to find an SME / person match compare them to our CVs and rank them accordingly.")
        service_context = ServiceContext.from_defaults(llm=llm)
        index = GPTVectorStoreIndex.from_documents(
            docs, service_context=service_context)
        return index


index = load_data()
# chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True,
#                                   system_prompt="You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features.")

if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    st.session_state.chat_engine = index.as_chat_engine(
        chat_mode="condense_question", verbose=True)

# Prompt for user input and save to chat history
if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking...👋"):
            # message = {"role": "user", "content": prompt}
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            # Add response to message history
            st.session_state.messages.append(message)
