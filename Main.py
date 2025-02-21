
# from datetime import datetime
# import streamlit as st
# import openai
# from openai import OpenAI
# import time
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# # OpenAI configuration
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# DEFAULT_ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# # Initialize session state variables
# if 'current_assistant_id' not in st.session_state:
#     st.session_state.current_assistant_id = DEFAULT_ASSISTANT_ID
# if 'thread_id' not in st.session_state:
#     st.session_state.thread_id = None
# if 'messages' not in st.session_state:
#     st.session_state.messages = []
# if 'show_timestamps' not in st.session_state:
#     st.session_state.show_timestamps = False
# if 'dark_mode' not in st.session_state:
#     st.session_state.dark_mode = False
# if 'message_count' not in st.session_state:
#     st.session_state.message_count = 0
# if 'temperature' not in st.session_state:
#     st.session_state.temperature = 0.7
# if 'chatbot_title' not in st.session_state:
#     st.session_state.chatbot_title = "Rodney ChatBot"

# # Initialize OpenAI client
# client = OpenAI(api_key=OPENAI_API_KEY)


# def create_new_thread():
#     """Create a new thread and reset messages"""
#     st.session_state.thread_id = client.beta.threads.create().id
#     st.session_state.messages = []
#     st.session_state.message_count = 0


# def process_message(thread_id, user_message):
#     """Process a user message and get the assistant's response"""
#     client.beta.threads.messages.create(
#         thread_id=thread_id,
#         role="user",
#         content=user_message
#     )

#     run = client.beta.threads.runs.create(
#         thread_id=thread_id,
#         assistant_id=st.session_state.current_assistant_id,
#         temperature=st.session_state.temperature
#     )

#     while True:
#         run_status = client.beta.threads.runs.retrieve(
#             thread_id=thread_id,
#             run_id=run.id
#         )
#         if run_status.status == 'completed':
#             break
#         elif run_status.status == 'failed':
#             st.error("Assistant response failed. Please try again.")
#             return None
#         time.sleep(1)

#     messages = client.beta.threads.messages.list(thread_id=thread_id)
#     return messages.data


# def export_chat():
#     """Export chat history as text"""
#     if not st.session_state.messages:
#         return "No messages to export."

#     export_text = "Chat History\n\n"
#     for msg in st.session_state.messages:
#         role = "Assistant" if msg["role"] == "assistant" else "User"
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         export_text += f"{timestamp} - {role}:\n{msg['content']}\n\n"
#     return export_text


# def main():
#     if st.session_state.dark_mode:
#         st.markdown("""
#             <style>
#             .stApp {
#                 background-color: #262626;
#                 color: #FFFFFF;
#             }
#             </style>
#             """, unsafe_allow_html=True)

#     st.title(st.session_state.chatbot_title)

#     with st.sidebar:
#         st.subheader("Chatbot Settings")
#         chatbot_name = st.text_input(
#             "Chatbot Title", value=st.session_state.chatbot_title)
#         if st.button("Update Title"):
#             st.session_state.chatbot_title = chatbot_name
#             st.rerun()

#         st.subheader("Assistant Configuration")
#         new_assistant_id = st.text_input(
#             "Assistant ID", value=st.session_state.current_assistant_id)
#         if st.button("Update Assistant ID"):
#             st.session_state.current_assistant_id = new_assistant_id
#             create_new_thread()
#             st.success("Assistant ID updated! New chat thread created.")
#             st.rerun()

#         st.caption(
#             f"Current Assistant ID: {st.session_state.current_assistant_id}")

#     if st.session_state.thread_id is None:
#         create_new_thread()

#     if prompt := st.chat_input("Type your message here..."):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         st.session_state.message_count += 1
#         messages = process_message(st.session_state.thread_id, prompt)
#         if messages:
#             new_messages = [
#                 {"role": msg.role, "content": msg.content[0].text.value}
#                 for msg in reversed(messages)
#             ]
#             st.session_state.messages = new_messages
#             st.rerun()

#     for message in st.session_state.messages:
#         role = "🤖 Assistant" if message["role"] == "assistant" else "👤 You"
#         with st.chat_message(message["role"]):
#             if st.session_state.show_timestamps:
#                 st.caption(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#             st.write(f"{message['content']}")


# if __name__ == "__main__":
#     main()

from datetime import datetime
import streamlit as st
import openai
from openai import OpenAI
import time
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Initialize session state variables
if 'current_assistant_id' not in st.session_state:
    st.session_state.current_assistant_id = DEFAULT_ASSISTANT_ID
if 'thread_id' not in st.session_state:
    st.session_state.thread_id = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'show_timestamps' not in st.session_state:
    st.session_state.show_timestamps = False
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.7
if 'chatbot_title' not in st.session_state:
    st.session_state.chatbot_title = "Rodney ChatBot"

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def create_new_thread():
    """Create a new thread and reset messages"""
    st.session_state.thread_id = client.beta.threads.create().id
    st.session_state.messages = []
    st.session_state.message_count = 0


def process_message(thread_id, user_message):
    """Process a user message and get the assistant's response"""
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=st.session_state.current_assistant_id,
        temperature=st.session_state.temperature
    )

    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run_status.status == 'completed':
            break
        elif run_status.status == 'failed':
            st.error("Assistant response failed. Please try again.")
            return None
        time.sleep(1)

    messages = client.beta.threads.messages.list(thread_id=thread_id)
    return messages.data


def export_chat():
    """Export chat history as text"""
    if not st.session_state.messages:
        return "No messages to export."

    export_text = "Chat History\n\n"
    for msg in st.session_state.messages:
        role = "Assistant" if msg["role"] == "assistant" else "User"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        export_text += f"{timestamp} - {role}:\n{msg['content']}\n\n"
    return export_text


def main():
    if st.session_state.dark_mode:
        st.markdown("""
            <style>
            .stApp {
                background-color: #262626;
                color: #FFFFFF;
            }
            </style>
            """, unsafe_allow_html=True)

    st.title(st.session_state.chatbot_title)

    with st.sidebar:
        st.subheader("Chatbot Settings")
        chatbot_name = st.text_input(
            "Chatbot Title", value=st.session_state.chatbot_title)
        if st.button("Update Title"):
            st.session_state.chatbot_title = chatbot_name
            st.rerun()

        st.subheader("Assistant Configuration")
        new_assistant_id = st.text_input(
            "Assistant ID", value=st.session_state.current_assistant_id)
        if st.button("Update Assistant ID"):
            st.session_state.current_assistant_id = new_assistant_id
            create_new_thread()
            st.success("Assistant ID updated! New chat thread created.")
            st.rerun()

        st.caption(
            f"Current Assistant ID: {st.session_state.current_assistant_id}")

    if st.session_state.thread_id is None:
        create_new_thread()

    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.message_count += 1
        messages = process_message(st.session_state.thread_id, prompt)
        if messages:
            new_messages = [
                {"role": msg.role, "content": msg.content[0].text.value}
                for msg in reversed(messages)
            ]
            st.session_state.messages = new_messages
            st.rerun()

    for message in st.session_state.messages:
        role = "🤖 Assistant" if message["role"] == "assistant" else "👤 You"
        with st.chat_message(message["role"]):
            if st.session_state.show_timestamps:
                st.caption(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            st.write(f"{message['content']}")


if __name__ == "__main__":
    main()
