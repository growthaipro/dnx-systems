from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
import uuid
import enum

class BusinessType(str, enum.Enum):
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

class BusinessStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"

class Business(Base):
    __tablename__ = "businesses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String(36), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    business_type = Column(SQLEnum(BusinessType), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20), nullable=True)
    website = Column(String(255), nullable=True)
    logo_url = Column(String(500), nullable=True)
    banner_url = Column(String(500), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Verification
    verified = Column(Boolean, default=False)
    verification_token = Column(String(255), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    
    # Subscription
    subscription_plan = Column(String(50), default="free")
    subscription_active = Column(Boolean, default=True)
    subscription_expires_at = Column(DateTime, nullable=True)
    
    # Status
    status = Column(SQLEnum(BusinessStatus), default=BusinessStatus.ACTIVE)
    
    # Metadata
    metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    users = relationship("User", back_populates="business", cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="business", cascade="all, delete-orphan")
    customers = relationship("Customer", back_populates="business", cascade="all, delete-orphan")
    campaigns = relationship("Campaign", back_populates="business", cascade="all, delete-orphan")
    creatives = relationship("Creative", back_populates="business", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Business {self.name}>"