import streamlit as st
import os.path
import pathlib
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader
from PIL import Image

openai.api_key = st.secrets.openai_key
st.set_page_config(page_title="SME: t∞ether ai", page_icon="icon.svg",
                   layout="centered", initial_sidebar_state="auto", menu_items=None)

st.title("SME: Upload your CV with t∞ether")

uploaded_file = st.file_uploader("Upload your CV")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = uploaded_file.getvalue().decode('utf-8').splitlines()
    st.session_state["preview"] = ''

    for i in range(0, min(5, len(data))):
        st.session_state["preview"] += data[i]

preview = st.text_area("CV Preview", "", height=150, key="preview")
upload_state = st.text_area("Upload State", "", key="upload_state")


def upload():
    if uploaded_file is None:
        st.session_state["upload_state"] = "Upload a file first!"
    else:
        data = uploaded_file.getvalue().decode('utf-8')
        parent_path = pathlib.Path(__file__).parent.parent.resolve()
        save_path = os.path.join(parent_path, "data")
        complete_name = os.path.join(save_path, uploaded_file.name)
        destination_file = open(complete_name, "w")
        destination_file.write(data)
        destination_file.close()
        st.session_state["upload_state"] = "Saved " + \
            complete_name + " successfully!"


st.button("Upload file to Sandbox", on_click=upload)
