import os
import time
import shutil
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from dotenv import load_dotenv

# ────────────── CONFIG ────────────── #
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
assert OPENAI_API_KEY, "🔑 Set your OPENAI_API_KEY in .env"

DATA_DIR = "data"
CHROMA_DIR = "chroma_db"
WHOOSH_DIR = "whoosh_index"
BASE_URL = "https://kcppromoters.com/"

# ───────── Web Scraping ───────── #
def get_selenium_driver():
    chrome_opts = Options()
    chrome_opts.add_argument("--headless")
    chrome_opts.add_argument("--disable-gpu")
    chrome_opts.add_argument("--no-sandbox")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_opts)

def scrape_site():
    os.makedirs(DATA_DIR, exist_ok=True)
    driver = get_selenium_driver()
    driver.get(BASE_URL)
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    with open(os.path.join(DATA_DIR, "home.txt"), "w", encoding="utf-8") as f:
        f.write(text)
    driver.quit()

# ───────── Preparation ───────── #
def load_and_chunk():
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = []
    for fn in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, fn)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        docs.extend(splitter.create_documents([content]))
    return docs

def safe_delete(path):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except PermissionError:
            backup = f"{path}_backup_{int(time.time())}"
            os.rename(path, backup)
            print(f"⚠️ Renamed old {path} to {backup}")

# ───── Vector DB & Keyword Index ───── #
def build_sources(docs):
    safe_delete(CHROMA_DIR)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectordb = Chroma.from_documents(docs, embedding=embeddings, persist_directory=CHROMA_DIR)
    vectordb.persist()

    safe_delete(WHOOSH_DIR)
    schema = Schema(content=TEXT(stored=True), path=ID(stored=True))
    ix = create_in(WHOOSH_DIR, schema)
    writer = ix.writer()
    for i, d in enumerate(docs):
        writer.add_document(content=d.page_content, path=str(i))
    writer.commit()
    return vectordb, ix

# ─── Corrective RAG Function ───── #
def run_corrective_rag(q, vectordb, ix):
    llm = ChatOpenAI(temperature=0)
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    res = qa.invoke({"query": q})
    answer = res["result"]

    if len(answer.strip()) < 30 or "I don't know" in answer.lower():
        print("↩️ Falling back to keyword retrieval")
        searcher = open_dir(WHOOSH_DIR).searcher()
        qp = QueryParser("content", schema=searcher.schema)
        hits = searcher.search(qp.parse(q), limit=3)
        context = "\n".join(hit["content"] for hit in hits)
        prompt = f"Answer using this content:\n{context}\n\nQ: {q}"
        answer = llm.invoke(prompt).content

    return answer

# ─────── Main Flow ─────── #
if __name__ == "__main__":
    print("🕷 Scraping website...")
    scrape_site()

    print("📄 Loading and chunking...")
    docs = load_and_chunk()

    print("⚙️ Building vector & keyword indexes...")
    vectordb, ix = build_sources(docs)

    print("✅ Ready! Ask your questions now.")
    while True:
        q = input("\n🧠 Your question (or 'exit'): ")
        if q.strip().lower() == "exit":
            break
        reply = run_corrective_rag(q, vectordb, ix)
        print("\n💬 Answer:\n", reply)
