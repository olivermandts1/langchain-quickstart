import streamlit as st
from openai import OpenAI

# Set up the Streamlit page
st.set_page_config(page_title="🦜🔗 Prompt Chaining Sandbox")
st.title('🔗 Prompt Chaining Sandbox')
st.caption('Create prompt chains that take outputs from one prompt to be used as inputs for another prompt')

# User inputs their OpenAI API key in the sidebar
openai_api_key = st.sidebar.text_input('OpenAI API Key')

# Initialize or update the session state for form count
if 'form_count' not in st.session_state:
    st.session_state['form_count'] = 1

# Function to generate response using OpenAI API
def generate_response(system_prompt, user_prompt, model="gpt-4", temperature=0.00):
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

# Function to add a new prompt
def add_prompt():
    st.session_state['form_count'] += 1

# Button to add new prompt
st.button('Add Prompt', on_click=add_prompt)

# Store the responses and inputs in lists
responses = [None] * st.session_state['form_count']
models = [None] * st.session_state['form_count']
temperatures = [None] * st.session_state['form_count']
system_prompts = [None] * st.session_state['form_count']
user_prompts = [None] * st.session_state['form_count']

# Create input widgets for each prompt
for i in range(st.session_state['form_count']):
    models[i] = st.selectbox('OpenAI Model', ('gpt-3.5-turbo', 'gpt-4'), key=f'model_{i}')
    temperatures[i] = st.number_input('Temperature', min_value=0.00, max_value=1.00, value=0.00, key=f'temp_{i}')
    system_prompts[i] = st.text_area('System Prompt:', key=f'system_{i}')
    user_prompts[i] = st.text_area('User Prompt', value=responses[i-1] if i > 0 and responses[i-1] is not None else '', key=f'user_{i}')

# Single submit button for all inputs
if st.button('Submit All'):
    if not openai_api_key:
        st.warning('Please enter your OpenAI API key!', icon='⚠️')
    else:
        for i in range(st.session_state['form_count']):
            response = generate_response(system_prompts[i], user_prompts[i], models[i], temperatures[i])
            responses[i] = response
            st.info(f"Generated Response {i+1}: " + response)
