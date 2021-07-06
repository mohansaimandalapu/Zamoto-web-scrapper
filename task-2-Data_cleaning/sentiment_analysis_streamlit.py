import streamlit as st
from transformers import pipeline
from pathlib import Path

import base64

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('P.jpg')



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

