from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse

from utils.templates import templates

from schemas.chatbot import ChatQuestion, ChatAnswer
from services.ai import (
    generate_gpt_chat_response, 
    generate_gemini_chat_response,
    generate_local_gemma_chat_response,
)

router = APIRouter()

@router.get("/image", response_class=HTMLResponse)
async def show_image_ai(request: Request):
    return templates.TemplateResponse("image_ai.html", {"request": request})

@router.get("/chatbot", response_class=HTMLResponse)
async def show_chatbot(request: Request):
    return templates.TemplateResponse("chatbot_ai.html", {"request": request})
    
@router.post("/chatbot", response_class=HTMLResponse)
async def process_chatbot(
    request: Request, 
    user_input: str = Form(...),
    model: str = Form(...)
    ):
    question = ChatQuestion(user_input=user_input)
    messages = [{"role": "user", "content": question.user_input}]
    
    if model == "gpt":
        response = generate_gpt_chat_response(messages)
    elif model == "gemini":
        response = generate_gemini_chat_response(messages)
    elif model == "local_gemma":
        response = generate_local_gemma_chat_response(messages)
    else:
        response = "Invalid model selected."
    
    answer = ChatAnswer(answer=response)
    
    return templates.TemplateResponse("chatbot_ai.html", {
        "request": request, 
	    "user_input": question.user_input, 
	    "response": answer.answer,
        "selected_model": model
	})