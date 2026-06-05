"""
User management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from models.models import User, UserRole
from schemas.auth import UserResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/profile/{user_id}", response_model=UserResponse)
async def get_user_profile(user_id: str, db: Session = Depends(get_db)):
    """Get user profile"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error getting user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user profile"
        )


@router.put("/profile/{user_id}", response_model=UserResponse)
async def update_user_profile(
    user_id: str,
    update_data: dict,
    db: Session = Depends(get_db)
):
    """Update user profile"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        for field, value in update_data.items():
            if hasattr(user, field) and field not in ['id', 'email', 'password_hash']:
                setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error updating user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user profile"
        )


@router.get("/list")
async def list_users(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """List all users (admin only)"""
    try:
        users = db.query(User).offset(skip).limit(limit).all()
        total = db.query(User).count()
        
        return {
            "total": total,
            "data": users
        }
    except Exception as e:
        logger.error(f"Error listing users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving users"
        )
