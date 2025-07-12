from fastapi import FastAPI
from routes import index, user, ai
from core.init_database import create_tables

app = FastAPI()

@app.on_event("startup")
def startup_event():
    create_tables()
    print("데이터베이스 테이블 초기화 완료")

app.include_router(index.router) # / -> index router
app.include_router(user.router, prefix="/user") # /user -> user router
app.include_router(ai.router, prefix="/ai") # /ai -> ai router