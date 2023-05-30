from typing import List

import streamlit as st
from langchain.schema import Document
import numpy as np
import behind_processes
import preprocessor
import os
import pandas as pd

st.sidebar.title("AXIS Resume Parser")
dummy_result = pd.DataFrame()
tab1, tab2 = st.tabs(['Resume Preference', 'Questions'])
changer = False
with tab1:
    st.caption('Press ctrl+Enter to load JD...', unsafe_allow_html=False, help=None)
    txt = st.text_area('Paste your JD(Job Description) here...', '''''')
    uploaded_files = st.file_uploader("Choose a CVs", type=['pdf'], accept_multiple_files=True)

    def save_uploadedfile(uploaded_file):
        with open(os.path.join("./", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        return 1


    digit = 0
    for uploaded_file in uploaded_files:
        if uploaded_file is not None:
            k = save_uploadedfile(uploaded_file)
            if (k):
                digit += 1

    if (digit != 0):
        if (digit == len(uploaded_files)):
            st.success("All filed uploaded")
            digit = 0
        else:
            st.error("Some Error Occured")

    openings = st.number_input('Number of openings')

    if st.button('Analyze'):
        changer = True
        datas: list[list[Document]]
        result, datas = preprocessor.resume_analyzer(txt)
        st.dataframe(result)
        dummy_result = result
        # os.remove(uploaded_files.name + '')
        # print(stng)
        # df['Questions'] =
if changer:
    with tab2:
        content = []
        for i in range(len(datas)):
            stng = ''
            for j in range(len(datas[i])):
                stng = stng + datas[i][j].page_content
            content.append(stng)
        df1 = dummy_result.copy()
        x = []
        for i in range(len(content)):
            x.append(behind_processes.generate_resume_questions(content[i]))
        
        df1['Questions'] = x
        st.dataframe(df1)
