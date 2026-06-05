"""
Authentication routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from core.database import get_db
from core.security import (
    hash_password, verify_password, create_access_token, 
    create_refresh_token, decode_token
)
from models.models import User, UserRole
from schemas.auth import UserSignUp, UserLogin, TokenResponse
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/signup", response_model=TokenResponse)
async def signup(user_data: UserSignUp, db: Session = Depends(get_db)):
    """User signup endpoint"""
    try:
        # Check if email exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        new_user = User(
            id=str(uuid.uuid4()),
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role=UserRole.CUSTOMER,
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Create tokens
        access_token = create_access_token(
            user_id=new_user.id,
            email=new_user.email,
            role=new_user.role.value
        )
        refresh_token = create_refresh_token(
            user_id=new_user.id,
            email=new_user.email,
            role=new_user.role.value
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user_id=new_user.id,
            email=new_user.email,
            role=new_user.role.value
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Signup error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """User login endpoint"""
    try:
        user = db.query(User).filter(User.email == credentials.email).first()
        if not user or not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        access_token = create_access_token(
            user_id=user.id,
            email=user.email,
            role=user.role.value
        )
        refresh_token = create_refresh_token(
            user_id=user.id,
            email=user.email,
            role=user.role.value
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user_id=user.id,
            email=user.email,
            role=user.role.value
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed"
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token: str):
    """Refresh access token"""
    try:
        token_data = decode_token(token)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        new_access_token = create_access_token(
            user_id=token_data.sub,
            email=token_data.email,
            role=token_data.role
        )
        
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=token,
            token_type="bearer",
            user_id=token_data.sub,
            email=token_data.email,
            role=token_data.role
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )
