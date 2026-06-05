"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# Authentication Schemas
class UserSignUp(BaseModel):
    """User signup request"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str
    last_name: str


class UserLogin(BaseModel):
    """User login request"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response"""
    access_token: str
    refresh_token: str
    token_type: str
    user_id: str
    email: str
    role: str


class UserResponse(BaseModel):
    """User response"""
    id: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str]
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Business Schemas
class BusinessCreate(BaseModel):
    """Create business request"""
    business_name: str
    business_email: EmailStr
    phone: str
    industry: str
    website: Optional[str]
    description: Optional[str]


class BusinessUpdate(BaseModel):
    """Update business request"""
    business_name: Optional[str]
    phone: Optional[str]
    industry: Optional[str]
    website: Optional[str]
    description: Optional[str]


class BusinessResponse(BaseModel):
    """Business response"""
    id: str
    business_name: str
    business_email: str
    phone: str
    industry: str
    is_verified: bool
    subscription_tier: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Lead Schemas
class LeadCreate(BaseModel):
    """Create lead request"""
    name: str
    email: EmailStr
    phone: Optional[str]
    company: Optional[str]
    position: Optional[str]
    source: str


class LeadUpdate(BaseModel):
    """Update lead request"""
    status: Optional[str]
    score: Optional[float]
    notes: Optional[str]
    tags: Optional[List[str]]


class LeadResponse(BaseModel):
    """Lead response"""
    id: str
    name: str
    email: str
    company: Optional[str]
    status: str
    score: float
    source: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Customer Schemas
class CustomerCreate(BaseModel):
    """Create customer request"""
    name: str
    email: EmailStr
    phone: Optional[str]
    company: Optional[str]


class CustomerResponse(BaseModel):
    """Customer response"""
    id: str
    name: str
    email: str
    company: Optional[str]
    lifetime_value: float
    churn_risk: float
    created_at: datetime
    
    class Config:
        from_attributes = True


# Pagination Schemas
class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class PaginatedResponse(BaseModel):
    """Paginated response"""
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List


# Analytics Schemas
class AnalyticsResponse(BaseModel):
    """Analytics response"""
    metric: str
    value: float
    trend: Optional[float]
    timestamp: datetime
