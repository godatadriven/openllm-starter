import streamlit as st
import time


@st.cache_data()
def load_model():
    return None


def predict(model, input_text):
    time.sleep(1)  # Simulate inference time
    return "This is a response from the chat bot. Use your model here."


def prepare_for_predict(chat_history):
    text = "\nYou are a chat bot and reply to user input messages.\n\n"
    for message in chat_history[::-1]:
        if "user" in message:
            text += f"User: {message['user']}\n"
        elif "response" in message:
            text += f"Response: {message['response']}\n"
    text += "Response: "
    return text


model = load_model()

st.title("Chat Interface")

# Init chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Allow user to delete all previous messages
if st.button("Clear history"):
    st.session_state.chat_history = []
    st.experimental_rerun()

# Allow user to send a message to the chatbot
with st.form(key="message_form"):
    user_input = st.text_input("Type your message here:")

    if st.form_submit_button("Send"):
        if user_input:
            st.session_state.chat_history.insert(0, {"user": user_input})
            user_input = ""

# Add custom CSS to display messages in a pretty way
st.markdown(
    """
    <style>
        .user-msg {
            background-color: #DCF8C6;
            border-radius: 15px;
            padding: 10px;
            display: inline-block;
            max-width: 80%;
        }
        .response-msg {
            background-color: #ECECEC;
            border-radius: 15px;
            padding: 10px;
            display: inline-block;
            max-width: 80%;
        }
        .right-align {
            text-align: right;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display messages
for message in st.session_state.chat_history:
    if "user" in message:
        st.markdown(f"<div class='user-msg'>{message['user']}</div>", unsafe_allow_html=True)
    elif "response" in message:
        st.markdown(
            f"<div class='right-align'><div class='response-msg'>{message['response']}</div></div>",
            unsafe_allow_html=True,
        )


# Generate response to last user message
if len(st.session_state.chat_history) and "user" in st.session_state.chat_history[0]:
    response = predict(model, prepare_for_predict(st.session_state.chat_history))
    st.session_state.chat_history.insert(0, {"response": response})
    st.experimental_rerun()
