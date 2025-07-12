from pydantic import BaseModel

# 요청
class ChatQuestion(BaseModel):
    user_input: str

# 응답
class ChatAnswer(BaseModel):
    answer: str