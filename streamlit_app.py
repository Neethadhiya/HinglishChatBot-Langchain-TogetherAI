import streamlit as st
from streamlit_chat import message
# from langchain.chat_models import ChatOpenAI
# from langchain_openai import ChatOpenAI
from langchain_together import ChatTogether
from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_anthropic import ChatAnthropic
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from together import Together
from dotenv import load_dotenv
load_dotenv()

import os

# os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))


# Initialize session state variables
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "Main hun aapki Ziva, poochiye mujhe kuch bhi!"}
    ]
llm = ChatTogether(
    # together_api_key="YOUR_API_KEY",
    model="meta-llama/Meta-Llama-3-8B-Instruct-Turbo",
)


conversation = ConversationChain(memory=st.session_state.buffer_memory, llm=llm)

# Create user interface
st.title("🎈🎈 हिन्glish bot 🎉🎉 ")
if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

system_message = "Please respond in Hinglish (Hindi + English) along with emojis. Keep your responses short and witty."

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            messages = [SystemMessage(content=system_message),
                        HumanMessage(content=prompt)]
            response = conversation.run(messages)
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message) # Add response to message history