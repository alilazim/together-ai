#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from glob import glob

from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import Pinecone

from configure import configure_openai, configure_pinecone
from data_interfaces import document_loaders


def store_vectores(document, index):
    load_documents = document_loaders(document)
    embedding_model = OpenAIEmbeddings()
    cv_buffer = [str(d.page_content)+"[source:" +
                 str(d.metadata)+"]" for d in load_documents]
    combined_field = []
    temp = ""
    for field in cv_buffer:
        temp += field + "\n"
    # Make only one vector even if the upload cv is 2 or more pages
    combined_field.append(temp)
    docsearch = Pinecone.from_texts(
        combined_field, embedding_model, index_name=index)
    print(f"Vector Stored {document} with success")


def query_vector(index_name, query):
    embedding_model = OpenAIEmbeddings()
    llm = OpenAI(temperature=0)
    chain = load_qa_chain(llm, chain_type="refine")
    index_search = Pinecone.from_existing_index(index_name, embedding_model)
    docs = index_search.similarity_search(query)
    response = chain.run(input_documents=docs, question=query)
    return response


if __name__ == "__main__":
    configure_openai()
    configure_pinecone()
    prompt = """

**Job Title:** Web Developer with Blockchain Experience

**Location:** United States (Location flexible, remote work available)


**Job Description:**

Are you an experienced Web Developer with a passion for blockchain technology? Do you have a proven track record of creating innovative and secure web applications? If you're ready to join a dynamic team that values creativity and cutting-edge solutions, we want to hear from you!

**Key Responsibilities:**

- Develop and maintain web applications with a strong focus on security and performance.
- Collaborate with cross-functional teams to understand project requirements and deliver high-quality software solutions.
- Utilize blockchain technology to create decentralized applications (DApps) and smart contracts.
- Implement best practices for blockchain development and contribute to the development of blockchain-based solutions.
- Stay up-to-date with emerging technologies and trends in the blockchain space.

**Qualifications:**

- Bachelor's or Master's degree in Computer Science or a related field.
- Minimum of 3 years of professional web development experience.
- Strong proficiency in web development technologies such as HTML, CSS, JavaScript, and modern web frameworks (e.g., React, Angular, Vue.js).
- Experience with blockchain programming and development (e.g., Ethereum, Solidity).
- Familiarity with blockchain concepts, decentralized applications, and smart contracts.
- Knowledge of blockchain security best practices.
- Excellent problem-solving and analytical skills.

**Benefits:**

- Competitive salary and benefits package.
- Flexible work arrangements, including the option for remote work.
- Opportunities for professional development and growth.
- Collaborative and innovative work environment.

**How to Apply:**

If you're a talented Web Developer with a passion for blockchain and you're ready to work on groundbreaking projects, please send your resume and a cover letter explaining why you're the right fit for this role to [Your Application Email].

---
     """
    command = "\n\n\This is job Ads .Give me only the name and the source(the name of cv) of top 10 employees who are more qualified for this job and how much they match  in percentage. for example if it it five persone, the first persone must have the highest percentage and the last the lowest."
    final_prompt = prompt + command
    # cvs = glob("../Resumes/*.*")
    # for cv in cvs:
    #    store_vectores(cv,"together")
    print(query_vector("together", final_prompt))
