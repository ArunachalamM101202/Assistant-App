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

# Replace with your actual assistant ID
ASSISTANT_ID = os.getenv("ASSISTANT_ID")


# Initialize OpenAI client

client = OpenAI(api_key=OPENAI_API_KEY)


# Initialize session state variables if they don't exist

if 'thread_id' not in st.session_state:

    st.session_state.thread_id = None


if 'messages' not in st.session_state:

    st.session_state.messages = []


def create_new_thread():
    """Create a new thread and reset messages"""

    st.session_state.thread_id = client.beta.threads.create().id

    st.session_state.messages = []


def process_message(thread_id, user_message):
    """Process a user message and get the assistant's response"""

    # Add user message to thread

    client.beta.threads.messages.create(

        thread_id=thread_id,

        role="user",

        content=user_message

    )

    # Run the assistant

    run = client.beta.threads.runs.create(

        thread_id=thread_id,

        assistant_id=ASSISTANT_ID

    )

    # Wait for the assistant to complete its response

    while True:

        run_status = client.beta.threads.runs.retrieve(

            thread_id=thread_id,

            run_id=run.id

        )

        if run_status.status == 'completed':

            break

        time.sleep(1)

    # Get all messages

    messages = client.beta.threads.messages.list(thread_id=thread_id)

    return messages.data


def main():

    st.title("OpenAI Assistant Chat")

    # Add New Chat button in the sidebar

    if st.sidebar.button("New Chat"):

        create_new_thread()

        st.rerun()

    # Create initial thread if none exists

    if st.session_state.thread_id is None:

        create_new_thread()

    # Display chat messages

    for message in st.session_state.messages:

        role = "🤖 Assistant" if message["role"] == "assistant" else "👤 You"

        with st.chat_message(message["role"]):

            st.write(f"{message['content']}")

    # Chat input

    if prompt := st.chat_input("Type your message here..."):

        # Add user message to display

        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get assistant response

        messages = process_message(st.session_state.thread_id, prompt)

        # Update messages in session state

        st.session_state.messages = [

            {"role": msg.role, "content": msg.content[0].text.value}

            for msg in messages

        ]

        st.rerun()


if __name__ == "__main__":

    main()
