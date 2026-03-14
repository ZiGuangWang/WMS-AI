from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.db.mongodb import get_perm_database
from app.core.security import create_access_token, verify_password
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login", response_model=Token)
async def login(
    data: LoginRequest,
    db: AsyncIOMotorDatabase = Depends(get_perm_database)
) -> Any:
    # 查找 PermiHub-AI 的 accounts 集合中的用户 (不区分大小写并去除首尾空格)
    username = data.username.strip()
    
    # 使用正则表达式进行不区分大小写的查找
    user = await db["accounts"].find_one({"username": {"$regex": f"^{username}$", "$options": "i"}})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 验证密码（PermiHub-AI 使用 bcrypt 加密）
    hashed_password = user.get("password")
    if not verify_password(data.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查状态 (确保 status 为 1)
    if user.get("status") != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已停用",
        )
    
    # 生成 Token，Payload 为用户名
    access_token = create_access_token(subject=user["username"])
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get("/me")
async def get_me(
    db: AsyncIOMotorDatabase = Depends(get_perm_database)
) -> Any:
    # 简易实现：在实际生产中应添加 JWT 校验中间件
    return {"username": "Admin", "role": "admin"}
