from typing import Annotated
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy import select
from app.model.model import User
from app.schema.schema import UserLoginRequest, UserLoginResponse, UserRegisterRequest, UserRegisterResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_db
from app.config.config import hash_password ,verify_password,encode_access_token
from sqlalchemy.exc import IntegrityError

router=APIRouter()

@router.post("/register", response_model=UserRegisterResponse)
async def register(
    request: UserRegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    new_user = User(
        first_name=request.first_name.strip(),
        last_name=request.last_name.strip(),
        email=request.email.strip(),
        phone=request.phone.strip(),
        password=hash_password(request.password)
    )

    db.add(new_user)

    try:
        await db.commit()
        await db.refresh(new_user)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

    return UserRegisterResponse(
        id=new_user.id,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        phone=new_user.phone,
        created_at=new_user.created_at.isoformat(),
        updated_at=new_user.updated_at.isoformat(),
    )


@router.post("/login", response_model=UserLoginResponse)
async def login(
    request: UserLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    email = request.email.strip()
    password = request.password.strip()

    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    return UserLoginResponse(
        access_token=encode_access_token(
            user.id,
            user.email
        )
    )
