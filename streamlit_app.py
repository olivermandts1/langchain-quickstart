import streamlit as st
from langchain.llms import OpenAI
st.set_page_config(page_title="🦜🔗 Quickstart App")
st.title('🦜🔗 Quickstart App')

openai_api_key = st.sidebar.text_input('OpenAI API Key')

def generate_response(input_text):
    # Specify the model name here. For example, "gpt-3.5-turbo", "text-davinci-003", etc.
    model_name = "gpt-3.5-turbo"  # Replace with your desired model

    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key, model=model_name)
    st.info(llm(input_text))

with st.form('my_form'):
    text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
    submitted = st.form_submit_button('Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submitted and openai_api_key.startswith('sk-'):
        generate_response(text)
