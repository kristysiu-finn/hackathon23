import requests
import openai
import re
import os
import logging
from typing import Optional
from utils import text_to_docs, embed_docs, search_docs, get_answer
from bs4 import BeautifulSoup
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


load_dotenv()
logger = logging.getLogger('main')
logging.basicConfig(level=logging.INFO)


class Input(BaseModel):
    url: Optional[str] = None
    query: str
    

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/answer/")
async def get_embedding_answer(input: Input):
    url = input.url
    response = requests.get(url) 
    soup = BeautifulSoup(response.content, 'html.parser') 
        
    doc = soup.get_text()

    query = input.query

    text = text_to_docs(doc)

    logger.info('Indexing document... This may take a while⏳')
    index = embed_docs(text)

    logger.info('Searching docs')
    sources = search_docs(index, query)

    logger.info('Getting answer')
    answer = get_answer(sources, query)

    logger.info(f"Answer: {answer}")
    return answer["output_text"].split("SOURCES: ")[0]


@app.post("/answer_gpt/")
async def get_gpt_answer(input: Input):
    url = input.url
    doc = ''
    if url:
        response = requests.get(url) 
        soup = BeautifulSoup(response.content, 'html.parser') 
            
        doc = soup.get_text()
        doc = re.sub('\n', ' ', doc)

    query = input.query

    prompt = f"""
        {query}

        {doc}
    """
    messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{prompt}"},
    ]

    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        #model='gpt-4',
        messages=messages,
        temperature=0.8,    
    )

    return completion.choices[0].message.content
