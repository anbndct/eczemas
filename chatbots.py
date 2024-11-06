import streamlit as st
import openai

st.title("Eczema Chatbot✨")

# Instantiate the OpenAI client
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history if not already in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
prompt = st.chat_input("What is up?")
if prompt:
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response from assistant
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Construct prompt from chat history for latest API compatibility
        history_prompt = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages]) + "\nassistant:"

        # Use the `client.completions.create` method
        response = client.completions.create(
            model=st.session_state["openai_model"],
            prompt=history_prompt,
            max_tokens=150,
            stream=True
        )

        # Process and display the streamed response
        for completion in response:
            full_response += completion.choices[0].message.content.strip()
            message_placeholder.markdown(full_response + "▌")

        # Display the full response and update history
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
