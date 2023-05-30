import glob
import os
import streamlit as st
from langchain.document_loaders import PyMuPDFLoader
from openai.embeddings_utils import get_embedding
from openai.embeddings_utils import cosine_similarity
import numpy as np
import openai
import pandas as pd

OPENAI_API_KEY = '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'


def backend_process(JD):
    pdf_cvs = glob.glob('*.pdf')
    loader = []
    for i in range(len(pdf_cvs)):
        pass
        # nm = pdf_cvs[i].name
        loader.append(PyMuPDFLoader(pdf_cvs[i]))
    datas = []
    for i in range(len(loader)):
        datas.append(loader[i].load())
    openai.api_key = OPENAI_API_KEY

    df = pd.DataFrame()
    data = {'Name': ['Aiyana'],
            'text': ['gsa']}
    df = pd.DataFrame(data)
    for i in range(len(datas)):
        text = ''
        print()
        for j in range(len(datas[i])):
            text = text + datas[i][j].page_content
        new_row = {'Name': datas[i][j].metadata['source'], 'text': text}
        df.loc[len(df)] = new_row
    df = df[1:]

    df['embedding'] = df['text'].apply(lambda x: get_embedding(x, engine='text-embedding-ada-002'))
    df.to_csv('embeddings.csv')

    df = pd.read_csv('embeddings.csv')
    df['embedding'] = df['embedding'].apply(eval).apply(np.array)

    search_term_vector = get_embedding(JD, engine='text-embedding-ada-002')
    # search_term_vector

    df['Similarities'] = df['embedding'].apply(lambda x: cosine_similarity(x, search_term_vector))
    df = df.sort_values(by='Similarities', ascending=False)
    df.drop(['embedding', 'text'], axis=1, inplace=True)
    df.reset_index(inplace=True)
    df = df.drop(['index', 'Unnamed: 0'], axis=1)
    # df['Questions'] = st.button('Generate Questions')
    # print(datas[0])
    return df, datas

def generate_resume_questions(resume_text):
    openai.api_key = OPENAI_API_KEY

    # Define the prompt
    prompt = f"Resume: {resume_text}\nQuestions:"

    # Generate questions using OpenAI
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
        n=5,
        stop=None,
    )

    # Extract the generated questions from the API response
    questions = [choice['text'].strip() for choice in response.choices]

    return questions