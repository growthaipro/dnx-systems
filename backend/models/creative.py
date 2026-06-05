from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, Text, JSON, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
import uuid
import enum

class CreativeType(str, enum.Enum):
    BANNER = "banner"
    POSTER = "poster"
    FLYER = "flyer"
    CAROUSEL = "carousel"
    SOCIAL_POST = "social_post"
    VIDEO_AD = "video_ad"
    PRODUCT_AD = "product_ad"
    LOGO = "logo"

class CreativeStatus(str, enum.Enum):
    DRAFT = "draft"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class Creative(Base):
    __tablename__ = "creatives"
    __table_args__ = (
        Index('idx_business_type', 'business_id', 'creative_type'),
        Index('idx_business_created', 'business_id', 'created_at'),
    )

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String(36), ForeignKey("businesses.id"), nullable=False, index=True)
    
    # Creative Details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    creative_type = Column(SQLEnum(CreativeType), nullable=False)
    status = Column(SQLEnum(CreativeStatus), default=CreativeStatus.DRAFT)
    
    # Content
    content = Column(JSON, nullable=True)  # Store design data
    image_url = Column(String(500), nullable=True)
    video_url = Column(String(500), nullable=True)
    url = Column(String(500), nullable=True)
    
    # AI Generation
    ai_generated = Column(Boolean, default=False)
    ai_model = Column(String(100), nullable=True)
    
    # Performance
    views = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    
    # Metadata
    metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    business = relationship("Business", back_populates="creatives")

    def __repr__(self):
        return f"<Creative {self.title}>"