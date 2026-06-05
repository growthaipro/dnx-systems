from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, Text, JSON, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
import uuid
import enum

class CampaignType(str, enum.Enum):
    FACEBOOK_ADS = "facebook_ads"
    INSTAGRAM_ADS = "instagram_ads"
    GOOGLE_ADS = "google_ads"
    YOUTUBE_ADS = "youtube_ads"
    LINKEDIN_ADS = "linkedin_ads"
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    ORGANIC = "organic"

class CampaignStatus(str, enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class Campaign(Base):
    __tablename__ = "campaigns"
    __table_args__ = (
        Index('idx_business_status', 'business_id', 'status'),
        Index('idx_business_created', 'business_id', 'created_at'),
    )

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String(36), ForeignKey("businesses.id"), nullable=False, index=True)
    
    # Campaign Details
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    campaign_type = Column(SQLEnum(CampaignType), nullable=False)
    status = Column(SQLEnum(CampaignStatus), default=CampaignStatus.DRAFT, index=True)
    
    # Budget & Pricing
    budget = Column(Float, default=0.0)
    actual_spend = Column(Float, default=0.0)
    currency = Column(String(3), default="USD")
    
    # Dates
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    scheduled_at = Column(DateTime, nullable=True)
    
    # Performance
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    ctr = Column(Float, default=0.0)  # Click Through Rate
    cvr = Column(Float, default=0.0)  # Conversion Rate
    cpc = Column(Float, default=0.0)  # Cost Per Click
    cpa = Column(Float, default=0.0)  # Cost Per Action
    roi = Column(Float, default=0.0)  # Return on Investment
    
    # Audience & Targeting
    target_audience = Column(JSON, nullable=True)
    target_locations = Column(JSON, nullable=True)
    target_demographics = Column(JSON, nullable=True)
    
    # Metadata
    metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    business = relationship("Business", back_populates="campaigns")

    def __repr__(self):
        return f"<Campaign {self.name}>"