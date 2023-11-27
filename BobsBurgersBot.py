import streamlit as st
import os
import google.cloud.dialogflow_v2 as dialogflow
import google.generativeai as palm
import random
import json
import tempfile
import time
from streamlit_extras.let_it_rain import rain 

# local imports
# import GenAIParameters as genai
import v2_GenAIParameters_v2 as genai_v2

def version_info():
    # write the markdown file VersionInformation.md to st.write()
    with open("VersionInformation.md", "r") as f:
        st.markdown(f.read())

def format_prompt(message):
    return (f"Please answer within 250 characters. {message}. The response must be based on the personality, backstory, and knowledge base that you have. The answer must be concise and short.")

def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)

def burger_rain():
    rain(
        emoji="🍔",
        font_size=54,
        falling_speed=5,
        animation_length=5,
    )

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


if "debug" not in st.session_state:
    st.session_state.debug = 0
debug = st.session_state.debug

# Streamlit setup
st.title("Bob's Burgers Chatbot")

with st.expander("Version Information"):
    version_info()

# conversation = []  # Store the entire conversation
if "conversation" not in st.session_state:
    st.session_state.conversation = []
else:
    st.write("Chat History:")

# Display the conversation
for message in st.session_state.conversation:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# user_input = st.text_input("You:", "")
if user_input := st.chat_input("Enter your message:"):

# if st.button("Send"):
    user_message = user_input.strip()
    # if user message contains the word burger, then rain burgers
    if "burger" in user_message.lower():
        burger_rain()
    # if user message contains birthday, celebrate, or balloon, then rain balloons
    if "birthday" in user_message.lower() or "celebrate" in user_message.lower() or "balloon" in user_message.lower():
        st.balloons()
    if user_message == "debug":
        #flip the value of debug between 0 and 1
        if debug == 0:
            debug = 1
            version_info()
        else:
            debug = 0
        print("Debug: ", debug)
        st.write("Debug: ", debug)
        st.session_state.debug = debug

    elif user_message == "version":
        version_info()

    # elif user_message == "image":
    #     st.image("louse1.svg", caption="Louise", use_column_width=True)
    #     st.image("louse2.svg", caption="Louise", use_column_width=True)
    #     st.image("louise3.svg", caption="Louise", use_column_width=True)

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

        if debug == 1:
            st.write("Dialogflow response:", response)
        if response.query_result.intent.display_name != "Default Fallback Intent":
            assistant_response = response.query_result.fulfillment_text
            # extra easter eggs
            if response.query_result.intent.display_name == "nick.eastereggs.snow":
                st.snow()
            # if response.query_result.intent.display_name == "nick.eastereggs.balloons":
            #     st.balloons()
        else:
            # with st.spinner("Louise is busy with customers. Please wait..."):

            # Grab a random away_message to display while we wait
            away_message = random.choice(genai_v2.away_messages)
            # prepend the message with the text "Louise is away. Status: "
            away_message = "Louise is away: " + away_message
            with st.spinner(away_message):
                            
                # Send the conversation to Generative AI
                conversation_text = []
                for message in st.session_state.conversation:
                    if message["role"] == "user":
                        conversation_text.append(format_prompt(message["content"]))
                    else:
                        conversation_text.append(message["content"])

                if debug == 1:
                    st.write("Conversation Text: ", conversation_text)
                full_response = palm.chat(
                    context=genai_v2.overall_context,
                    examples=genai_v2.examples,
                    messages=conversation_text,
                    **genai_v2.defaults  # Include Generative AI defaults
                )
                if debug == 1:
                    st.write("Full assistant response: ", full_response )
                assistant_response = full_response.last  
                
                # If the generative AI response starts with "Louise: " or "Louise Belcher:", remove it
                if assistant_response.startswith("Louise: "):
                    assistant_response = assistant_response[8:]
                elif assistant_response.startswith("Louise Belcher: "):
                    assistant_response = assistant_response[16:]
                
        # Check and make sure the response is not empty
        if not assistant_response:
            assistant_response = "Yeah, I'm not even going to try to respond to that."

        st.session_state.conversation.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            # st.markdown(assistant_response)
            typewriter(text=assistant_response, speed=9)
            #Sample Example
# text = "This is an example of streamlit text with typewriter effect :)"
# typewriter(text=text, speed=speed)
