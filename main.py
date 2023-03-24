import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chat_models import ChatOpenAI
from collections import defaultdict


if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'input' not in st.session_state:
    st.session_state['input'] = ''
if 'stored_session' not in st.session_state:
    st.session_state['stored_session'] =[]

def get_text():
    user_input = st.text_input(
        "User: ", key="input", placeholder="Say something to Davic...")
    return user_input

st.title('Chatbot with GPT-3.5 Turbo')
api_key = st.sidebar.text_input('API Key', type='password')

if api_key:
    llm = ChatOpenAI(
        temperature=0.7,
        openai_api_key=api_key,
        model_name='gpt-3.5-turbo'
    )
    
    # CONV MEMORY
    if 'entity_memory' not in st.session_state:
        st.session_state.entity_memory = ConversationEntityMemory(llm = llm, k=10)
        
    Conversation = ConversationChain(
        llm = llm,
        prompt = ENTITY_MEMORY_CONVERSATION_TEMPLATE,
        memory=st.session_state.entity_memory,
    )
    
else:
    st.error('Not found API Key')
    
user_input = get_text()
if user_input:
    
    output = Conversation.run(input=user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

with st.expander('Conversation'):
    for i in range(len(st.session_state['generated'])-1 , -1, -1):
        st.success(st.session_state['generated'][i], icon='🤖')
        st.info(st.session_state['past'][i], icon='🧐')