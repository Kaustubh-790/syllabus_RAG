import os
from groq import Groq
import streamlit as st

def get_groq_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

def get_answer(query, context, prompts):
    """
    Generates an answer using Groq API.
    """
    client = get_groq_client()
    
    system_prompt = prompts.RAG_SYSTEM_PROMPT.format(context=context)
    
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        temperature=0.0,
        max_tokens=1024,
    )
    
    return completion.choices[0].message.content
