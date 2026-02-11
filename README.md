# Talk-to-Syllabus RAG System

An AI-powered conversational interface that allows students to upload course syllabi (PDF) and ask natural language questions.

## Setup

1.  **Clone the repository** (if not already local).
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure Secrets**:
    - Update `.streamlit/secrets.toml` with your `PINECONE_API_KEY` and `GROQ_API_KEY`.
    - Ensure you have a Pinecone index named `course-syllabus` (dimension 384, metric cosine). The app attempts to create it if it doesn't exist, but you need permissions.

## Usage

1.  Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```
2.  **Upload a Syllabus**: Use the sidebar to upload a PDF file.
3.  **Process PDF**: Click the "Process PDF" button to extract text, generate embeddings, and store them in Pinecone.
4.  **Ask Questions**: Use the chat interface to ask questions about the syllabus content.

## Architecture

-   **Frontend**: Streamlit
-   **Backend**: Python
-   **PDF Parsing**: PyPDF2
-   **Chunking**: LangChain RecursiveCharacterTextSplitter
-   **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
-   **Vector DB**: Pinecone
-   **LLM**: Groq (Llama 3.1 70B)
