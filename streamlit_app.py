import streamlit as st
from openai import OpenAI

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

# Function to generate response using OpenAI API
def generate_response(system_prompt, user_prompt, model="gpt-4", temperature=0.00):
    client = OpenAI(api_key=openai_api_key)

    # Map the friendly model name to the actual model ID
    model_id = {
        'gpt-3.5-turbo': 'gpt-3.5-turbo',
        'gpt-4': 'gpt-4',
        'gpt-3.5-turbo-asset-templatization-model-1': 'ft:gpt-3.5-turbo-1106:personal::8ceweUNE',
        'gpt-3.5-turbo-asset-templatization-model-2' : 'ft:gpt-3.5-turbo-1106:personal::8ch5oXdo',
        'gpt-3.5-turbo-asset-templatization-model-3' : 'ft:gpt-3.5-turbo-1106:personal::8dNEkYP7',
        'gpt-3.5-turbo-asset-templatization-model-4' : 'ft:gpt-3.5-turbo-1106:personal::8epn5CVM',
        'gpt-3.5-turbo-angle-classification-model-1' : 'ft:gpt-3.5-turbo-1106:personal::8epdhWtH'
    }.get(model, model)  # Default to the provided model name if it's not in the dictionary

    response = client.chat.completions.create(
        model=model_id,
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
        model = st.selectbox('OpenAI Model', 
                             ('gpt-3.5-turbo', 'gpt-4', 'gpt-3.5-turbo-asset-templatization-model-1','gpt-3.5-turbo-asset-templatization-model-2','gpt-3.5-turbo-asset-templatization-model-3','gpt-3.5-turbo-asset-templatization-model-4','gpt-3.5-turbo-angle-classification-model-1'), 
                             key=f'model_{i}')
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
            # Retrieve the model and temperature specific to each form
            current_model = st.session_state[f'model_{i}']
            current_temperature = st.session_state[f'temp_{i}']

            # Get the current system and user prompts
            current_system_prompt = st.session_state[f'system_{i}']
            current_user_prompt = st.session_state[f'user_{i}']

            # Apply dynamic replacements to both system and user prompts
            for j in range(i):
                replacement_text = st.session_state['responses'][j]
                current_system_prompt = current_system_prompt.replace(f'[output {j+1}]', replacement_text)
                current_user_prompt = current_user_prompt.replace(f'[output {j+1}]', replacement_text)

            # Pass the specific model and temperature for each form
            response = generate_response(current_system_prompt, current_user_prompt, current_model, current_temperature)
            st.session_state['responses'].append(response)
            st.text(f"**Generated Response {i+1}:** \n\n{response}")
