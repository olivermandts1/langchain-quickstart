import streamlit as st
from openai import OpenAI

# Set up the Streamlit page
st.set_page_config(page_title="🦜🔗 Prompt Chaining Sandbox")
st.title('🔗 Prompt Chaining Sandbox')
st.caption('Create prompt chains that take outputs from one prompt to be used as inputs for another prompt')

# User inputs their OpenAI API key in the sidebar
openai_api_key = st.sidebar.text_input('OpenAI API Key')

# Initialize or update the session state for form count and responses
if 'form_count' not in st.session_state:
    st.session_state['form_count'] = 1
if 'responses' not in st.session_state:
    st.session_state['responses'] = []

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

# Create expanders for each set of inputs
for i in range(st.session_state['form_count']):
    with st.expander(f"Chain Link {i+1}", expanded=True):
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
        for i in range(st.session_state['form_count']):
            user_prompt_with_replacements = st.session_state[f'user_{i}']
            for j in range(i):
                user_prompt_with_replacements = user_prompt_with_replacements.replace(f'[output {j+1}]', st.session_state['responses'][j])

            response = generate_response(st.session_state[f'system_{i}'], user_prompt_with_replacements, model, temperature)
            st.session_state['responses'].append(response)
            st.info(f"Generated Response {i+1}: " + response)
