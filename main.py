from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import timedelta
from database import database
from models import UserRegister, UserLogin, Token, Task
from auth import authenticate_user, create_access_token, register_user, get_current_user
from routers import tasks
from config import settings

# Tạo FastAPI app
app = FastAPI(
    title="Task Manager API",
    description="API quản lý danh sách công việc với JWT authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include task routes
app.include_router(tasks.router)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Trang chủ - serve frontend"""
    return FileResponse("static/index.html")

@app.post("/register", response_model=dict)
async def register(user: UserRegister):
    """Đăng ký người dùng mới"""
    return register_user(user.username, user.password)

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Đăng nhập và nhận JWT token"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không đúng",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Tạo access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api")
async def api_info():
    """Thông tin API"""
    return {
        "message": "Task Manager API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/me", response_model=dict)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Lấy thông tin user hiện tại"""
    return {
        "id": current_user["id"],
        "username": current_user["username"],
        "created_at": current_user["created_at"]
    }

# Khởi tạo database khi app khởi động
@app.on_event("startup")
async def startup_event():
    """Khởi tạo database khi app khởi động"""
    # Database đã được khởi tạo trong Database class
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 