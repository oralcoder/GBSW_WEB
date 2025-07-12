from fastapi import APIRouter, Request, Form, Depends, UploadFile, File
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from core.database import get_db

from utils.templates import templates

from schemas.chatbot import ChatQuestion, ChatAnswer
from services.ai import (
    generate_gpt_chat_response, 
    generate_gemini_chat_response,
    generate_local_gemma_chat_response,
    generate_rag_response,
    process_document_and_store_vectors,
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


@router.get("/rag", response_class=HTMLResponse)
async def show_rag_page(request: Request):
    return templates.TemplateResponse("rag_ai.html", {"request": request})


@router.post("/rag/upload", response_class=HTMLResponse)
async def upload_rag_document(
    request: Request,
    upload_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    result = await process_document_and_store_vectors(db=db, upload_file=upload_file)

    return templates.TemplateResponse("rag_ai.html", {
        "request": request,
        "upload_result": result,
    })


@router.post("/rag/chat", response_class=HTMLResponse)
async def rag_chat(
    request: Request,
    user_input: str = Form(...),
    model: str = Form(...),
    db: Session = Depends(get_db)
):
    response = generate_rag_response(db=db, query=user_input, model=model)

    return templates.TemplateResponse("rag_ai.html", {
        "request": request,
        "user_input": user_input,
        "response": response,
        "selected_model": model
    })