import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter

def parse_pdf(file):
    """
    Extracts text from a PDF file using pdfplumber.
    """
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text

def chunk_text(text, chunk_size=500, chunk_overlap=50):
    """
    Splits text into chunks using LangChain's RecursiveCharacterTextSplitter.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_text(text)
    return chunks
