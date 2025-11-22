from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
RETRIEVE_K = 6

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
)

def extract_pdf_text(path: str) -> str:
    reader = PdfReader(path)
    text = []
    for p in reader.pages:
        t = p.extract_text()
        if t:
            text.append(t)
    return "\n".join(text)

def chunk_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.split_text(text)

def create_rag_store_from_text(text: str):
    chunks = chunk_text(text)
    if not chunks:
        return {"vectorstore": None, "chunks": []}
    vectorstore = FAISS.from_texts(chunks, embeddings)
    return {"vectorstore": vectorstore, "chunks": chunks}

def create_rag_store_from_pdf(path: str):
    text = extract_pdf_text(path)
    return create_rag_store_from_text(text)

def retrieve(query: str, store, k=RETRIEVE_K):
    vs = store.get("vectorstore")
    if vs is None:
        return ""
    retriever = vs.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(query)
    return "\n".join(d.page_content for d in docs)
