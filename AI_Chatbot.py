from langchain_openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain_community.tools import DuckDuckGoSearchRun
import streamlit as st
api_key = ""

st.set_page_config(page_title="Usama Nawaz Chabot", page_icon="")
st.title("Usama Nawaz Chatbot")



if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant", "content":"How can I help you?"}]
    print(st.session_state.messages)


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

  
if prompt := st.chat_input(placeholder="Will Donald Trump be indicted?"):
    st.session_state.messages.append({"role":"assistant", "content":prompt})
    st.chat_message("user").write(prompt)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo" ,temperature = 0, streaming = True, api_key=api_key)
    tools = [DuckDuckGoSearchRun(name="Search")]

    agent = initialize_agent(tools = tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,handle_parsing_error=True)



    with st.chat_message("assistant"):
        st.write("Generating...")
        st_callback = StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
        response = agent.run(st.session_state.messages, callbacks=[st_callback])
        st.session_state.messages.append({"role":"assistant", "content":response})
        st.write(response)
