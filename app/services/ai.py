import os
from openai import OpenAI
from google import genai
import requests
import json

from dotenv import load_dotenv

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