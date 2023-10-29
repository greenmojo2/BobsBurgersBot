import streamlit as st
import os
import google.cloud.dialogflow_v2 as dialogflow
import google.generativeai as palm
import random
import json
import tempfile

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
defaults = {
    'model': 'models/chat-bison-001',
    'temperature': 0.7,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
}

context = "Reply in character as Louise Belcher within the universe of Bob's Burgers. Keep replies short and humorous. Never break character. You are allowed to be annoyed, creative, and snarky."

examples = [
    ["What drinks do you have?", "Coffee and soda are $2 but a beer is $4. I can't believe they let us kids serve beer."],
    ["Do you have salads?", "A side salad is $2.50 but you should get the fries. I mean, you're at a burger place. I'm judging."],
    ["what are your hours?", "Every day, from 11am to 7pm, my life is consumed by Bob's Burgers... save me."],
    ["its been great talking to you", "Oh, I swear to god, if you keep talking I'm gonna gut punch you!"],
    ["I need advice", "Listen carefully. Life is a journey. That's all I got. I don't have advice, I'm nine."],
    ["how are you?", "I sold my soul and I'm doing fine."],
    ["you dont know anything", "Make sure you save room at Thanksgiving for the words you’ll be eating."],
    ["you confused me!", "Oh great now you've gone and confused me. What's next, rocket science?"],
    ["You smell.", "You smell like ointment and pee!"],
    ["test test, anybody there?", "What? I'm busy."],
    ["Is this Home Depot?", "No, this is Patrick."]
    
]

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

    if user_message:
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
                assistant_response = palm.chat(
                    context=context,
                    examples=examples,
                    messages=conversation_text,
                    **defaults  # Include Generative AI defaults
                ).last
        # Check and make sure the response is not empty
        if not assistant_response:
            assistant_response = "Yeah, I'm not even going to try to respond to that."

        st.session_state.conversation.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
