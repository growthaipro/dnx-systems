from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class BusinessType(str, Enum):
    RESTAURANT = "restaurant"
    HOSPITAL = "hospital"
    CLINIC = "clinic"
    COLLEGE = "college"
    TRAINING_INSTITUTE = "training_institute"
    REAL_ESTATE = "real_estate"
    CONSULTING = "consulting"
    RETAIL = "retail"
    FREELANCER = "freelancer"
    STARTUP = "startup"
    ENTERPRISE = "enterprise"
    OTHER = "other"

class BusinessBase(BaseModel):
    name: str
    business_type: BusinessType
    email: EmailStr
    phone: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None

class BusinessCreate(BusinessBase):
    pass

class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None

class BusinessResponse(BusinessBase):
    id: str
    owner_id: str
    verified: bool
    subscription_plan: str
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True