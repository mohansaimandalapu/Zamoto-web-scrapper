import streamlit as st
from transformers import pipeline
from pathlib import Path


st.markdown('<h1 align="center"> RESTAURENT REVIEW SENTIMET ANLYSIS </h1>',unsafe_allow_html=True)
Feedback = st.text_input("enter review",None)
if Feedback == 'None':
    st.markdown(f"""<h4 align="center">Enter review of the resturent get stentiment analysis</h4>""",unsafe_allow_html=True)
else:
    classifier = pipeline('sentiment-analysis')
    result = classifier(f'{Feedback}')
    if result[0]['label'] == 'POSITIVE':
        st.markdown('<center><img src="https://imgur.com/wTZdKbl.png" alt="centered image"> </center>', unsafe_allow_html=True)
        st.markdown(f"""<h1 align="center"> Positive Feedback </h1>""",unsafe_allow_html=True)
    else:
        st.markdown('<center><img src="https://imgur.com/MuIhUuo.png" alt="centered image"> </center>', unsafe_allow_html=True)
        st.markdown(f"""<h1 align="center"> Negitive Feedback </h1>""",unsafe_allow_html=True)

