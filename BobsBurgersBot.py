import streamlit as st
import os
import google.cloud.dialogflow_v2 as dialogflow
import google.generativeai as palm
import random
import json
import tempfile
# local imports
import GenAIParameters as genai
import VersionInformation as vi

# Write the credentials to a temporary file
with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
    temp.write(json.dumps(st.secrets["dialog_flow_file"].to_dict()))
    temp_path = temp.name
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_path

# Initialize Dialogflow client within try block to make sure
# we can nuke the temp file even if it crashes and burns
try:
    # Set the environment variable to point to the temporary file
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_path
    
    # Initialize Dialogflow client
    project_id = "bobsburgersbot"
    session_id = random.randint(0, 100000)
    client = dialogflow.SessionsClient()
finally:
    # Delete the temporary file
    os.unlink(temp_path)

# Configure Generative AI
palm.configure(api_key=st.secrets["palm_apikey"])

# Generative AI settings
defaults = genai.defaults
context = genai.context
examples = genai.examples

if "debug" not in st.session_state:
    st.session_state.debug = 0
debug = st.session_state.debug

# Streamlit setup
st.title("Bob's Burgers Chatbot")
st.write("Chat History:")

# conversation = []  # Store the entire conversation
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Display the conversation
for message in st.session_state.conversation:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# user_input = st.text_input("You:", "")
if user_input := st.chat_input("You:"):

# if st.button("Send"):
    user_message = user_input.strip()

    if user_message == "debug":
        #flip the value of debug between 0 and 1
        if debug == 0:
            debug = 1
        else:
            debug = 0
        print("Debug: ", debug)
        st.write("Debug: ", debug)
        st.session_state.debug = debug
    elif user_message == "version":
        st.write("Version: ", vi.version)
        st.write("Date: ", vi.date)
        st.write("Changelog: ", vi.changelog)
    elif user_message:
        st.session_state.conversation.append({"role": "user", "content": user_message})
        with st.chat_message("user"):
            st.markdown(user_message)

        # Dialogflow
        query_input = dialogflow.types.QueryInput()
        text_input = dialogflow.types.TextInput(
            text=user_message,
            language_code="en"
        )
        query_input.text = text_input
        request = dialogflow.types.DetectIntentRequest(
            session=client.session_path(project_id, session_id),
            query_input=query_input,
        )
        response = client.detect_intent(request)

        if response.query_result.intent.display_name != "Default Fallback Intent":
            assistant_response = response.query_result.fulfillment_text
            # extra easter eggs
            if response.query_result.intent.display_name == "nick.eastereggs.snow":
                st.snow()
        else:
            # assistant_response = ""
            with st.spinner("Louise is busy with customers. Please wait..."):
                            
                # Send the conversation to Generative AI
                conversation_text = [message["content"] for message in st.session_state.conversation]
                if debug == 1:
                    st.write("Conversation Text: ", conversation_text)
                assistant_response = palm.chat(
                    context=genai.context,
                    examples=genai.examples,
                    messages=conversation_text,
                    **genai.defaults  # Include Generative AI defaults
                    # **defaults  # Include Generative AI defaults
                ).last
                if debug == 1:
                    full_response = palm.chat(
                    context=genai.context,
                    examples=genai.examples,
                    messages=conversation_text,
                    **genai.defaults  # Include Generative AI defaults
                    # **defaults  # Include Generative AI defaults
                )
                    st.write("Full assistant response: ", full_response )
                
        # Check and make sure the response is not empty
        if not assistant_response:
            assistant_response = "Yeah, I'm not even going to try to respond to that."

        st.session_state.conversation.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
