import streamlit as st
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import os

# 🍕 Pizza knowledge base with today's offer
pizza_texts = [
    "We serve pepperoni, margherita, and veggie pizzas.",
    "Our opening hours are 10 AM to 11 PM every day.",
    "We deliver within 5 km of the shop.",
    "You can pay by cash, card, or UPI.",
    "We offer 20% discount on your first order through the app.",
    "Today's offer: Buy 1 pizza, get 2 free!"
]

VECTOR_STORE_PATH = "Pizza_FAISS_DB"

# Load or create FAISS vector store
@st.cache_resource
def load_vector_store():
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    if os.path.exists(VECTOR_STORE_PATH):
        return FAISS.load_local(VECTOR_STORE_PATH, embedding_model )
        vector_store = FAISS.from_texts(pizza_texts, embedding_model)
        vector_store.save_local(VECTOR_STORE_PATH)
        return vector_store

# UI setup
st.set_page_config(page_title="🍕 Pizza Chatbot", layout="centered")
st.title("🍕 Pizza Shop Chatbot")
st.write("Ask me anything about our pizza shop!")

# Load FAISS
vector_store = load_vector_store()

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
user_input = st.chat_input("Type your message here...")

# Handle input
if user_input:
    # Add user message to history
    st.session_state.chat_history.append(("user", user_input))

    # Search vector store
    results = vector_store.similarity_search(user_input, k=1)
    bot_reply = results[0].page_content

    # Add bot reply to history
    st.session_state.chat_history.append(("bot", bot_reply))

# Display conversation
for speaker, message in st.session_state.chat_history:
    if speaker == "user":
        st.chat_message("user").write(message)
    else:
        st.chat_message("assistant").write(message)
