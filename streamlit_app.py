import streamlit as st
from openai import OpenAI
import logging
import pandas as pd

# Set up the Streamlit page
st.set_page_config(page_title="🦜🔗 Prompt Chaining Sandbox")
st.title('🔗 Prompt Chaining Sandbox')
st.subheader('Create prompt chains that take outputs from one prompt to be used as inputs for another prompt')

# Instructions text box
instructions = """
    **Instructions:**
    Use the `[output #]` dynamic replacement to reference the outputs from any previous prompts in your new prompt.

    **Example:** 
    - Prompt 1 output was ‘Best SUV Deals’
    - In prompt 2, the dynamic replacement `[Output 1]` will send ‘Best SUV Deals’ where that dynamic replacement is in your second prompt.
    """
st.info(instructions)

# User inputs their OpenAI API key in the sidebar
openai_api_key = st.secrets["openai_secret"]

# Initialize or update the session state for form count and responses
if 'form_count' not in st.session_state:
    st.session_state['form_count'] = 1
if 'responses' not in st.session_state:
    st.session_state['responses'] = []

# Setup logging
logging.basicConfig(filename='prompt_chain_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

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

# Function to log form data and responses
def log_data(form_data, responses):
    for i, data in enumerate(form_data):
        logging.info(f"Form {i+1}: Model: {data['model']}, Temperature: {data['temperature']}, System Prompt: {data['system_prompt']}, User Prompt: {data['user_prompt']}, Response: {responses[i]}")

# Function to read log and convert to DataFrame
def read_log_to_df():
    with open('prompt_chain_log.txt', 'r') as file:
        lines = file.readlines()

    log_data = []
    for line in lines:
        timestamp, info = line.split(' - ')
        form_number, details = info.split(': ', 1)
        form_data = {'timestamp': timestamp, 'form_number': form_number}
        for item in details.split(', '):
            key, value = item.split(': ', 1)
            form_data[key.strip()] = value.strip()
        log_data.append(form_data)

    return pd.DataFrame(log_data)

# Function to add a new prompt
def add_prompt():
    st.session_state['form_count'] += 1

# Function to remove the latest prompt
def remove_prompt():
    if st.session_state['form_count'] > 1:
        st.session_state['form_count'] -= 1

# Buttons to add or remove a prompt
col1, col2 = st.columns(2)
with col1:
    st.button('Add Prompt', on_click=add_prompt)
with col2:
    st.button('Remove Prompt', on_click=remove_prompt)

# Create expanders for each set of inputs
for i in range(st.session_state['form_count']):
    with st.expander(f"Chain Link {i+1}", expanded=False):
        model = st.selectbox('OpenAI Model', ('gpt-3.5-turbo', 'gpt-4'), key=f'model_{i}')
        temperature = st.number_input('Temperature', min_value=0.00, max_value=1.00, value=0.00, key=f'temp_{i}')
        system_prompt = st.text_area('System Prompt:', key=f'system_{i}')
        user_prompt = st.text_area('User Prompt', key=f'user_{i}')

# Single submit button for all inputs
if st.button('Submit All'):
    if not openai_api_key:
        st.warning('Please enter your OpenAI API key!', icon='⚠️')
    else:
        st.session_state['responses'] = []
        form_data = []  # Collect form data for logging

        for i in range(st.session_state['form_count']):
            current_model = st.session_state[f'model_{i}']
            current_temperature = st.session_state[f'temp_{i}']

            user_prompt_with_replacements = st.session_state[f'user_{i}']
            for j in range(i):
                user_prompt_with_replacements = user_prompt_with_replacements.replace(f'[output {j+1}]', st.session_state['responses'][j])

            response = generate_response(st.session_state[f'system_{i}'], user_prompt_with_replacements, current_model, current_temperature)
            st.session_state['responses'].append(response)
            st.markdown(f"**Generated Response {i+1}:** \n\n{response}")

            form_data.append({
                'model': current_model,
                'temperature': current_temperature,
                'system_prompt': st.session_state[f'system_{i}'],
                'user_prompt': user_prompt_with_replacements
            })

        # Log the data
        log_data(form_data, st.session_state['responses'])

# Sidebar for logs
with st.sidebar:
    st.header("Logs")
    if st.button('Load Log'):
        log_df = read_log_to_df()
        st.dataframe(log_df)
