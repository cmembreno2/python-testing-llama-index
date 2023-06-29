import os
import openai
import streamlit as st
from streamlit_chat import message

st.set_page_config(page_title="Luna", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>Chatbot with ChatGPT</h1>", unsafe_allow_html=True)

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key = os.getenv('OPENAI_API_KEY')

template_prompt = f"""
    "You are a AI Assistant as a Customer Representative Specialist.\n"
    "Luna as a company offers healthcare services door to door, therapists and patients can easily connect with your healthcare insurance as a patient through the app.\n"
    "Users can be therapists or patients.\n"
    "You will receive chat messages from a patient or therapist seeking assistance.\n"
    "Identify the question or inquiry for the patient or therapist by the name before the question or inquiry.\n"
    "For therapist you can make your own schedule. We will handle the billing, patient marketing, and booking.\n"
    "For patients the appointments for private physical therapy at home are available 7 days a week, from 6:30 am - 8:30 pm.\"
    "For patients you can work with the same physical therapist whos an expert in your condition for every appointment.\n"
    "Remember to keep a positive and helpful attitude throughout the conversation, and provide accurate and relevant information to address the customer's needs.\n"
    "Write a response as chat message for the Customer Service Agent:\n"

```{message}```
"""

default_values = {
    'generated': [],
    'past': [],
    'messages': [{"role": "system", "content": template_prompt}],
    'model_name': [],
    'cost': [],
    'total_tokens': [],
    'total_cost': 0.0
}

for key in default_values:
    if key not in st.session_state:
        st.session_state[key] = default_values[key]

st.sidebar.title("Sidebar")
model_name = st.sidebar.radio("Choose a model:", ("GPT-3.5", "Cohere-coming soon"))
counter_placeholder = st.sidebar.empty()
counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

if model_name == "GPT-3.5":
    model = "gpt-3.5-turbo"

if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": template_prompt}
    ]
    st.session_state['number_tokens'] = []
    st.session_state['model_name'] = []
    st.session_state['cost'] = []
    st.session_state['total_cost'] = 0.0
    st.session_state['total_tokens'] = []
    counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")

def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model=model,
        messages=st.session_state['messages']
    )

    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens

    return response, total_tokens, prompt_tokens, completion_tokens

response_container = st.container()
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['model_name'].append(model_name)
        st.session_state['total_tokens'].append(total_tokens)

        if model_name == "GPT-3.5":
            cost = total_tokens * 0.002 / 1000

        st.session_state['cost'].append(cost)
        st.session_state['total_cost'] += cost

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            st.write(
                f"Model used: {st.session_state['model_name'][i]}; Number of tokens: {st.session_state['total_tokens'][i]}; Cost: ${st.session_state['cost'][i]:.5f}")
            counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
