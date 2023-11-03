#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from glob import glob

from configure import configure_openai, configure_pinecone
from data_interfaces import document_loaders
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pinecone import Pinecone
from llama_index.llms import OpenAI


def store_vectores(document,index):
    load_documents = document_loaders(document)
    embedding_model = OpenAIEmbeddings()
    cv_buffer = [str(d.page_content)+"[source:"+str(d.metadata)+"]" for d in load_documents]
    combined_field = []
    temp = ""
    for field in cv_buffer:
       temp += field + "\n" 
    combined_field.append(temp) # Make only one vector even if the upload cv is 2 or more pages
    docsearch = Pinecone.from_texts(combined_field,embedding_model,index_name = index)
    print(f"Vector Stored {document} with success")

def query_vector(index_name,query):
    embedding_model = OpenAIEmbeddings()
    llm = OpenAI(temperature = 0)
    chain = load_qa_chain(llm,chain_type = "refine")
    index_search = Pinecone.from_existing_index(index_name,embedding_model)
    docs = index_search.similarity_search(query)
    response = chain.run(input_documents = docs,question= query)
    return response
