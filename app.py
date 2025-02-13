from typing import List, Optional, Any
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.embeddings import HuggingFaceEmbeddings
from CustomLLM import CustomLLM

def get_pdf_text(pdf_docs: List[Any]) -> str:
    """
    Extract text content from uploaded PDF documents.
    
    Args:
        pdf_docs (List[Any]): List of uploaded PDF file objects from Streamlit
        
    Returns:
        str: Concatenated text content from all PDFs
        
    Raises:
        ValueError: If pdf_docs is empty or contains invalid files
    """
    if not pdf_docs:
        raise ValueError("No PDF documents provided")
    
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text: str) -> List[str]:
    """
    Split input text into smaller chunks for processing.
    
    Args:
        text (str): Input text to be split into chunks
        
    Returns:
        List[str]: List of text chunks
        
    Raises:
        ValueError: If input text is empty
    """
    if not text.strip():
        raise ValueError("Input text is empty")
        
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=10000,
        chunk_overlap=5000,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks: List[str]) -> FAISS:
    """
    Create a FAISS vector store from text chunks using HuggingFace embeddings.
    
    Args:
        text_chunks (List[str]): List of text chunks to be vectorized
        
    Returns:
        FAISS: Initialized FAISS vector store
        
    Raises:
        ValueError: If text_chunks is empty
    """
    if not text_chunks:
        raise ValueError("No text chunks provided")
        
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore: FAISS) -> ConversationalRetrievalChain:
    """
    Initialize a conversational chain with the given vector store.
    
    Args:
        vectorstore (FAISS): Initialized FAISS vector store
        
    Returns:
        ConversationalRetrievalChain: Configured conversation chain
    """
    llm = CustomLLM()
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question: str) -> None:
    """
    Process user input and update chat history in the Streamlit session.
    
    Args:
        user_question (str): User's input question
        
    Raises:
        RuntimeError: If conversation chain is not initialized
    """
    if not st.session_state.conversation:
        raise RuntimeError("Conversation chain not initialized")
        
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    chat_history = st.session_state.chat_history
    for i in range(len(chat_history) - 1, 0, -2):
        st.write(user_template.replace("{{MSG}}", chat_history[i-1].content), unsafe_allow_html=True)
        st.write(bot_template.replace("{{MSG}}", chat_history[i].content), unsafe_allow_html=True)

def main() -> None:
    """
    Main application function that sets up the Streamlit interface and handles the application flow.
    """
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", 
            accept_multiple_files=True,
            type=['pdf']  # Add file type restriction
        )
        if st.button("Process"):
            with st.spinner("Processing"):
                try:
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    vectorstore = get_vectorstore(text_chunks)
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                    st.success("Documents processed successfully!")
                except Exception as e:
                    st.error(f"Error processing documents: {str(e)}")

if __name__ == '__main__':
    main()
