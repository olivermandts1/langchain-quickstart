import streamlit as st
from openai import OpenAI

# Set up the Streamlit page
st.set_page_config(page_title="🦜🔗 Prompt Chaining Sandbox")
st.title('🔗 Prompt Chaining Sandbox')
st.caption('Create prompt chains that take outputs from one prompt to be used as inputs for another prompt')

# User inputs their OpenAI API key in the sidebar
openai_api_key = st.sidebar.text_input('OpenAI API Key')

# Function to generate response using OpenAI API
def generate_response(system_prompt, user_prompt, model="gpt-4", temperature=0):
    client = OpenAI(api_key=openai_api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature
    )

    return response.choices[0].message.content.strip('"')

# Streamlit form for user input
with st.form('my_form'):
    # Model selection
    model = st.selectbox('OpenAI Model', ('gpt-3.5-turbo', 'gpt-4'))

    # Temperature setting
    temperature = st.number_input('Temperature', min_value=0.0, max_value=1.0, value=0)

    # Text inputs for system, user, and assistant prompts
    system_prompt = st.text_area('System Prompt:')
    user_prompt = st.text_area('User Prompt')
    
    # Form submission button
    submitted = st.form_submit_button('Submit')

    if submitted:
        if not openai_api_key:
            st.warning('Please enter your OpenAI API key!', icon='⚠️')
        else:
            # Generating response
            response = generate_response(system_prompt, user_prompt, model, temperature)
            st.info("Generated Response: " + response)

