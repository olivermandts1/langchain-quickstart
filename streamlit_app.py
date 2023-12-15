import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="🦜🔗 Quickstart App")
st.title('🦜🔗 Quickstart App')
st.header('Testing for formatating?')

openai_api_key = st.sidebar.text_input('OpenAI API Key')

def generate_response(input_text, model="gpt-3.5-turbo"):
    client = OpenAI(api_key=openai_api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "user", "content": input_text}
        ]
    )

    return response.choices[0].message.content.strip('"')

with st.form('my_form'):
    text1 = st.text_area('Enter text:', 'Write me 1 short headline marketing SUV deals')
    text2 = st.text_area('Does this even work?')
    submitted = st.form_submit_button('Submit')

    if submitted:
        if not openai_api_key:
            st.warning('Please enter your OpenAI API key!', icon='⚠️')
        else:
            headline = generate_response(text1)
            st.info("Generated Headline: " + headline)