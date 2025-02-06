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

# # Replace with your actual assistant ID
# ASSISTANT_ID = os.getenv("ASSISTANT_ID")


# # Initialize OpenAI client

# client = OpenAI(api_key=OPENAI_API_KEY)


# # Initialize session state variables if they don't exist

# if 'thread_id' not in st.session_state:

#     st.session_state.thread_id = None


# if 'messages' not in st.session_state:

#     st.session_state.messages = []


# def create_new_thread():
#     """Create a new thread and reset messages"""

#     st.session_state.thread_id = client.beta.threads.create().id

#     st.session_state.messages = []


# def process_message(thread_id, user_message):
#     """Process a user message and get the assistant's response"""

#     # Add user message to thread

#     client.beta.threads.messages.create(

#         thread_id=thread_id,

#         role="user",

#         content=user_message

#     )

#     # Run the assistant

#     run = client.beta.threads.runs.create(

#         thread_id=thread_id,

#         assistant_id=ASSISTANT_ID

#     )

#     # Wait for the assistant to complete its response

#     while True:

#         run_status = client.beta.threads.runs.retrieve(

#             thread_id=thread_id,

#             run_id=run.id

#         )

#         if run_status.status == 'completed':

#             break

#         time.sleep(1)

#     # Get all messages

#     messages = client.beta.threads.messages.list(thread_id=thread_id)

#     return messages.data


# def main():

#     st.title("OpenAI Assistant Chat")

#     # Add New Chat button in the sidebar

#     if st.sidebar.button("New Chat"):

#         create_new_thread()

#         st.rerun()

#     # Create initial thread if none exists

#     if st.session_state.thread_id is None:

#         create_new_thread()

#     # Display chat messages

#     for message in st.session_state.messages:

#         role = "🤖 Assistant" if message["role"] == "assistant" else "👤 You"

#         with st.chat_message(message["role"]):

#             st.write(f"{message['content']}")

#     # Chat input

#     if prompt := st.chat_input("Type your message here..."):

#         # Add user message to display

#         st.session_state.messages.append({"role": "user", "content": prompt})

#         # Get assistant response

#         messages = process_message(st.session_state.thread_id, prompt)

#         # Update messages in session state

#         st.session_state.messages = [

#             {"role": msg.role, "content": msg.content[0].text.value}

#             for msg in messages

#         ]

#         st.rerun()


# if __name__ == "__main__":

#     main()



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

# # Initialize OpenAI client
# client = OpenAI(api_key=OPENAI_API_KEY)


# def create_new_thread():
#     """Create a new thread and reset messages"""
#     st.session_state.thread_id = client.beta.threads.create().id
#     st.session_state.messages = []
#     st.session_state.message_count = 0


# def process_message(thread_id, user_message):
#     """Process a user message and get the assistant's response"""
#     # Add user message to thread
#     client.beta.threads.messages.create(
#         thread_id=thread_id,
#         role="user",
#         content=user_message
#     )

#     # Run the assistant with current settings
#     run = client.beta.threads.runs.create(
#         thread_id=thread_id,
#         assistant_id=st.session_state.current_assistant_id,
#         temperature=st.session_state.temperature
#     )

#     # Wait for the assistant to complete its response
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

#     # Get all messages
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
#     # Apply dark mode if enabled
#     if st.session_state.dark_mode:
#         st.markdown("""
#             <style>
#             .stApp {
#                 background-color: #262626;
#                 color: #FFFFFF;
#             }
#             </style>
#             """, unsafe_allow_html=True)

#     st.title("OpenAI Assistant Chat")

#     # Sidebar content
#     with st.sidebar:
#         st.header("Settings")

#         # Assistant ID settings
#         st.subheader("Assistant Configuration")
#         new_assistant_id = st.text_input(
#             "Assistant ID",
#             value=st.session_state.current_assistant_id,
#             placeholder="Enter Assistant ID..."
#         )

#         if st.button("Update Assistant ID"):
#             st.session_state.current_assistant_id = new_assistant_id
#             create_new_thread()
#             st.success("Assistant ID updated! New chat thread created.")
#             st.rerun()

#         st.caption(
#             f"Current Assistant ID: {st.session_state.current_assistant_id}")

#         # Model behavior settings
#         st.subheader("Model Settings")
#         st.session_state.temperature = st.slider(
#             "Temperature",
#             min_value=0.0,
#             max_value=1.0,
#             value=st.session_state.temperature,
#             help="Higher values make the output more random, lower values make it more focused and deterministic."
#         )

#         # Display settings
#         st.subheader("Display Settings")
#         st.session_state.show_timestamps = st.checkbox(
#             "Show Timestamps",
#             value=st.session_state.show_timestamps,
#             help="Display timestamp for each message"
#         )

#         # Chat management
#         st.subheader("Chat Management")
#         if st.button("New Chat"):
#             create_new_thread()
#             st.rerun()

#         if st.button("Export Chat"):
#             chat_export = export_chat()
#             st.download_button(
#                 label="Download Chat History",
#                 data=chat_export,
#                 file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
#                 mime="text/plain"
#             )

#         # Chat statistics
#         st.subheader("Statistics")
#         st.caption(
#             f"Messages in current chat: {st.session_state.message_count}")
#         if st.session_state.messages:
#             last_message_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             st.caption(f"Last message: {last_message_time}")

#     # Create initial thread if none exists
#     if st.session_state.thread_id is None:
#         create_new_thread()

#     # Chat input and message processing
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

#     # Display chat messages
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

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def create_new_thread():
    """Create a new thread and reset messages"""
    st.session_state.thread_id = client.beta.threads.create().id
    st.session_state.messages = []
    st.session_state.message_count = 0


def process_message(thread_id, user_message):
    """Process a user message and get the assistant's response"""
    # Add user message to thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message
    )

    # Run the assistant with current settings
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=st.session_state.current_assistant_id,
        temperature=st.session_state.temperature
    )

    # Wait for the assistant to complete its response
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

    # Get all messages
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
    # Apply dark mode if enabled
    if st.session_state.dark_mode:
        st.markdown("""
            <style>
            .stApp {
                background-color: #262626;
                color: #FFFFFF;
            }
            </style>
            """, unsafe_allow_html=True)

    st.title("Rodney ChatBot")

    # Sidebar content
    with st.sidebar:
        # Welcome section with styled title and description
        st.markdown("""
            <div style='text-align: center; padding: 1rem 0;'>
                <h1 style='font-size: 2rem; margin-bottom: 0.5rem;'>🤖 OpenAI Assistant Hub</h1>
                <p style='font-size: 1.1rem; color: #666; margin-bottom: 1rem;'>Your Gateway to OpenAI Assistants</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            Welcome to OpenAI Assistant Hub, where you can interact with any OpenAI Assistant! Simply:
            1. Enter your Assistant ID below
            2. Click "Update Assistant ID"
            3. Start chatting with your chosen assistant!
            
        """)

        st.divider()

        st.header("Settings")

        # Assistant ID settings
        st.subheader("Assistant Configuration")
        new_assistant_id = st.text_input(
            "Assistant ID",
            value=st.session_state.current_assistant_id,
            placeholder="Enter Assistant ID..."
        )

        if st.button("Update Assistant ID"):
            st.session_state.current_assistant_id = new_assistant_id
            create_new_thread()
            st.success("Assistant ID updated! New chat thread created.")
            st.rerun()

        st.caption(
            f"Current Assistant ID: {st.session_state.current_assistant_id}")

        # Model behavior settings
        st.subheader("Model Settings")
        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            help="Higher values make the output more random, lower values make it more focused and deterministic."
        )

        # Display settings
        st.subheader("Display Settings")
        st.session_state.show_timestamps = st.checkbox(
            "Show Timestamps",
            value=st.session_state.show_timestamps,
            help="Display timestamp for each message"
        )

        # Chat management
        st.subheader("Chat Management")
        if st.button("New Chat"):
            create_new_thread()
            st.rerun()

        if st.button("Export Chat"):
            chat_export = export_chat()
            st.download_button(
                label="Download Chat History",
                data=chat_export,
                file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

        # Chat statistics
        st.subheader("Statistics")
        st.caption(
            f"Messages in current chat: {st.session_state.message_count}")
        if st.session_state.messages:
            last_message_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.caption(f"Last message: {last_message_time}")

        # Footer with version and credits
        st.sidebar.markdown("""
            ---
            <div style='text-align: center; color: #666; padding: 1rem 0;'>
                <p>v1.0.1 | Powered by OpenAI</p>
                <p style='font-size: 0.8rem;'></p>
            </div>
        """, unsafe_allow_html=True)

    # Create initial thread if none exists
    if st.session_state.thread_id is None:
        create_new_thread()

    # Chat input and message processing
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

    # Display chat messages
    for message in st.session_state.messages:
        role = "🤖 Assistant" if message["role"] == "assistant" else "👤 You"
        with st.chat_message(message["role"]):
            if st.session_state.show_timestamps:
                st.caption(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            st.write(f"{message['content']}")


if __name__ == "__main__":
    main()
