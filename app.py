import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from htmlTemplates import css, user_template, bot_template
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import importlib.util
import os





def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(separator="\n",
                                        chunk_size=1000,
                                        chunk_overlap=200,
                                        length_function=len)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_texts(texts=text_chunks, embedding=embeddings, persist_directory="embeddings")
    return vectorstore

def get_conversation_chain(vector_store, temperature):
    llm = ChatOpenAI(temperature=temperature)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vector_store.as_retriever(), memory=memory)
    return conversation_chain

def handle_user_input(user_question):
    response = st.session_state.conversation({'question': user_question})
    
    st.session_state.chat_history = response["chat_history"]
    
    if user_question.lower() in ["ciao", "hi", "salut", "hallo"]:
        st.write(user_template.replace("{{MSG}}", user_question), unsafe_allow_html=True)
        st.write(bot_template.replace("{{MSG}}", "Ciao sono Clizia l'amica della giustizia! Sono un'esperta di legge e il mio scopo è garantire equità e abbattere le discriminazioni. Come posso esserti d'aiuto?"), unsafe_allow_html=True)
    else:
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def popola_database():
    pdf_folder_path = './data'
    pdf_files = [os.path.join(pdf_folder_path, f) for f in os.listdir(pdf_folder_path) if f.endswith('.pdf')]
    pdf_text = get_pdf_text(pdf_files)
    text_chunks = get_text_chunks(pdf_text)   
    vectorstore = get_vector_store(text_chunks)
    return vectorstore

def reset_conversation():   
    st.session_state.conversation = get_conversation_chain(st.session_state.vector_store, st.session_state.temperature)
    st.session_state.chat_history = []

def load_page(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.run()

def info():
    st.title("Se hai bisogno di assistenza umana,ecco alcuni contatti:")
    st.write("ufficio legale: ufficio_legale@gmail.com\:judge:")
    st.write("ufficio amministrativo: ufficio_amministrativo@gmail.com\:mortar_board:")
    st.write("Numero Verde:800 400 5050\:phone:")
    
def main():
    load_dotenv()
    
    background_image= '''
    <style>
    body {
    background-image: url("https://i.ibb.co/zhYsd9T/immagine-1.png");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    }
    .stApp {
        background-color: rgba(249, 198, 147, 0.8); 
    }
    .st-emotion-cache-eeyzq7{
        background-color: transparent;
    }
    </style>
    '''
    #st.markdown(page_bg_img, unsafe_allow_html=True)
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">
    <style>
    .netflix-font {
        font-family: 'Bebas Neue', sans-serif;
        color: #4A2713;
        font-size: 48px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(background_image, unsafe_allow_html=True)
    st.markdown('<h1 class="netflix-font">Clizia-la chat della Giustizia </h1>', unsafe_allow_html=True)

            
    components.html("""
    <style>
    div[pseudo="placeholder"] input::placeholder {
        color:#4A2713;
        background-color: rgba(249, 198, 147, 0.8);
    }
    </style>
    """, height=0)
    
    st.write(css, unsafe_allow_html=True)
    
    if "vector_store" not in st.session_state:
        with st.spinner("Sto Popolando il Database..."):
            st.session_state.vector_store = popola_database()
            st.success("Database Popolato!")
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = get_conversation_chain(st.session_state.vector_store, 0.7)
        
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    st.session_state.temperature = st.slider('Scegli la temperatura per le risposte del modello\:thermometer:', 0.0, 1.0, 0.5)
    
    
    
    user_question = st.chat_input("Fammi una domanda")
    
    if user_question:
        handle_user_input(user_question)
        
        
    with st.sidebar:
        selected = option_menu("Menu", ["Esplora", "Nuova chat", "Aiuto"], icons=['compass', 'plus','question'], menu_icon=":scales:", default_index=0)
        if selected == "Nuova chat":
            st.button('Reset Chat', on_click=reset_conversation)
        if selected == "Aiuto":
            st.title("Se hai bisogno di assistenza umana, ecco alcuni contatti:")
            st.write("ufficio legale:")
            st.write("ufficio_legale@gmail.com\:judge:")
            st.write("ufficio amministrativo: ufficio_amministrativo@gmail.com\:memo:")
            st.write("Numero Verde: 800 400 5050\:phone:")
        if selected == "Esplora":
            load_page("explorer", "explorer.py")

if __name__ == '__main__':
    main()