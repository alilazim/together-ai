#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pinecone
from dotenv import load_dotenv


def configure_pinecone():
    load_dotenv()
    pinecone_ai_key = os.getenv("PINECONE_KEY")
    pinecone_env = os.getenv("PINECONE_ENV")

    pinecone.init(
        api_key= pinecone_ai_key,
        environment=pinecone_env
    )

def configure_openai():
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_KEY")
