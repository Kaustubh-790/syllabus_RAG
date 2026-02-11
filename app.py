import streamlit as st
import pdf_processor
import vector_store
import llm_handler
import prompts

st.set_page_config(page_title="Talk-to-Syllabus RAG", layout="wide")

st.title("Talk-to-Syllabus RAG System")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pinecone_index" not in st.session_state:
    try:
        st.session_state.pinecone_index = vector_store.initialize_pinecone()
        st.success("Connected to Pinecone!")
    except Exception as e:
        st.error(f"Failed to connect to Pinecone: {e}")

# Sidebar for File Upload
with st.sidebar:
    st.header("Upload Syllabus")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        if st.button("Process PDF"):
            with st.spinner("Processing PDF..."):
                try:
                    # 1. Parse PDF
                    text = pdf_processor.parse_pdf(uploaded_file)
                    st.info(f"Extracted {len(text)} characters.")
                    
                    # 2. Chunk Text
                    chunks = pdf_processor.chunk_text(text)
                    st.info(f"Created {len(chunks)} chunks.")
                    
                    # 3. Generate Embeddings
                    embeddings = vector_store.create_embeddings(chunks)
                    
                    # 4. Upsert to Pinecone
                    if "pinecone_index" in st.session_state:
                        vector_store.upsert_vectors(st.session_state.pinecone_index, chunks, embeddings)
                        st.success("Syllabus processed and stored in Pinecone!")
                    else:
                         st.error("Pinecone index not initialized.")

                except Exception as e:
                    st.error(f"Error processing PDF: {e}")

# Chat Interface
st.header("Ask Questions")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know about the syllabus?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # 1. Retrieve Context
                context = ""
                if "pinecone_index" in st.session_state:
                    results = vector_store.query_vectors(st.session_state.pinecone_index, prompt)
                    context = "\n".join([match.metadata["text"] for match in results.matches])
                
                # 2. Get LLM Answer
                response = llm_handler.get_answer(prompt, context, prompts)
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Show sources (optional)
                with st.expander("View Retrieved Context"):
                    st.write(context)

            except Exception as e:
                st.error(f"Error generating answer: {e}")
