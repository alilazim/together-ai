#!/usr/bin/env python
# -*- coding: utf-8 -*-




import openai
from llama_index import (Document, GPTVectorStoreIndex, ServiceContext,
                         SimpleDirectoryReader)
from llama_index.llms import OpenAI

import streamlit as st
from configure import configure_pinecone
from vector import query_vector

st.set_page_config(page_title="Chat with t∞ether AI ", page_icon="icon.svg",
                    initial_sidebar_state="auto",layout="centered", menu_items=None)
st.title("Chat with t∞ether Ai")

openai.api_key = st.secrets.openai_key
configure_pinecone()
pinecone_index_name = "together"



company = {

    "Cloudlytics Solutions":[
        "None",
        "Cloud Solutions Architect","SaaS Product Manager",
                             "DevOps Engineer","Cloud Security Specialist",
                             "Sales Development Representative (SDR)",
                             "Customer Success Manager","Cloud Data Analyst",
                             "SaaS Implementation Consultant","Cloud Software Engineer",
                             "Technical Support Specialist"],
    "MediTech Innovations":[
                "None",
                "Medical Device Engineer","Clinical Research Associate",
                "Regulatory Affairs Specialist","Product Development Manager"
                ,"Quality Assurance Analyst","Biomedical Engineer",
                "Medical Device Sales Representative","Manufacturing Technician"
                ,"Research and Development Scientist","Medical Device Project Manager"
    ],
    "LegalEdge LLP":[
                "None",
                "Senior Legal Counsel",
                "Associate Attorney",
                "Legal Consultant",
                "Contract Manager",
                "Compliance Officer",
                "Litigation Specialist",
                "Paralegal",
                "Corporate Counsel",
                "Legal Researcher",
                "Document Review Specialist"
    ]
}


default_company = "Cloudlytics Solutions"
selected_postion = None
searching_keywords = ["find","search","finds"]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="t∞ether, Loading and indexing.. Hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data/CV", recursive=True)
        docs = reader.load_data()

        llm = OpenAI(model="gpt-3.5-turbo",
                     temperature=0.5, system_prompt="You are an HR expert and your job is to help the manager writing a open job position. Always the Job description should have; Job title, required skills, and payment info.")
        service_context = ServiceContext.from_defaults(llm=llm)
        index = GPTVectorStoreIndex.from_documents(
            docs, service_context=service_context)
        return index

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
        st.session_state.messages = [
            {"role": "assistant", "content": "Which job position to want search CV for.","position":company[default_company]}
        ]
index = load_data()
    #    chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True,
    #                                   system_prompt="You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features.")

if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(
            chat_mode="condense_question", verbose=True)

if "selected_postion" not in st.session_state:
    st.session_state.selected_postion = "None"

   
    # Prompt for user input and save to chat history/
if prompt := st.chat_input("Your question"):
        # prompt = "If the following request for job ad, not providing; Job title, required skills, or payment info, then ask them for that information." + prompt
        st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: 

    # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message.get("position") is not None:
            selected_postion = st.radio("Positions:",message["position"])

    # If last message is not from assistant, generate a new response
def is_search_query(query:str)->bool:
    for keyword in searching_keywords:
        if keyword in query:
            return True
    return False

if st.session_state.messages[-1]["role"] != "assistant":
    if prompt and is_search_query(prompt) is False:
        with st.chat_message("assistant"):
            with st.spinner("Thinking...👋"):
                response = st.session_state.chat_engine.chat(prompt)
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                # Add response to message history
                st.session_state.messages.append(message)
    else:
        with st.chat_message("assistant"):
            with st.spinner("Searching Sepecific...👋"):
                response = query_vector(pinecone_index_name,"Give me the name of all CV who are is who are more matched to "+str(prompt))
                st.write(response)
                message = {"role": "assistant", "content": response}
                # Add response to message history
                st.session_state.messages.append(message)
elif  st.session_state.messages[-1]["role"] == "assistant" and selected_postion != st.session_state.selected_postion:
    st.session_state.selected_postion = selected_postion
    with st.chat_message("assistant"):
            with st.spinner("Searching all...👋"):
                response = query_vector(pinecone_index_name,"Give me the name of all CV who are more convenable to ths is job position: "+str(selected_postion))
                st.write(response)
                message = {"role": "assistant", "content": response}
                # Add response to message history
                st.session_state.messages.append(message)
                
