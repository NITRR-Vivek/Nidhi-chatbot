from pinecone import Pinecone
from pinecone import  PodSpec
import streamlit as st
import google.generativeai as genai 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
PINE_API_KEY = os.environ.get("PINE_API_KEY")
PINECONE_API_ENV = os.environ.get("PINE_API_ENV")
INDEX_NAME = os.environ.get("PINE_INDEX")

if not all([GOOGLE_API_KEY, PINE_API_KEY, PINECONE_API_ENV, INDEX_NAME]):
    try:
        GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
        PINE_API_KEY = st.secrets["PINE_API_KEY"]
        PINECONE_API_ENV = st.secrets["PINE_API_ENV"]
        INDEX_NAME = st.secrets["PINE_INDEX"]
    except FileNotFoundError as e:
        st.warning("Secrets file not found. Using environment variables.")
    except Exception as e:
        st.error("Error loading secrets. Please make sure secrets are properly configured.")
        st.stop()
embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001",google_api_key=GOOGLE_API_KEY)

spec = PodSpec(environment=PINECONE_API_ENV)
pc = Pinecone(
    api_key=PINE_API_KEY
)

def chat(input_query):
  model = genai.GenerativeModel('gemini-pro')
  query = input_query
  query_vector = embeddings.embed_query(query)
  index = pc.Index(INDEX_NAME)
  vectors = index.query(
    vector = query_vector,
    top_k = 2,
    include_values = False,
    include_metadata = True
  )

  context = ""
  for i, match in enumerate(vectors['matches'], start=1):
    context += f"{i}. {match['metadata']['text']}\n"

  prompt_template =f"""
    You are Nidhi, an AI chatbot made by NITRR MakerSpace to help the students of NIT Raipur with their queries. Please use the following information to answer the user's question.
    If the user greets and congratulates, you should also greets and say thanks in the same way and if user asks the question then you should reply.
    If you cannot answer the question using the given information just reply 'I don't know',
    don't try to make up an answer.

  Context: {context}\n
  User query: {query}

  Only return the helpful answer and nothing else.
  Helpful answer:
  """

  response = model.generate_content(prompt_template)
  return response

def custom_chat():
 
 input_text = st.text_input("Enter your Question: ")
 if input_text:
    answer = chat(input_text)
    st.write(f"User : {input_text} ")
    try:
      st.write("Bot: " + answer.text)
    except ValueError:
       st.write(f"Bot: Could not answer this question due to following reason.\n,{answer.prompt_feedback.safety_ratings[0]}")