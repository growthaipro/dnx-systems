from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, Text, JSON, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
import uuid
import enum

class LeadSource(str, enum.Enum):
    WEBSITE = "website"
    FACEBOOK = "facebook"
    GOOGLE = "google"
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    EMAIL = "email"
    PHONE = "phone"
    REFERRAL = "referral"
    ORGANIC = "organic"
    PAID_ADS = "paid_ads"
    OTHER = "other"

class LeadStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    NEGOTIATION = "negotiation"
    CONVERTED = "converted"
    LOST = "lost"
    NURTURE = "nurture"

class Lead(Base):
    __tablename__ = "leads"
    __table_args__ = (
        Index('idx_business_status', 'business_id', 'status'),
        Index('idx_business_created', 'business_id', 'created_at'),
    )

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String(36), ForeignKey("businesses.id"), nullable=False, index=True)
    
    # Lead Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    company = Column(String(255), nullable=True)
    job_title = Column(String(100), nullable=True)
    website = Column(String(255), nullable=True)
    
    # Lead Details
    message = Column(Text, nullable=True)
    source = Column(SQLEnum(LeadSource), nullable=True)
    status = Column(SQLEnum(LeadStatus), default=LeadStatus.NEW, index=True)
    
    # Scoring
    lead_score = Column(Float, default=0.0)
    conversion_probability = Column(Float, default=0.0)
    estimated_value = Column(Float, default=0.0)
    
    # Assignment
    assigned_to_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    assigned_at = Column(DateTime, nullable=True)
    
    # Tracking
    last_contacted_at = Column(DateTime, nullable=True)
    next_followup_at = Column(DateTime, nullable=True)
    conversion_date = Column(DateTime, nullable=True)
    
    # Metadata
    metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    business = relationship("Business", back_populates="leads")
    assigned_user = relationship("User", foreign_keys=[assigned_to_id])

    def __repr__(self):
        return f"<Lead {self.email}>"