import os
from openai import OpenAI
from google import genai
import requests
import json

from dotenv import load_dotenv

import tempfile
from fastapi import UploadFile

from utils.embedder import embed_text, embed_pdf_to_vectors
from utils.file_loader import load_pdf
from models.vector import Vector
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_gpt_chat_response(messages: list[dict]) -> str:
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error occurred: {str(e)}"

def generate_gemini_chat_response(messages: list[dict]) -> str:
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages[0]['content'],
        )
        return response.text
    except Exception as e:
        return f"Error occurred: {str(e)}"

def generate_local_gemma_chat_response(messages: list[dict]) -> str:
    try:
        user_input = messages[0]["content"]
        url = "http://ollama:11434/api/chat"  # Ollama 컨테이너 내부 서비스 주소
        #url = "http://192.168.0.19:11434/api/chat" 

        payload = {
            "model": "gemma3:4b",  # Ollama에 설치된 모델 이름
            "messages": [{"role": "user", "content": user_input}],
            "temperature": 0.7,
            "stream": False  # 스트리밍을 사용하지 않음
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        content = data.get("message", {}).get("content", "")
        return content.strip()

    except Exception as e:
        return f"Error occurred (Local): {str(e)}"

async def process_document_and_store_vectors(db: Session, upload_file: UploadFile) -> str:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            contents = await upload_file.read()
            tmp.write(contents)
            tmp_path = tmp.name

        # 문단별 텍스트와 벡터 리스트 추출
        texts, vectors = embed_pdf_to_vectors(tmp_path)
        print(f"[DEBUG] 문단 수: {len(texts)}")
        
        for idx, (text, vector) in enumerate(zip(texts, vectors)):
            print(f"[DEBUG] 저장 중: 문단 {idx + 1} - 길이 {len(text)}")
            doc_vector = Vector(
                content=text,
                embedding=vector
            )
            db.add(doc_vector)
            
        db.commit()
        return f"Successfully stored {len(vectors)} vectors."
    except SQLAlchemyError as e:
        db.rollback()
        return f"Database error: {str(e)}"
    except Exception as e:
        return f"Error occurred: {str(e)}"

def generate_rag_response(db: Session, query: str, model: str) -> str:
    try:
        query_vector = embed_text(query)
        vector_str = '[' + ','.join(map(str, query_vector)) + ']'
        
        result = db.execute(
            text(f"""
            SELECT id, content, embedding <=> '{vector_str}'::vector AS distance
            FROM vectors
            ORDER BY distance ASC
            LIMIT 3
            """)
        ).fetchall()

        context = "\n".join([row[1] for row in result])
        prompt = f"Answer based on the following context:\n{context}\n\nQ: {query}\nA:"
        print(f"[DEBUG] RAG Prompt: {prompt}")
        messages = [{"role": "user", "content": prompt}]

        if model == "gpt":
            return generate_gpt_chat_response(messages)
        elif model == "gemini":
            return generate_gemini_chat_response(messages)
        elif model == "local_gemma":
            return generate_local_gemma_chat_response(messages)
        else:
            return "Invalid model."

    except Exception as e:
        return f"Error occurred (RAG): {str(e)}"