from pydantic import BaseModel, EmailStr, Field

# 요청: 회원가입 요청용
class UserRegister(BaseModel):
    userid: str = Field(..., max_length=50)
    password: str = Field(..., min_length=4)
    name: str
    email: EmailStr

# 요청: 로그인인 요청용
class UserLogin(BaseModel):
    userid: str
    password: str

# 내부 처리용 (예: DB 저장 전 모델 생성용)
class UserInDB(UserRegister):
    hashed_password: str

# 응답: 클라이언트에게 보낼 사용자 정보
class UserResponse(BaseModel):
    id: int
    userid: str
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
