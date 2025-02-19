# -*- coding: utf-8 -*-
"""
PDF_assistant_LangChain.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15LbPzzkVyF-LpfpH906IeCz6PEr5B0Ns

# Quickstart: Querying PDF With Astra and LangChain

### A question-answering demo using Astra DB and LangChain, powered by Vector Search

#### Pre-requisites:

You need a **_Serverless Cassandra with Vector Search_** database on [Astra DB](https://astra.datastax.com) to run this demo. As outlined in more detail [here](https://docs.datastax.com/en/astra-serverless/docs/vector-search/quickstart.html#_prepare_for_using_your_vector_database), you should get a DB Token with role _Database Administrator_ and copy your Database ID: these connection parameters are needed momentarily.

You also need an [OpenAI API Key](https://cassio.org/start_here/#llm-access) for this demo to work.

#### What you will do:

- Setup: import dependencies, provide secrets, create the LangChain vector store;
- Run a Question-Answering loop retrieving the relevant headlines and having an LLM construct the answer.

"""Import the packages you'll need:"""

# LangChain components to use
from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings

# Support for dataset retrieval with Hugging Face
from datasets import load_dataset

# With CassIO, the engine powering the Astra DB integration in LangChain,
# you will also initialize the DB connection:
import cassio

!pip install PyPDF2

from PyPDF2 import PdfReader


cqlsh = cassio.CqlSession(token=ASTRA_DB_APPLICATION_TOKEN, keyspace="langchain")

"""Create a vector store and index:"""

embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
astra_vector_store = Cassandra(cqlsh, vector_size=1536)
astra_vector_index = VectorStoreIndexWrapper(astra_vector_store)

"""Load a sample PDF document:"""

pdf_path = "sample.pdf"  # Specify the path to your PDF file
reader = PdfReader(pdf_path)
text = ""
for page in reader.pages:
    text += page.extract_text()

"""Insert the document into the vector store:"""

astra_vector_store.add_documents([text], embeddings)

"""Run a question-answering loop:"""

llm = OpenAI(api_key=OPENAI_API_KEY)

while True:
    query_text = input("Enter your question (or type 'quit' to exit): ").strip()
    if query_text.lower() == "quit":
        break

    if query_text == "":
        continue

    answer = astra_vector_index.query(query_text, llm=llm).strip()
    print("ANSWER: \"%s\"\n" % answer)

    print("FIRST DOCUMENTS BY RELEVANCE:")
    for doc, score in astra_vector_store.similarity_search_with_score(query_text, k=4):
        print("    [%0.4f] \"%s ...\"" % (score, doc.page_content[:84]))

import random

def generate_mcqs(question, answer):
    mcqs = []
    options = [answer]
    # Add the correct answer to the options list
    for _ in range(3):
        # Generate 3 incorrect options randomly
        while True:
            incorrect_option = astra_vector_index.query(question, llm=llm).strip()
            if incorrect_option not in options:
                options.append(incorrect_option)
                break
    # Shuffle the options
    random.shuffle(options)
    # Generate the MCQ format
    for i, option in enumerate(options, start=1):
        if option == answer:
            mcq = f"{chr(65 + i)}) {option} (Correct)"
        else:
            mcq = f"{chr(65 + i)}) {option}"
        mcqs.append(mcq)
    return mcqs

first_question = True
all_answers = []

while True:
    if first_question:
        query_text = input("\nEnter your question (or type 'quit' to exit): ").strip()
    else:
        query_text = input("\nWhat's your next question (or type 'quit' to exit): ").strip()

    if query_text.lower() == "quit":
        break

    if query_text == "":
        continue

    first_question = False

    print("\nQUESTION: \"%s\"" % query_text)
    answer = astra_vector_index.query(query_text, llm=llm).strip()
    print("ANSWER: \"%s\"\n" % answer)

    # Generate MCQs
    mcqs = generate_mcqs(query_text, answer)
    all_answers.append((query_text, answer))  # Store question-answer pair

    # Display MCQs
    for i, mcq in enumerate(mcqs, start=1):
        print(f"{i}. {mcq}")

# Display all correct answers at the end
print("\nCorrect Answers:")
for question, answer in all_answers:
    print(f"\nQuestion: {question}")
    print(f"Answer: {answer}")
