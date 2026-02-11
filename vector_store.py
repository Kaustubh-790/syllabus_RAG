import os
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import streamlit as st

# Initialize Pinecone
def initialize_pinecone():
    api_key = st.secrets["PINECONE_API_KEY"]
    pc = Pinecone(api_key=api_key)
    index_name = "course-syllabus"
    
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384, 
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            ) 
        )
    return pc.Index(index_name)

# Initialize Embedding Model
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(chunks):
    """
    Generates embeddings for a list of text chunks.
    """
    embeddings = model.encode(chunks)
    return embeddings.tolist()

def upsert_vectors(index, chunks, embeddings):
    """
    Upserts vectors to Pinecone.
    """
    vectors = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        vectors.append({
            "id": str(i),
            "values": embedding,
            "metadata": {"text": chunk}
        })
    
    # Upsert in batches of 100
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i+batch_size]
        index.upsert(vectors=batch)

def query_vectors(index, query, top_k=5):
    """
    Queries Pinecone for similar chunks.
    """
    query_embedding = model.encode([query]).tolist()[0]
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    return results
