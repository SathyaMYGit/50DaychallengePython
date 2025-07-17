import streamlit as st
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

st.set_page_config(page_title="Local Sheet QA", layout="wide")
st.title("📋 Ask Questions from Your Local Excel/CSV File")

# 🔐 OpenAI API Key
openai_api_key = st.text_input("🔑 Enter your OpenAI API Key:", type="password")

# 📤 Upload your sheet file
sheet_file = st.file_uploader("📥 Upload your Excel or CSV file", type=["xlsx", "csv"])

if sheet_file and openai_api_key:
    # Step 1: Load sheet data into pandas
    if sheet_file.name.endswith(".csv"):
        df = pd.read_csv(sheet_file)
    else:
        df = pd.read_excel(sheet_file)

    st.success("✅ File loaded successfully!")
    st.dataframe(df.head())

    # Step 2: Convert rows to text
    text_data = df.astype(str).apply(lambda row: " | ".join(row), axis=1).tolist()
    joined_text = "\n".join(text_data)

    # Step 3: Split text
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(joined_text)

    # Step 4: Embed using OpenAI
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)

    # Step 5: QA chain setup
    llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )

    # Step 6: Ask your question
    query = st.text_input("❓ Ask your question about the sheet:")
    if query:
        result = qa_chain({"query": query})
        st.subheader("📌 Answer:")
        st.write(result["result"])

        with st.expander("📚 Source Data"):
            for doc in result["source_documents"]:
                st.markdown(doc.page_content)
else:
    st.info("Please upload a sheet and enter your OpenAI API key to get started.")
